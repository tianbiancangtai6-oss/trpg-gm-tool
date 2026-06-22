import streamlit as st
import random  # ダイス（ランダムな数値）を振るために必要なPythonの道具

# アプリのタイトル
st.title("🎲 TRPG GMサポート＆セッションツール")

# ----------------------------------------------------
# 1. ログとステータスの保存処理（初期化）
# ----------------------------------------------------
if "chat_log" not in st.session_state:
    st.session_state.chat_log = []

# 各キャラクターのHPやSAN値を保存する仕組み
if "characters_status" not in st.session_state:
    st.session_state.characters_status = {}


# ----------------------------------------------------
# 2. シナリオ作成・確認エリア（サイドバー）
# ----------------------------------------------------
st.sidebar.header("📝 シナリオ管理データ")
npc_info = st.sidebar.text_area("NPC一覧・設定", "・酒場の店主\n・謎の魔術師")
clues_info = st.sidebar.text_area("手がかり・秘密", "・地下室の古い日記")

st.sidebar.markdown("---")
st.sidebar.header("👥 セッション設定")
player_count = st.sidebar.number_input("プレイヤーキャラクター（PC）の人数", min_value=1, max_value=10, value=3, step=1)


# ----------------------------------------------------
# 3. メイン画面：ダイスボット（共通機能）
# ----------------------------------------------------
st.subheader("🎲 クイック・ダイス")
col1, col2, col3 = st.columns(3)

with col1:
    if st.button("🎲 1D100 を振る（クトゥルフ等）"):
        roll = random.randint(1, 100)
        st.session_state.chat_log.append(f"【ダイス】: 1D100 ➔ 🎲 **{roll}**")
        st.rerun()

with col2:
    if st.button("🎲 2D6 を振る（ソードワールド等）"):
        die1 = random.randint(1, 6)
        die2 = random.randint(1, 6)
        total = die1 + die2
        st.session_state.chat_log.append(f"【ダイス】: 2D6 ➔ 🎲 **{total}** ({die1}, {die2})")
        st.rerun()

with col3:
    if st.button("🎲 1D6 を振る"):
        roll = random.randint(1, 6)
        st.session_state.chat_log.append(f"【ダイス】: 1D6 ➔ 🎲 **{roll}**")
        st.rerun()


# ----------------------------------------------------
# 4. メイン画面：キャラクター行動入力＆ステータス管理
# ----------------------------------------------------
st.write("---")
st.subheader("💬 キャラクター管理（1人4役）")

# タブの作成（PC人数分 ＋ GM）
tab_names = [f"👤 PC {i+1}" for i in range(player_count)] + ["👁️ GM"]
tabs = st.tabs(tab_names)

for index, tab in enumerate(tabs):
    with tab:
        if index == player_count:
            # --- GM用の画面 ---
            st.write("**ゲームマスター（GM）**として描写")
            msg_gm = st.text_input("ナレーションやNPCの発言...", key="input_gm")
            if st.button("GMとして送信", key="btn_gm"):
                if msg_gm:
                    st.session_state.chat_log.append(f"【GM】: {msg_gm}")
                    st.rerun()
        else:
            # --- 各PC用の画面 ---
            pc_num = index + 1
            pc_key = f"PC_{pc_num}"
            
            # 各PCのステータス初期値がなければ作成（HP初期値:10, SAN初期値:50）
            if pc_key not in st.session_state.characters_status:
                st.session_state.characters_status[pc_key] = {"hp": 10, "san": 50}
            
            # 【新機能】ステータス表示と増減ボタン
            status = st.session_state.characters_status[pc_key]
            
            # 横並びでHPとSAN値を表示・操作できるようにする
            stat_col1, stat_col2 = st.columns(2)
            with stat_col1:
                status["hp"] = st.number_input(f"PC {pc_num} の HP", min_value=0, max_value=100, value=status["hp"], key=f"hp_{pc_key}")
            with stat_col2:
                status["san"] = st.number_input(f"PC {pc_num} の SAN値", min_value=0, max_value=100, value=status["san"], key=f"san_{pc_key}")
            
            st.caption(f"現在の状態 ➔ ❤️ HP: {status['hp']} | 🧠 SAN: {status['san']}")
            
            # 行動入力
            msg_pc = st.text_input(f"PC {pc_num} の発言や行動...", key=f"input_{pc_key}")
            
            # 送信ボタンと、このキャラ専用のダイスボタン
            btn_col1, btn_col2 = st.columns([1, 2])
            with btn_col1:
                if st.button(f"PC {pc_num} として送信", key=f"btn_{pc_key}"):
                    if msg_pc:
                        st.session_state.chat_log.append(f"【PC {pc_num}】: {msg_pc} (HP:{status['hp']}/SAN:{status['san']})")
                        st.rerun()
            with btn_col2:
                if st.button(f"🎲 PC {pc_num} が 1D100を振る", key=f"dice_{pc_key}"):
                    roll = random.randint(1, 100)
                    # SANチェックなどの判定用に、現在のSAN値も一緒にログに出す
                    st.session_state.chat_log.append(f"【PC {pc_num}】ダイス ➔ 🎲 **{roll}** (現在のSAN値:{status['san']})")
                    st.rerun()


# ----------------------------------------------------
# 5. セッションログ表示エリア
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
