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

    # Create a dataframe with multiple-choice questions, correct answers, and explanations
    result_df = pd.DataFrame(columns=['Question', 'Choice A', 'Choice B', 'Choice C', 'Choice D', 'Correct Answer'])

    # Populate the dataframe
    for i in range(0, len(mcq_data), 6):
        question = mcq_data[i]
        choices = mcq_data[i + 1:i + 5]
        correct_answer = mcq_data[i + 4] if i + 4 < len(mcq_data) else ""

        result_df = result_df.append({
            'Question': question,
            'Choice A': choices[0] if len(choices) > 0 else "",
            'Choice B': choices[1] if len(choices) > 1 else "",
            'Choice C': choices[2] if len(choices) > 2 else "",
            'Choice D': choices[3] if len(choices) > 3 else "",
            'Correct Answer': correct_answer
        }, ignore_index=True)

    # Display the resulting dataframe
    st.subheader('Generated Multiple-Choice Questions:')
    st.table(result_df)
