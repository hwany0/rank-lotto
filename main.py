# main.py
import streamlit as st
from load import update_lotto_db
import os

# ===================== 기본 설정 =====================
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


# ===================== URL 버튼 선택 처리 =====================
params = st.query_params
if "num" in params:
    num = int(params["num"])
    if num in st.session_state.selected:
        st.session_state.selected.remove(num)
    elif len(st.session_state.selected) < 6:
        st.session_state.selected.append(num)

    st.query_params.clear()
    st.rerun()


# ===================== 번호 색상 CSS 자동 생성 =====================
colors_css = "\n".join([
    f".num-button.num-{i} {{ background: {color} !important; }}"
    for i, color in [
        *[(i, "#fbc400") for i in range(1, 11)],   # 노랑
        *[(i, "#69c8f2") for i in range(11, 21)],  # 파랑
        *[(i, "#ff7272") for i in range(21, 31)],  # 빨강
        *[(i, "#aaaaaa") for i in range(31, 41)],  # 회색
        *[(i, "#b0d840") for i in range(41, 46)],  # 초록
    ]
])


# ===================== CSS =====================
st.markdown(
    f"""
<style>
    body {{
        background: linear-gradient(to bottom, #003087, #001f5a);
        color: white;
        font-family: 'Malgun Gothic', sans-serif;
    }}

    .title {{
        font-size: 3rem;
        color: #ffd700;
        text-align: center;
        margin: 20px 0;
        text-shadow: 3px 3px 12px #000;
    }}

    .ball {{
        width: 60px; height: 60px;
        border-radius: 50%;
        display: inline-flex; justify-content: center; align-items: center;
        margin: 5px;
        font-weight: bold; font-size: 24px;
        border: 3px solid white;
    }}

    .ball-1 {{ background:#fbc400; }}
    .ball-2 {{ background:#69c8f2; }}
    .ball-3 {{ background:#ff7272; }}
    .ball-4 {{ background:#aaaaaa; }}
    .ball-5 {{ background:#b0d840; }}

    /* 번호 버튼 GRID 반응형 */
    .number-grid {{
        display: grid;
        grid-template-columns: repeat(9, 1fr);
        gap: 10px;
        margin-top: 20px;
        justify-items: center;
    }}

    @media (max-width: 900px) {{
        .number-grid {{
            grid-template-columns: repeat(5, 1fr);
        }}
    }}

    @media (max-width: 500px) {{
        .number-grid {{
            grid-template-columns: repeat(3, 1fr);
        }}
    }}

    .num-button {{
        width: 62px;
        height: 62px;
        border-radius: 50%;
        font-size: 20px;
        font-weight: bold;
        border: 3px solid #ffffffaa;
        color: white;
        cursor: pointer;
    }}

    /* 자동 생성된 번호별 색상 */
    {colors_css}

</style>
""",
    unsafe_allow_html=True
)


# ===================== UI =====================
st.markdown('<h1 class="title">로또 6/45 당첨 확인기</h1>', unsafe_allow_html=True)

# 초기화
if st.button("번호 초기화"):
    st.session_state.selected = []
    st.rerun()

# 선택 번호 표시
if st.session_state.selected:
    display = "".join(
        f"<span class='ball ball-{(n-1)//10 + 1}'>{n}</span>"
        for n in sorted(st.session_state.selected)
    )
    st.markdown(f"<div style='text-align:center'>{display}</div>", unsafe_allow_html=True)
else:
    st.markdown("<p style='text-align:center'>6개의 번호를 선택하세요.</p>", unsafe_allow_html=True)


# ===================== 번호 선택 버튼 =====================
button_html = ""
for num in range(1, 46):
    button_html += f"""
        <form method="get" style="display:inline;">
            <input type="hidden" name="num" value="{num}">
            <button class="num-button num-{num}" type="submit">{num}</button>
        </form>
    """

st.markdown(f'<div class="number-grid">{button_html}</div>', unsafe_allow_html=True)


# ===================== 결과 =====================
if len(st.session_state.selected) == 6:
    my_set = set(st.session_state.selected)
    result_html = ""
    found = False

    for no, info in lotto_db.items():
        win_set = set(info["numbers"])
        match = len(my_set & win_set)

        if match >= 4:
            if match == 6:
                rank = "1등"
            elif match == 5 and info["bonus"] in my_set:
                rank = "2등"
            elif match == 5:
                rank = "3등"
            else:
                rank = "4등"

            win_balls = "".join(
                f"<span class='ball ball-{(n-1)//10 + 1}'>{n}</span>"
                for n in info["numbers"]
            )
            result_html += f"""
            <div style="text-align:center; background:rgba(255,255,255,0.15); 
                        padding:20px; margin:20px; border-radius:15px;">
                <h3 style='color:gold'>제 {no}회 → {rank} 당첨!</h3>
                {win_balls}
                 + <span class='ball ball-5'>{info['bonus']}</span>
                <br><small>{info['date']}</small>
            </div>
            """
            found = True

    if found:
        st.success("🎉 축하합니다! 당첨입니다!")
        st.balloons()
    else:
        st.info("4등 이상 당첨 없음. 다음 기회에!")

    st.markdown(result_html, unsafe_allow_html=True)
