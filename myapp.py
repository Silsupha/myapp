import openai
import streamlit as st
import pandas as pd

# Set your OpenAI API key
openai.api_key = "YOUR_OPENAI_API_KEY"

# Function to perform sentiment analysis using OpenAI GPT-3.5-turbo
def analyze_sentiment(input_text):
    # Call the OpenAI API with GPT-3.5-turbo
    response = openai.Completion.create(
        engine="text-davinci-002",  # Specify the GPT-3.5-turbo engine
        prompt=f"Analyze the sentiment of the following text: {input_text}",
        max_tokens=50,  # Adjust max_tokens as needed
        temperature=0.7,  # Adjust temperature as needed
    )
    
    # Extract sentiment from the response
    sentiment_result = response["choices"][0]["text"].strip()
    
    return sentiment_result

# Streamlit UI
def main():
    st.title("Sentiment Analysis App")
    
    # Input Form for Text
    text_input = st.text_area("Enter Text for Sentiment Analysis", "")

    # Button to Trigger Analysis
    if st.button("Analyze Sentiment"):
        if text_input:
            # Call the function to perform sentiment analysis
            sentiment_result = analyze_sentiment(text_input)

            # Display results using pandas dataframe
            result_df = pd.DataFrame({"Text": [text_input], "Sentiment": [sentiment_result]})
            st.dataframe(result_df)

            # Provide Download Link for Results as CSV
            csv_data = result_df.to_csv(index=False).encode()
            st.download_button(
                label="Download Results as CSV",
                data=csv_data,
                file_name="sentiment_results.csv",
                key="download_csv",
            )
        else:
            st.warning("Please enter text for analysis.")

if __name__ == "__main__":
    main()
