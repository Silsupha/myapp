import streamlit as st
import openai
import pandas as pd

# Get the API key from the sidebar called OpenAI API key
user_api_key = st.sidebar.text_input("OpenAI API key", type="password")
client = openai.OpenAI(api_key=user_api_key)

st.title('Multiple-Choice Question Generator')
st.markdown('Input a passage, and the app will generate multiple-choice (4 choices) questions for you.')

passage_input = st.text_area("Enter a passage:", "Your passage here")

# submit button after text input
if st.button('Generate Multiple-Choice Questions'):
    messages = [
        {"role": "system", "content": "Generate multiple-choice questions for the given passage:"},
        {"role": "user", "content": passage_input},
    ]
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages,
        temperature=0.5,
        max_tokens=200
    )
    
    mcq_data = response.choices[0].message.content.split('\n')

    rows = []
    for i in range(0, len(mcq_data), 6):
        question = mcq_data[i].split('.')[1].strip()  # Remove the question number
        choices = mcq_data[i + 1:i + 5]
        correct_answer = next((choice.replace("(Correct)", "").strip() for choice in choices if "(Correct)" in choice), "")
        if len(choices) == 4:
            rows.append({
                'Question': question,
                'Choice A': choices[0],
                'Choice B': choices[1],
                'Choice C': choices[2],
                'Choice D': choices[3],
                'Correct Answer': correct_answer
            })
    result_df = pd.DataFrame(rows)

    st.subheader('Generated Multiple-Choice Questions:')
    st.table(result_df)
