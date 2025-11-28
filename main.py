import streamlit as st
from load import update_lotto_db

st.set_page_config(page_title="로또", layout="centered")

# ==================== 번호 전달 처리 ====================
query = st.query_params

if "selected" not in st.session_state:
    st.session_state.selected = []

if "pick" in query:
    num = int(query["pick"])
    sel = st.session_state.selected

    if num in sel:
        sel.remove(num)
    elif len(sel) < 6:
        sel.append(num)

    st.session_state.selected = sel

    # 선택 후 URL 정리
    st.query_params.clear()

# ==================== CSS ====================
st.markdown("""
<style>
.grid {
    display: grid;
    grid-template-columns: repeat(9, 1fr);
    gap: 10px;
    margin-top: 20px;
}

@media (max-width: 900px) {
    .grid { grid-template-columns: repeat(5, 1fr); }
}

@media (max-width: 600px) {
    .grid { grid-template-columns: repeat(3, 1fr); }
}

.btn {
    width: 60px;
    height: 60px;
    border-radius: 50%;
    font-size: 20px;
    font-weight: bold;
    border: 3px solid #fff;
    color: #fff;
    cursor: pointer;
}

/* 색상 */
.btn.y { background: #fbc400; }
.btn.b { background: #69c8f2; }
.btn.r { background: #ff7272; }
.btn.g { background: #aaaaaa; }
.btn.l { background: #b0d840; }

</style>
""", unsafe_allow_html=True)

# ==================== 버튼 렌더 ====================
html = '<div class="grid">'

for n in range(1, 46):
    if n <= 10:
        cls = "y"
    elif n <= 20:
        cls = "b"
    elif n <= 30:
        cls = "r"
    elif n <= 40:
        cls = "g"
    else:
        cls = "l"

    html += f"""
    <button class="btn {cls}" onclick="window.location.href='?pick={n}'">
        {n}
    </button>
    """

html += '</div>'

st.markdown(html, unsafe_allow_html=True)

# ==================== 선택 번호 표시 ====================
st.write("선택된 번호:", st.session_state.selected)
