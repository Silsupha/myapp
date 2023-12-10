import streamlit as st
import openai
import json
import pandas as pd

# Get the API key from the sidebar called OpenAI API key
user_api_key = st.sidebar.text_input("OpenAI API key", type="password")

client = openai.OpenAI(api_key=user_api_key)
prompt = """Transform the following informal sentences into formal language and remove any unnecessary sentences:
"""

st.title('Formalization and Sentence Filtering App')
st.markdown('Input a list of informal sentences. The AI will transform them into formal language and filter out unnecessary sentences.')

user_input = st.text_area("Enter informal sentences (one per line):", "Your sentences here")

# submit button after text input
if st.button('Transform and Filter'):
    sentences = user_input.split('\n')
    messages_so_far = [
        {"role": "system", "content": prompt},
        {'role': 'user', 'content': user_input},
    ]
    response = client.chat.completions.create(
        model="text-davinci-003",
        messages=messages_so_far
    )
    # Show the response from the AI in a box
    st.markdown('**AI response:**')
    suggestion_dictionary = response.choices[0].message.content

    sd = json.loads(suggestion_dictionary)
    suggestion_df = pd.DataFrame.from_dict(sd)
    
    # Display the transformed and filtered result
    st.table(suggestion_df)
