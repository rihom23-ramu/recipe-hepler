import streamlit as st
import google.generativeai as genai
from PIL import Image
import os

# --- ページ設定 (カフェ風アイコンに) ---
st.set_page_config(page_title="献立お助け Cafe 2026", page_icon="🥗", layout="centered")

# --- ✨ カフェ風スタイル調整 (追加！) ✨ ---
st.markdown("""
    <style>
    /* 全体の背景を温かみのあるクリーム色に */
    .stApp { background-color: #fffaf0; }
    
    /* ボタンのスタイルを丸く、アースカラーに */
    .stButton>button { 
        width: 100%; 
        border-radius: 20px; 
        background-color: #8fbc8f; /* サージグリーン */
        color: white; 
        border: none;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        font-weight: bold;
    }
    .stButton>button:hover {
        background-color: #ff7f50; /* ホバー時はアースオレンジ */
    }
    
    /* タイトルのフォントを少しおしゃれに */
    h1 {
        color: #4b3621; /* ダークブラウン */
        font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
    }
    
    /* 画像のアップロードエリアを丸く */
    .stFileUploader {
        border-radius: 15px;
        background-color: rgba(255,255,255,0.8);
        border: 2px dashed #8fbc8f;
    }
    
    /* 提案セクションをカード風に */
    .stAlert {
        border-radius: 15px;
        background-color: rgba(255,255,255,0.7);
        border: 1px solid #ddd;
    }
    </style>
    """, unsafe_allow_html=True)

# --- サイドバー：API設定 ---
st.sidebar.header("⚙️ 設定")
api_key = st.sidebar.text_input("Gemini API Key を入力", type="password")

# --- メイン画面 ---
st.title("🥗 献立お助け Cafe - 2026")
st.write("食材や冷蔵庫の写真をからレシピのヒントをもらっちゃお！")

uploaded_file = st.file_uploader("食材や冷蔵庫の写真をアップロード...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption='読み込んだ写真', use_container_width=True)
    
    # ボタンエリア
    col1, col2 = st.columns(2)
    with col1:
        submit = st.button("✨ 献立を3案提案！")
    with col2:
        # --- 🔄 「他の候補を探す」機能を追加！ 🔄 ---
        refind = st.button("🔄 他の候補を探す")

    if submit or refind:
        if not api_key:
            st.error("🔑 左側のサイドバーに API Key を入力してください。")
        else:
            genai.configure(api_key=api_key)
            
            # 安定している2026年のFlashモデル
            model_name = 'models/gemini-2.5-flash'
            
            # --- プロンプトの調整：他の候補を探す場合 ---
            if refind:
                prompt_instruction = "画像から食材を特定し、それらを使って作れる*先ほどとは異なる*献立を3つ提案してください。異なるレシピサイトを参照するか、別の調理方法を提案してください。"
            else:
                prompt_instruction = "画像に写っている食材を特定し、それらを使って作れる献立を3つ提案してください。"

            try:
                model = genai.GenerativeModel(model_name)
                
                with st.spinner('AIがレシピを探索中...'):
                    prompt = f"""
                    {prompt_instruction}
                    
                    【参照サイト】
                    - きょうの料理, 白ごはん.com, 久原醤油, 山本ゆりさんブログ, オレンジページ, 朝日放送 おかずのクッキング

                    【出力項目】
                    1. 料理名（カフェメニューのような名前で）
                    2. おおよそのカロリー（1人前あたり）
                    3. Google検索リンク（https://www.google.com/search?q=site:[ドメイン]+[料理名]）
                    4. ワンポイント（カフェ風アレンジや、山本ゆりさん風時短コツなど）

                    親しみやすく、プロらしいアドバイスをお願いします。
                    """
                    
                    # AIによる生成
                    response = model.generate_content([prompt, image])
                    
                    st.success("✨ 献立が見つかりました！")
                    st.markdown("---")
                    st.markdown(response.text)

            except Exception as e:
                st.error(f"❌ エラーが発生しました: {e}")

else:
    st.info("💡 まずは左のメニューにAPIキーを入れ、食材の写真をアップしてね。")

# --- フッター ---
st.markdown("---")
st.caption("Produced by Gemini 2.5 Flash Cafe Assistant | 2026")
