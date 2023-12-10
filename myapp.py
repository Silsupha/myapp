import streamlit as st
import pandas as pd
import openai
from bs4 import BeautifulSoup
import requests
from nltk.corpus import wordnet

# เติม OpenAI API key ผ่าน sidebar
openai.api_key = st.sidebar.text_input("Enter your OpenAI API key", type="password")

# ฟังก์ชันสำหรับดึงข้อมูลจาก URL
def fetch_data_from_url(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    paragraphs = soup.find_all('p')
    text = ' '.join([paragraph.get_text() for paragraph in paragraphs])
    return text

# ฟังก์ชันสำหรับสรุปข่าว
def summarize_news(url):
    news_text = fetch_data_from_url(url)

    # ให้ LLM ประมวลผลข้อความ
    prompt = f"Summarize the following news article:\n{news_text}"
    response = openai.chat.completions.create(
        model="text-davinci-002",
        messages=prompt,
        max_tokens=150
    )
    summary = response.choices[0].text.strip()

    return summary

# ฟังก์ชันสำหรับดึงคำศัพท์ยากและ synonym จากข่าว
def extract_difficult_words(news_text):
    # ใช้ nltk เพื่อหาคำศัพท์
    words = nltk.word_tokenize(news_text)

    difficult_words = []
    synonyms = []

    # เลือกคำศัพท์ที่ยาก
    for word in words:
        if len(word) > 5 and word.isalpha() and word not in difficult_words:
            difficult_words.append(word)

            # หา synonym จาก WordNet
            syns = wordnet.synsets(word)
            if syns:
                synonyms.append(syns[0].lemmas()[0].name())
            else:
                synonyms.append("No synonym found")

    return difficult_words[:10], synonyms[:10]

# หน้าหลักของ Streamlit application
def main():
    st.title("News Summarizer and Difficult Words Extractor")

    # รับ input URL จากผู้ใช้
    news_url = st.text_input("Enter the URL of the news article:")
    if not news_url:
        st.warning("Please enter a valid URL.")
        st.stop()

    # สรุปข่าว
    news_summary = summarize_news(news_url)
    st.subheader("News Summary:")
    st.write(news_summary)

    # ดึงคำศัพท์ยากและ synonym
    difficult_words, synonyms = extract_difficult_words(news_summary)

    # แสดงผลลัพธ์ในรูปแบบของ pandas dataframe
    df_result = pd.DataFrame({"Difficult Words": difficult_words, "Synonyms": synonyms})
    st.subheader("Difficult Words and Synonyms:")
    st.dataframe(df_result, index=False)

    # สร้างลิงก์สำหรับดาวน์โหลดผลลัพธ์เป็นไฟล์ CSV
    csv_link = create_download_link(df_result, "Download Difficult Words and Synonyms")
    st.markdown(csv_link, unsafe_allow_html=True)

# ฟังก์ชันสร้างลิงก์ดาวน์โหลดไฟล์ CSV
def create_download_link(df, text):
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()
    href = f'<a href="data:file/csv;base64,{b64}" download="difficult_words_synonyms.csv">{text}</a>'
    return href

if __name__ == "__main__":
    main()


    

