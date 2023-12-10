import streamlit as st
import pandas as pd
import openai
import string

# เติม OpenAI API key ผ่าน sidebar
openai.api_key = st.sidebar.text_input("Enter your OpenAI API key", type="password")

# ฟังก์ชันสำหรับสรุปบทความ
def summarize_article(article):
    prompt = f"Summarize the following article:\n{article}"
    response = openai.chat.completions.create(
        model="text-davinci-002",
        messages=prompt,
        max_tokens=150
    )
    return response.choices[0].text.strip()

# ฟังก์ชันสำหรับดึงคำศัพท์ยากและ synonym
def extract_difficult_words(article):
    words = article.translate(str.maketrans("", "", string.punctuation)).split()

    difficult_words = []
    synonyms = []

    for word in words:
        if len(word) > 5 and word.isalpha() and word not in difficult_words:
            difficult_words.append(word)
            # For simplicity, we're not including synonyms without additional packages

    return difficult_words[:10], synonyms[:10]

# หน้าหลักของ Streamlit application
def main():
    st.title("Article Summarizer and Difficult Words Extractor")

    # รับ input จากผู้ใช้
    article = st.text_input

    # กรณีมีข้อความใน input
    if article:
        # สรุปบทความ
        summary = summarize_article(article)
        st.subheader("Article Summary:")
        st.write(summary)

        # ดึงคำศัพท์ยากและ synonym
        difficult_words, synonyms = extract_difficult_words(article)

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
