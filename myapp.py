import streamlit as st
import openai
import pandas as pd

# Set OpenAI API key
user_api_key = st.sidebar.text_input("OpenAI API key", type="password")
client = openai.OpenAI(api_key=user_api_key)

# Streamlit app
st.title('Multiple-Choice Question Generator')
st.markdown('Input a passage, and the app will generate multiple-choice questions for you.')

# User input for the passage
passage_input = st.text_area("Enter a passage:", "Your passage here")

# submit button after passage input
if st.button('Generate Multiple-Choice Questions'):
    # Create a message array with system message and user message
    messages = [
        {"role": "system", "content": "Generate multiple-choice questions for the given passage:"},
        {"role": "user", "content": passage_input},
    ]

    # Request multiple-choice questions from OpenAI
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages,
        temperature=0.5,
        max_tokens=200
    )

    # Extract multiple-choice questions, correct answers, and explanations from the response
    mcq_data = response.choices[0].message.content.split('\n')

    # Create a list to store rows
    rows = []

    # Populate the list
    for i in range(0, len(mcq_data), 6):
        question = mcq_data[i]
        choices = mcq_data[i + 1:i + 5]

        # Extract the correct answer by checking for "(Correct)" in each choice
        correct_answer = next((choice.replace("(Correct)", "").strip() for choice in choices if "(Correct)" in choice), "")

        rows.append({
            'Question': question,
            'Choice A': choices[0] if len(choices) > 0 else "",
            'Choice B': choices[1] if len(choices) > 1 else "",
            'Choice C': choices[2] if len(choices) > 2 else "",
            'Choice D': choices[3] if len(choices) > 3 else "",
            'Correct Answer': correct_answer
        })

    # Create the dataframe
    result_df = pd.DataFrame(rows)

    # Display the resulting dataframe
    st.subheader('Generated Multiple-Choice Questions:')
    st.table(result_df)
