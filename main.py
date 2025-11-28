# main.py
import streamlit as st
from load import update_lotto_db
import os

lotto_db = update_lotto_db()

# 웹 디자인
st.set_page_config(page_title="로또 당첨 확인기", page_icon="four_leaf_clover", layout="centered")
st.markdown("""
<style>
    .big-title {font-size: 3.5rem; font-weight: bold; text-align: center; color: gold; margin: 20px 0;}
    .subtitle {text-align: center; font-size: 1.5rem; color: #fff; margin-bottom: 30px;}
    .number-grid {display: grid; grid-template-columns: repeat(9, 1fr); gap: 10px; margin: 30px 0;}
    .number-btn {width: 60px; height: 60px; font-size: 20px; font-weight: bold;}
    .selected {background-color: #ff4444 !important; color: white !important;}
    .win {color: #00ff00; font-size: 2rem; font-weight: bold; background: rgba(0,0,0,0.3); padding: 20px; border-radius: 15px;}
    .main-bg {background: linear-gradient(135deg, #667eea, #764ba2); padding: 30px; border-radius: 20px;}
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-bg">', unsafe_allow_html=True)
st.markdown('<h1 class="big-title">로또 당첨 확인기</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">버튼으로 번호 6개 선택 → 자동으로 전체 회차 확인!</p>', unsafe_allow_html=True)

# 선택된 번호 관리
if "selected" not in st.session_state:
    st.session_state.selected = []

# 1~45 번호 버튼 그리드
st.markdown("### 번호 선택 (클릭하세요)")
cols = st.columns(9)
for i in range(1, 46):
    col_idx = (i - 1) % 9
    with cols[col_idx]:
        btn_class = "selected" if i in st.session_state.selected else ""
        if st.button(str(i), key=f"btn_{i}"):
            if i in st.session_state.selected:
                st.session_state.selected.remove(i)
            elif len(st.session_state.selected) < 6:
                st.session_state.selected.append(i)
            st.rerun()

# 선택된 번호 표시 + 초기화
st.markdown("### 선택된 번호")
selected_display = sorted(st.session_state.selected)
if selected_display:
    st.markdown(f"<h2 style='color:gold; text-align:center;'>{' '.join(map(str, selected_display))} ({len(selected_display)}/6)</h2>", unsafe_allow_html=True)
else:
    st.markdown("<h2 style='color:#ccc; text-align:center;'>아직 선택 안 함 (0/6)</h2>", unsafe_allow_html=True)

col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    if st.button("번호 초기화", type="secondary", use_container_width=True):
        st.session_state.selected = []
        st.rerun()

# 6개 다 선택하면 자동 확인
if len(st.session_state.selected) == 6:
    if st.button("당첨 확인하기!!!", type="primary", use_container_width=True):
        my_set = set(st.session_state.selected)
        found = False
        result = f"<h3 style='color:gold;'>내 번호: {' '.join(map(str, selected_display))}</h3><hr>"
        
        for no, info in lotto_db.items():
            win_set = set(info["numbers"])
            match = len(my_set & win_set)
            has_bonus = info["bonus"] in my_set
            
            if match >= 4:  # 4등 이상만 출력
                rank = {6:"1등", 5:"2등" if has_bonus else "3등",4:"4등"}[match]
                result += f"<div class='win'>{no}회 ({info['date']}) → {rank} 당첨!!!</div>"
                result += f"<p>당첨번호: {sorted(info['numbers'])} + 보너스 {info['bonus']}</p><hr>"
                found = True
        
        if found:
            st.success("축하합니다!!! 당첨된 회차가 있어요!!!")
            st.balloons()
        else:
            st.info("4등 이상 당첨된 적 없네요... 다음 기회에!")
        
        st.markdown(result, unsafe_allow_html=True)
else:
    st.info(f"현재 {len(st.session_state.selected)}/6 개 선택됨")

st.markdown('</div>', unsafe_allow_html=True)
st.caption("Made with ❤️ by 당신 + Grok")
