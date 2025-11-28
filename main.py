# main.py
import streamlit as st
from load import update_lotto_db
import os

# ==================== 기본 설정 ====================
st.set_page_config(
    page_title="로또 6/45 당첨 확인기",
    page_icon="🍀",
    layout="centered",
)

@st.cache_data(ttl=86400)
def get_db():
    return update_lotto_db()

lotto_db = get_db()

if "selected" not in st.session_state:
    st.session_state.selected = []


# ==================== CSS (Grid + 버튼 스타일) ====================
st.markdown("""
<style>
    body {
        background: linear-gradient(to bottom, #003087, #001f5a);
        color: white;
        font-family: 'Malgun Gothic', sans-serif;
    }

    .title {
        font-size: 3rem;
        color: #ffd700;
        text-align: center;
        margin: 20px 0;
        text-shadow: 3px 3px 12px #000;
    }

    .grid-container {
        display: grid;
        grid-template-columns: repeat(9, 1fr);
        gap: 10px;
        justify-items: center;
        margin-top: 20px;
    }

    @media (max-width: 900px) {
        .grid-container {
            grid-template-columns: repeat(5, 1fr);
        }
    }

    @media (max-width: 500px) {
        .grid-container {
            grid-template-columns: repeat(3, 1fr);
        }
    }

    /* Streamlit 버튼 기본 스타일 제거 */
    div.stButton > button {
        width: 60px !important;
        height: 60px !important;
        border-radius: 50% !important;
        font-size: 20px !important;
        font-weight: bold !important;
        color: white !important;
        border: 3px solid rgba(255,255,255,0.5) !important;
        box-shadow: 0 4px 10px rgba(0,0,0,0.5) !important;
    }

    /* 숫자별 실제 로또 색상 */
    %s

    .ball {
        width: 60px; height: 60px;
        border-radius: 50%;
        display: inline-flex;
        justify-content: center;
        align-items: center;
        margin: 5px;
        font-weight: bold;
        font-size: 24px;
        border: 3px solid white;
    }
    .ball-1 { background: #fbc400; }
    .ball-2 { background: #69c8f2; }
    .ball-3 { background: #ff7272; }
    .ball-4 { background: #aaaaaa; }
    .ball-5 { background: #b0d840; }

</style>
""" % "\n".join(
    [f"div.stButton:nth-child({i}) > button {{ background:{color} !important; }}"
     for i, color in [
         *[(i, "#fbc400") for i in range(1, 11)],
         *[(i, "#69c8f2") for i in range(11, 21)],
         *[(i, "#ff7272") for i in range(21, 31)],
         *[(i, "#aaaaaa") for i in range(31, 41)],
         *[(i, "#b0d840") for i in range(41, 46)],
     ]]
),
    unsafe_allow_html=True
)


# ==================== UI ====================
st.markdown('<h1 class="title">로또 6/45 당첨 확인기</h1>', unsafe_allow_html=True)

if st.button("번호 초기화"):
    st.session_state.selected = []
    st.rerun()

# 선택 번호 표시
if st.session_state.selected:
    html = "".join(
        f"<span class='ball ball-{(n-1)//10 + 1}'>{n}</span>"
        for n in sorted(st.session_state.selected)
    )
    st.markdown(f"<div style='text-align:center'>{html}</div>", unsafe_allow_html=True)
else:
    st.markdown("<p style='text-align:center'>6개의 번호를 선택하세요.</p>", unsafe_allow_html=True)


# ==================== 번호 버튼 (Streamlit 버튼 + CSS Grid) ====================
st.markdown('<div class="grid-container">', unsafe_allow_html=True)

for num in range(1, 46):
    if st.button(str(num), key=f"num{num}"):
        if num in st.session_state.selected:
            st.session_state.selected.remove(num)
        elif len(st.session_state.selected) < 6:
            st.session_state.selected.append(num)
        st.rerun()

st.markdown('</div>', unsafe_allow_html=True)


# ==================== 결과 ====================
if len(st.session_state.selected) == 6:
    my_set = set(st.session_state.selected)
    results = ""
    found = False

    for no, info in lotto_db.items():
        match = len(my_set & set(info["numbers"]))

        if match >= 4:
            found = True

            if match == 6:
                rank = "1등"
            elif match == 5 and info["bonus"] in my_set:
                rank = "2등"
            elif match == 5:
                rank = "3등"
            else:
                rank = "4등"

            balls = "".join(
                f"<span class='ball ball-{(n-1)//10 + 1}'>{n}</span>"
                for n in info["numbers"]
            )

            results += f"""
            <div style="text-align:center; background:rgba(255,255,255,0.15); 
                        padding:20px; margin:20px; border-radius:15px;">
                <h3 style="color:gold">제 {no}회 → {rank} 당첨!</h3>
                {balls} + <span class='ball ball-5'>{info['bonus']}</span>
                <br><small>{info['date']}</small>
            </div>
            """

    if found:
        st.success("🎉 축하합니다! 당첨입니다!")
        st.balloons()
    else:
        st.info("4등 이상 당첨 없음. 다음 기회에!")

    st.markdown(results, unsafe_allow_html=True)
