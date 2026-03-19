import streamlit as st
import google.generativeai as genai
from PIL import Image

# --- 設定エリア ---
st.set_page_config(page_title="献立お助けAI", layout="centered")

# サイドバー設定
api_key = st.sidebar.text_input("Gemini API Keyを入力", type="password")

if api_key:
    genai.configure(api_key=api_key)
    # 2026年現在、安定しているモデルを指定
    model = # 使えるモデルの一覧から "flash" という名前が入っている最新のものを探す
try:
    available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
    # 'flash'が含まれるモデルを探し、なければ一番上のモデルを使う
    target_model = next((m for m in available_models if 'flash' in m), available_models[0])
    model = genai.GenerativeModel(target_model)
except Exception:
    # 万が一リスト取得に失敗したら、2.0を信じてセットする
    model = genai.GenerativeModel('models/gemini-2.0-flash')

st.title("🍳 献立お助け＆カロリー計算AI")
st.write("冷蔵庫の写真をアップして、プロのレシピから献立を選びましょう。")

uploaded_file = st.file_uploader("写真をアップロード...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption='アップロードされた画像', use_column_width=True)
    
    submit = st.button("献立を考えてもらう！")

    if submit:
        if not api_key:
            st.error("🔑 左側のサイドバーにAPIキーを入力してください。")
        else:
            with st.spinner('AIが献立を考案中...'):
                try:
                    # AIへの指示
                    prompt = """
                    画像から食材を特定し、献立を3つ提案してください。
                    参考サイト：白ごはん.com, 山本ゆり, きょうの料理, くばら, オレンジページ
                    各提案に「料理名」「概算カロリー」「Google検索リンク」を含めてください。
                    """
                    
                    # AI呼び出し実行
                    response = model.generate_content([prompt, image])
                    
                    st.subheader("💡 AIからの提案")
                    st.markdown(response.text)

                except Exception as e:
                    # --- ここでエラーを親切に解説 ---
                    error_msg = str(e)
                    
                    if "404" in error_msg or "not found" in error_msg.lower():
                        st.error("⚠️ **【モデルが見つかりません】**\nGoogle側でAIモデルの名称が変更された可能性があります。コード内の `gemini-1.5-flash` を最新の名称に更新してください。")
                    elif "403" in error_msg or "API key" in error_msg:
                        st.error("🔑 **【APIキーのエラー】**\n入力されたAPIキーが正しくないか、有効化されていません。Google AI Studioでキーを再確認してください。")
                    elif "quota" in error_msg.lower() or "429" in error_msg:
                        st.error("⏳ **【制限オーバー】**\n無料枠の利用制限に達しました。1分ほど待ってから再度ボタンを押してください。")
                    else:
                        st.error(f"❌ **【予期せぬエラー】**\n原因: {error_msg}\n（このメッセージをAIに伝えると解決が早まります！）")

else:
    st.info("左側のサイドバーにAPIキーを入れ、ここに写真をアップしてください。")

st.markdown("---")
st.caption("※カロリーはAIによる概算です。")
