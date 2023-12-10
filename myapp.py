import streamlit as st
import openai
import pandas as pd

# Set your OpenAI API key via the Streamlit sidebar
openai.api_key = st.sidebar.text_input("Enter your OpenAI API key", type="password")

# Function to summarize text using ChatGPT
def summarize_text(input_text):
    prompt = f"Summarize the following text:\n{input_text}"
    response = openai.chat.completions.create(
        model="text-davinci-002",
        messages=prompt,
        max_tokens=150
    )
    return response.choices[0].text.strip()

# Streamlit app
def main():
    st.title("Text Summarization with ChatGPT")

    # User input: text area to input the text
    input_text = st.text_area("Enter the text you want to summarize:")

    # Process the input and generate a summary
    if st.button("Generate Summary"):
        if input_text:
            summary = summarize_text(input_text)

            # Display the summary
            st.subheader("Summary:")
            st.write(summary)

            # Create a DataFrame to download the summary as CSV
            df_result = pd.DataFrame({"Original Text": [input_text], "Summary": [summary]})
            st.markdown(get_table_download_link(df_result), unsafe_allow_html=True)

# Function to create a download link for a DataFrame
def get_table_download_link(df):
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()
    href = f'<a href="data:file/csv;base64,{b64}" download="summary.csv">Download Summary</a>'
    return href

if __name__ == "__main__":
    main()

