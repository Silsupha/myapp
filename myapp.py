import streamlit as st
import openai
import json
import pandas as pd

# Get the OpenAI API key from the user through the sidebar
user_api_key = st.sidebar.text_input("OpenAI API key", type="password")

# Initialize the OpenAI GPT-3 client
openai.api_key = user_api_key

# Streamlit app
st.title("Historical Events Summarizer")
st.markdown("Enter a piece of text, and the app will summarize the events that occurred in different years.")

# Input text from the user
user_input = st.text_area("Enter the article or text:", "")

# Submit button
if st.button("Summarize Events"):
    # Create a prompt using user input
    prompt = f"Summarize the events that occurred in different years based on the following text:\n\n{user_input}"

    # Generate response from GPT-3 model
    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        prompt=prompt,
        max_tokens=400
    )

    # Extract summarized events from the generated response
    summarized_events = response.choices[0].text.strip()

    # Parse the summarized events into a DataFrame
    events_list = [event.split(': ') for event in summarized_events.split('\n')]
    events_df = pd.DataFrame(events_list, columns=["Year", "Event"])

    # Display the result
    st.subheader("Summarized Events:")
    st.table(events_df)
