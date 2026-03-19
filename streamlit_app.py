import streamlit as st
import google.generativeai as genai
from PIL import Image
import os

# --- 設定エリア ---
st.set_page_config(page_title="献立お助けAI", layout="centered")

# サイドバーでAPIキーを入力（またはコードに直接書くことも可能）
api_key = st.sidebar.text_input("Gemini API Keyを入力してください", type="password")

if api_key:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-1.5-flash') # 高速なFlashモデルを使用

st.title("🍳 献立お助け＆カロリー計算AI")
st.write("冷蔵庫の中身や食材を写真に撮ってアップロードしてください。")

# --- 画像アップロード ---
uploaded_file = st.file_uploader("写真をアップロード...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption='アップロードされた画像', use_column_width=True)
    
    submit = st.button("献立を考えてもらう！")

    if submit:
        if not api_key:
            st.error("APIキーを入力してください。")
        else:
            with st.spinner('AIが献立を考案中...'):
                # AIへの指示（プロンプト）
                prompt = """
                画像に写っている食材を特定し、それらを使って作れる献立を3つ提案してください。
                
                【条件】
                1. 以下のサイトのレシピを参考に、またはそのテイストで提案すること：
                   - きょうの料理 (kyounoryouri.jp)
                   - 白ごはん.com (sirogohan.com)
                   - 久原醤油 (kubara.jp)
                   - 山本ゆり (ameblo.jp/syunkon)
                   - オレンジページ (orangepage.net)
                   - おかずのクッキング/山本ゆり (asahi.co.jp/daidokoro)
                
                2. 各提案には以下を含めてください：
                   - 料理名
                   - おおよそのカロリー（1人前）
                   - その料理が載っていそうなサイトへの「Google検索リンク」
                     (形式: https://www.google.com/search?q=site:[ドメイン]+[料理名])
                   - 選んだ理由やコツ
                
                3. 回答は親しみやすい日本語でお願いします。
                """
                
                # Geminiに画像とテキストを送る
                response = model.generate_content([prompt, image])
                
                st.subheader("💡 AIからの提案")
                st.markdown(response.text)

else:
    st.info("左側のサイドバーにAPIキーを入れ、ここに写真をアップしてください。")

# --- フッター ---
st.markdown("---")
st.caption("※カロリーはAIによる概算です。正確な数値は各レシピサイトをご確認ください。")
