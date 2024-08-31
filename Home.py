import streamlit as st
import openai
import PyPDF2

st.set_page_config(
    page_title="Lexia chatbot",
    layout="wide",
)

# Function to read the document
def read_document(file):
    if file.type == "application/pdf":
        reader = PyPDF2.PdfReader(file)
        text = ""
        for page in range(len(reader.pages)):
            text += reader.pages[page].extract_text()
        return text
    else:
        return "Unsupported file type"


# Streamlit app
def main():
    st.title("Document Interaction Chatbot")

    # Sidebar configuration
    st.sidebar.title("Settings")

    # Input field for OpenAI API key in the sidebar
    openai_key = st.sidebar.text_input("Enter your OpenAI API Key:", type="password")

    if openai_key:
        openai.api_key = openai_key

        # Upload a document in the sidebar
        uploaded_file = st.sidebar.file_uploader("Upload a document", type=["pdf"])

        if uploaded_file is not None:
            document_text = read_document(uploaded_file)
            st.sidebar.write("Document content loaded. You can now interact with it.")

            # System prompt input in the sidebar
            system_prompt = st.sidebar.text_area(
                "Enter System Prompt (context for the AI)",
                value="You are a helpful assistant."
            )

            # Model selection in the sidebar
            model_name = st.sidebar.selectbox(
                "Choose OpenAI model",
                options=["gpt-4", "gpt-3.5-turbo", "gpt-3.5-turbo-16k"]
            )

            # Max tokens input in the sidebar
            max_tokens = st.sidebar.slider(
                "Set the maximum number of tokens for the response",
                min_value=50,
                max_value=500,
                value=150
            )

            # Temperature input in the sidebar
            temperature = st.sidebar.slider(
                "Set the temperature (creativity level)",
                min_value=0.0,
                max_value=1.0,
                value=0.7
            )

            # Chatbot interaction in the main screen
            user_question = st.text_input("Ask something about the document:")

            if user_question:
                response = openai.ChatCompletion.create(
                    model=model_name,
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": f"Document content: {document_text}"},
                        {"role": "user", "content": user_question},
                    ],
                    max_tokens=max_tokens,
                    temperature=temperature
                )

                st.write(response['choices'][0]['message']['content'])

            # Ensure data privacy
            st.sidebar.warning("Note: This interaction is private, and the data is not used for training.")


if __name__ == "__main__":
    main()
