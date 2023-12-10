import streamlit as st
import openai
import pandas as pd

# Get the API key from the sidebar called OpenAI API key
user_api_key = st.sidebar.text_input("OpenAI API key", type="password")

client = openai.OpenAI(api_key=user_api_key)
prompt = """Act as an AI writing poem. You will receive a 
            group of words and you should give a poem related to those words.
            Don't say anything at first. Wait for the user to say something.
        """    

st.title('Writing Poem Assistant')
st.markdown('Input group of words that you want to write poem about. \n\
            The AI will give you poem related to words you entered.')

user_input = st.text_area("Enter word group : ", "Your words here")

if st.button('Submit'):
            messages_so_far = [{"role": "system", "content": prompt},
            {'role': 'user', 'content': user_input},]

            response = client.chat.completions.create(
                        model="gpt-3.5-turbo",  # Specify the GPT-3.5-turbo engine
                        prompt=prompt_text,
                        max_tokens=150,  # Adjust max_tokens as needed
                        temperature=0.7,)  # Adjust temperature as needed)
            
            # Call the function to generate poem
            poem_result = response.choices[0].text.strip()

            # Show the response from the AI in a box
            st.markdown('**AI response:**')
            
            # Display results using Pandas DataFrame
            result_df = pd.DataFrame({"Generated Poem": [poem_result]})
            st.dataframe(result_df)

            # Provide Download Link for Results as CSV
            csv_data = result_df.to_csv(index=False).encode()
            st.download_button( label="Download Poem as CSV",
                               data=csv_data,
                               file_name="generated_poem.csv",
                               key="download_csv",)
          
