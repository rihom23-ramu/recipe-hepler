import streamlit as st
import google.generativeai as genai
from PIL import Image

# --- ページ設定 ---
st.set_page_config(page_title="献立お助け Cafe 2026", page_icon="🥗", layout="centered")

# --- カフェ風スタイル調整 ---
st.markdown("""
    <style>
    .stApp { background-color: #fffaf0; }
    .stButton>button { width: 100%; border-radius: 20px; background-color: #8fbc8f; color: white; border: none; box-shadow: 0 4px 6px rgba(0,0,0,0.1); font-weight: bold; }
    .stButton>button:hover { background-color: #ff7f50; }
    h1 { color: #4b3621; }
    /* 説明文をよりコンパクトに表示するための工夫 */
    .recipe-card { background-color: white; padding: 10px; border-radius: 10px; border-left: 5px solid #8fbc8f; margin-bottom: 10px; }
    </style>
    """, unsafe_allow_html=True)

st.sidebar.header("⚙️ 設定")
api_key = st.sidebar.text_input("Gemini API Key を入力", type="password")

st.title("🥗 献立お助け Cafe - 2026")
uploaded_file = st.file_uploader("写真をアップロード...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, use_container_width=True)
    
    col1, col2 = st.columns(2)
    with col1:
        submit = st.button("✨ 献立を3案提案！")
    with col2:
        refind = st.button("🔄 他の候補を探す")

    if submit or refind:
        if not api_key:
            st.error("🔑 API Key を入力してください。")
        else:
            genai.configure(api_key=api_key)
            model_name = 'models/gemini-2.5-flash'
            
            # 説明を短くするための指示を追加
            short_instruction = "説明は1案につき20文字以内で、一言アドバイスのみにしてください。"
            
            if refind:
                prompt_instruction = f"画像から食材を特定し、先ほどとは違う献立を3つ提案して。{short_instruction}"
            else:
                prompt_instruction = f"画像から食材を特定し、献立を3つ提案して。{short_instruction}"

            try:
                model = genai.GenerativeModel(model_name)
                with st.spinner('探索中...'):
                    prompt = f"""
                    {prompt_instruction}
                    
                    【出力形式（厳守）】
                    ■ [料理名] ([カロリー])
                    - [Google検索リンク]
                    - ひとこと：[20文字以内のアドバイス]
                    
                    【参照サイト】
                    きょうの料理, 白ごはん.com, 久原醤油, 山本ゆりさん, オレンジページ
                    """
                    
                    response = model.generate_content([prompt, image])
                    st.success("✨ 提案はこちら！")
                    st.markdown(response.text)

            except Exception as e:
                st.error(f"❌ エラー: {e}")
else:
    st.info("💡 写真をアップしてね。")
