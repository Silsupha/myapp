import streamlit as st
import openai

# Set your OpenAI API key
user_api_key = st.sidebar.text_input("Enter OpenAI API Key", type="password")

client = openai.OpenAI(api_key=user_api_key)
prompt = """Act as an AI writing tutor in English. You will receive a 
            piece of writing and you should give suggestions on how to improve it.
            List the suggestions in a JSON array, one suggestion per line.
            Each suggestion should have 3 fields:
            - "before" - the text before the suggestion
            - "after" - the text after the suggestion
            - "category" - the category of the suggestion one of "grammar", "style", "word choice", "other"
            - "comment" - a comment about the suggestion
            Don't say anything at first. Wait for the user to say something.
        """    

st.title("Text Analysis and Transformation App")

input_text = st.text_area("Enter text for analysis:", "")

def analyze_and_transform_text(input_text):
    message = [
        {"role": "system", "content": prompt},
        {'role': 'user', 'content': input_text},
    ]
    # Use the GPT-3.5-turbo engine to analyze and transform text
    response = client.chat.completions.create(
        model="text-davinci-002",
        messages=message,
        temperature=0.7,
        max_tokens=150
    )
    print(response)
    transformed_text = response['choices'][0]['message']['content']
    return transformed_text

if st.button("Analyze and Transform"):
    if input_text:
        # Call the function to analyze and transform text
        transformed_text = analyze_and_transform_text(input_text)

        # Display original and transformed text using Pandas DataFrame
        result_df = pd.DataFrame({
            "Original Text": [input_text],
            "Transformed Text": [transformed_text]})
        st.dataframe(result_df)

        # Provide Download Link for Results as CSV
        csv_data = result_df.to_csv(index=False).encode()
        st.download_button(
            label="Download Results as CSV",
            data=csv_data,
            file_name="text_analysis_results.csv",
            key="download_csv"
            )


    

