import streamlit as st
import google.generativeai as genai
from PIL import Image

# --- 1. ページ設定 (カフェ風) ---
st.set_page_config(page_title="献立お助け Cafe 2026", page_icon="🥗", layout="centered")

# --- 2. カフェ風スタイル (CSS) ---
st.markdown("""
    <style>
    .stApp { background-color: #fffaf0; }
    .stButton>button { 
        width: 100%; 
        border-radius: 20px; 
        background-color: #8fbc8f; 
        color: white; 
        border: none;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        font-weight: bold;
    }
    .stButton>button:hover { background-color: #ff7f50; }
    h1 { color: #4b3621; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. サイドバー設定 ---
st.sidebar.header("⚙️ 設定")
api_key = st.sidebar.text_input("Gemini API Key を入力", type="password")

# --- 4. メイン画面 ---
st.title("🥗 献立お助け Cafe - 2026")
uploaded_file = st.file_uploader("食材の写真をアップロード...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    
    # 画像軽量化（念のためエラーが出にくい書き方にしています）
    if image.width > 800 or image.height > 800:
        image.thumbnail((800, 800))
        
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
            # 確実に動いたモデル名
            model_name = 'models/gemini-2.5-flash'
            
            # 説明を短く(1/5)するための指示
            short_msg = "説明は1案20文字以内で一言だけにしてください。"
            
            if refind:
                prompt_text = f"画像から食材を特定し、先ほどとは違う献立を3つ提案して。{short_msg}"
            else:
                prompt_text = f"画像から食材を特定し、献立を3つ提案して。{short_msg}"

            try:
                model = genai.GenerativeModel(model_name)
                with st.spinner('カフェの店員が考え中...'):
                    prompt = f"""
                    {prompt_text}
                    
                    【出力形式】
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
                st.error(f"❌ エラーが発生しました。時間を置いて試してください。")
                st.info(f"技術的なエラー詳細: {e}")
else:
    st.info("💡 写真をアップしてね。")

st.markdown("---")
st.caption("Produced by Gemini 2.5 Flash Cafe Assistant")
