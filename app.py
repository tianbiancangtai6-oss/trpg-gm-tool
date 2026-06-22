import streamlit as st

# アプリのタイトル
st.title("🎲 TRPG GMサポート＆セッションツール")

# ----------------------------------------------------
# 1. シナリオ作成・確認エリア（サイドバー）
# ----------------------------------------------------
st.sidebar.header("📝 シナリオ管理データ")

npc_info = st.sidebar.text_area("NPC一覧・設定", "・酒場の店主（情報屋）\n・謎の魔術師")
clues_info = st.sidebar.text_area("手がかり・秘密", "・地下室の古い日記\n・深夜2時の鐘の音")

st.sidebar.markdown("---")
st.sidebar.header("👥 セッション設定")

# 【ここがポイント！】参加人数をスライダー、または数値入力で自由に選択できるようにします
# 今回は 1人〜6人 まで選べるように設定（初期値は 4人）
player_count = st.sidebar.number_input("プレイヤーキャラクター（PC）の人数", min_value=1, max_value=10, value=4, step=1)


# ----------------------------------------------------
# 2. ログの保存処理
# ----------------------------------------------------
if "chat_log" not in st.session_state:
    st.session_state.chat_log = []


# ----------------------------------------------------
# 3. メイン画面：選択された人数に合わせてタブを自動生成
# ----------------------------------------------------
st.subheader("💬 キャラクター行動入力")

# 選択された人数分の「PCタブ」＋「GM用のタブ」をリストとして自動で作ります
tab_names = [f"👤 PC {i+1}" for i in range(player_count)] + ["👁️ GM（ゲームマスター）"]
tabs = st.tabs(tab_names)

# ループ処理を使って、それぞれのタブの中身を自動で生成します
for index, tab in enumerate(tabs):
    with tab:
        # 最後のタブかどうかで、GMかPCかを判定します
        if index == player_count:
            # GM用の入力欄
            st.write("**ゲームマスター（GM）**として状況を描写します")
            msg_gm = st.text_input("ナレーションやNPCの発言を入力...", key="input_gm")
            if st.button("GMとして送信", key="btn_gm"):
                if msg_gm:
                    st.session_state.chat_log.append(f"【GM】: {msg_gm}")
                    st.rerun()
        else:
            # 各PC用の入力欄（インデックスは0から始まるので、表示上は +1 します）
            pc_num = index + 1
            st.write(f"**PC {pc_num}** として行動・発言を入力します")
            msg_pc = st.text_input(f"PC {pc_num} の発言やダイス結果...", key=f"input_pc_{pc_num}")
            if st.button(f"PC {pc_num} として送信", key=f"btn_pc_{pc_num}"):
                if msg_pc:
                    st.session_state.chat_log.append(f"【PC {pc_num}】: {msg_pc}")
                    st.rerun()


# ----------------------------------------------------
# 4. セッションログ表示エリア
# ----------------------------------------------------
st.write("---")
st.subheader("📜 セッションログ（タイムライン）")

if st.session_state.chat_log:
    for log in reversed(st.session_state.chat_log):
        st.write(log)
else:
    st.info("ここにセッションの記録が表示されます。上のタブから発言を入力してください。")

# ログのリセットボタン
if st.sidebar.button("ログをクリア"):
    st.session_state.chat_log = []
    st.rerun()
