import streamlit as st
import google.generativeai as genai
from PIL import Image
import os

# --- ページ設定 ---
st.set_page_config(page_title="献立お助けAI 2026", page_icon="🍳", layout="centered")

# --- スタイル調整（見た目を少しおしゃれに） ---
st.markdown("""
    <style>
    .main { background-color: #fffaf0; }
    .stButton>button { width: 100%; border-radius: 20px; background-color: #ff7f50; color: white; }
    </style>
    """, unsafe_allow_html=True)

# --- サイドバー：API設定 ---
st.sidebar.header("⚙️ 設定")
api_key = st.sidebar.text_input("Gemini API Key を入力", type="password")

# --- メイン画面 ---
st.title("🍳 献立お助け＆カロリー計算")
st.write("冷蔵庫の写真を撮ってアップするだけで、プロのレシピから献立を提案します。")

# 画像アップローダー
uploaded_file = st.file_uploader("食材や冷蔵庫の写真をアップロード...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption='読み込んだ写真', use_container_width=True)
    
    submit = st.button("献立を考えてもらう！")

    if submit:
        if not api_key:
            st.error("🔑 左側のサイドバーに API Key を入力してください。")
        else:
            # APIの設定
            genai.configure(api_key=api_key)
            
            # ユーザーが見つけた2026年最新モデルを指定
            # もしエラーが出る場合は 'models/gemini-1.5-flash' などに書き換えてください
            model_name = 'models/gemini-3.1-pro-preview'
            
            try:
                model = genai.GenerativeModel(model_name)
                
                with st.spinner('AIがレシピを探索中...'):
                    # プロンプト（AIへの指示書）
                    prompt = f"""
                    画像に写っている食材を特定し、それらを使って作れる献立を3つ提案してください。
                    
                    【参照すべきサイト（このテイストを優先して）】
                    - きょうの料理 (kyounoryouri.jp)
                    - 白ごはん.com (sirogohan.com)
                    - 久原醤油 (kubara.jp)
                    - 山本ゆりさんブログ (ameblo.jp/syunkon)
                    - オレンジページ (orangepage.net)
                    - 朝日放送 おかずのクッキング (asahi.co.jp/daidokoro)

                    【出力項目】
                    1. 料理名（目を引く名前で）
                    2. おおよそのカロリー（1人前あたり）
                    3. Google検索リンク（形式: https://www.google.com/search?q=site:[ドメイン]+[料理名]）
                    4. 山本ゆりさん風の「時短ポイント」や、白ごはん.com風の「丁寧なコツ」を一言

                    親しみやすく、かつプロらしいアドバイスをお願いします。
                    """
                    
                    # AIによる生成
                    response = model.generate_content([prompt, image])
                    
                    st.success("✨ 献立が完成しました！")
                    st.markdown("---")
                    st.markdown(response.text)

            except Exception as e:
                # エラーメッセージを親切に表示
                error_str = str(e)
                if "404" in error_str or "not_found" in error_str:
                    st.error(f"⚠️ **モデル名エラー**: '{model_name}' が見つかりません。最新の名称に更新が必要です。")
                elif "403" in error_str:
                    st.error("🔑 **APIキー無効**: APIキーが正しくないか、権限がありません。")
                elif "429" in error_str:
                    st.error("⏳ **利用制限**: 無料枠の上限です。少し時間を置いて試してください。")
                else:
                    st.error(f"❌ **エラーが発生しました**: \n{error_str}")

else:
    st.info("💡 まずは左のメニューにAPIキーを入れ、冷蔵庫の写真をアップしてね。")

# --- フッター ---
st.markdown("---")
st.caption("Produced by Gemini 3.1 Pro Assistant | 2026")
