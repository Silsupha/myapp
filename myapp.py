import streamlit as st
import pandas as pd

# Function to perform sentiment analysis using OpenAI API
def analyze_sentiment(input_text, api_key):
    # Placeholder code: Replace this with the actual implementation to call OpenAI API
    # For simplicity, this example just returns a random sentiment
    return "Positive" if hash(input_text) % 2 == 0 else "Negative"

# Streamlit UI
def main():
    st.title("Sentiment Analysis App")
    
    # Sidebar for API Key
    api_key = st.sidebar.text_input("Enter OpenAI API Key", type="password")

    # Input Form for Text
    text_input = st.text_area("Enter Text for Sentiment Analysis", "")

    # Button to Trigger Analysis
    if st.button("Analyze Sentiment"):
        if text_input:
            # Call the function to perform sentiment analysis
            sentiment_result = analyze_sentiment(text_input, api_key)

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
