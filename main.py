# main.py
import streamlit as st
from load import update_lotto_db
import os

lotto_db = update_lotto_db()

# 세션 상태 초기화
if "selected" not in st.session_state:
    st.session_state.selected = []

st.set_page_config(page_title="로또 당첨 확인기", page_icon="four_leaf_clover", layout="centered")

# CSS - 선택된 버튼 빨간색 + 예쁜 디자인
st.markdown("""
<style>
    .big-title {font-size: 3.5rem; font-weight: bold; text-align: center; color: gold; margin: 20px 0; text-shadow: 3px 3px 10px black;}
    .subtitle {text-align: center; font-size: 1.5rem; color: #fff; margin-bottom: 30px;}
    .number-grid {display: grid; grid-template-columns: repeat(9, 1fr); gap: 12px; margin: 30px 0;}
    .stButton>button {
        width: 70px; height: 70px; font-size: 24px; font-weight: bold;
        border-radius: 15px; border: none; box-shadow: 3px 3px 10px rgba(0,0,0,0.5);
    }
    .selected-btn {
        background: linear-gradient(45deg, #ff0066, #ff4444) !important;
        color: white !important;
        transform: scale(1.1);
        box-shadow: 0 0 20px gold !important;
    }
    .main-bg {background: linear-gradient(135deg, #667eea, #764ba2); padding: 40px; border-radius: 20px; min-height: 100vh;}
    .win {background: rgba(0,255,0,0.2); padding: 20px; border-radius: 15px; margin: 10px 0; border: 2px solid gold;}
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-bg">', unsafe_allow_html=True)
st.markdown('<h1 class="big-title">로또 당첨 확인기</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">버튼 클릭 → 6개 선택하면 자동 확인!</p>', unsafe_allow_html=True)

# 번호 선택 그리드
st.markdown("### 번호 선택 (클릭해서 선택/해제)")
grid = st.container()
with grid:
    cols = st.columns(9)
    for i in range(1, 46):
        col_idx = (i - 1) % 9
        is_selected = i in st.session_state.selected
        btn_label = f"**{i}**" if is_selected else str(i)
        if cols[col_idx].button(btn_label, key=f"num_{i}", 
                                help=f"{i}번 {'해제' if is_selected else '선택'}"):
            if is_selected:
                st.session_state.selected.remove(i)
            elif len(st.session_state.selected) < 6:
                st.session_state.selected.append(i)
            # st.rerun() 없이도 자동 갱신됨! (Streamlit의 마법)

# 선택된 번호 표시
selected_sorted = sorted(st.session_state.selected)
if selected_sorted:
    st.markdown(f"<h2 style='color:gold; text-align:center;'>내 번호: {' '.join(map(str, selected_sorted))} ({len(selected_sorted)}/6)</h2>", 
                unsafe_allow_html=True)
    if len(selected_sorted) == 6:
        st.success("6개 완성! 아래에서 결과 확인하세요!")
else:
    st.markdown("<h2 style='color:#ccc; text-align:center;'>아직 선택 안 함 (0/6)</h2>", unsafe_allow_html=True)

# 초기화 버튼
col1, col2, col3 = st.columns(3)
with col2:
    if st.button("번호 초기화", type="secondary", use_container_width=True):
        st.session_state.selected = []
        st.rerun()

# 6개 다 선택하면 자동 확인
if len(st.session_state.selected) == 6:
    my_set = set(st.session_state.selected)
    found = False
    result = f"<h3 style='color:gold;'>내 번호: {' '.join(map(str, selected_sorted))}</h3><hr>"

    for no, info in lotto_db.items():
        match = len(my_set & set(info["numbers"]))
        if match >= 4:
            rank = "1등" if match==6 else "2등" if match==5 and info["bonus"] in my_set else "3등" if match==5 else "4등"
            result += f"<div class='win'><strong>{no}회 ({info['date']}) → {rank} 당첨!!!</strong><br>"
            result += f"당첨번호: {sorted(info['numbers'])} + 보너스 {info['bonus']}</div><hr>"
            found = True

    if found:
        st.success("축하합니다!!! 당첨된 회차가 있어요!!!")
        st.balloons()
    else:
        st.info("4등 이상 당첨된 적 없네요... 다음 기회에!")

    st.markdown(result, unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)
st.caption("Made with ❤️ by 당신 + Grok")
