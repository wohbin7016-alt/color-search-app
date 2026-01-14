import streamlit as st
import pandas as pd
from textwrap import dedent

# ===============================
# Google Sheets 설정
# ===============================
SHEET_ID = "1CLdBGUUp8e5Rgyx-1p6xbMLvOQmq29MTLq31XEOMH-Y"

SHEETS = {
    "Sheet-01": "940998157",
    "Sheet-02": "1228023498",
    "Sheet-03": "1443676891",
    "Sheet-04": "734739962",
    "Sheet-05": "1918161246",
    "Sheet-06": "1042781439",
    "Sheet-07": "701385994",
    "Sheet-08": "1840483998",
    "Sheet-09": "1143728983",
    "Sheet-10": "1714955575",
    "Sheet-11": "1703228436",
    "Sheet-12": "1844578840",
    "Sheet-13": "1724424480",
    "Sheet-14": "324496210",
    "Sheet-15": "2102547878",
    "Sheet-16": "449587596",
}

# ===============================
# 데이터 로딩
# ===============================
@st.cache_data
def load_all_sheets():
    dfs = []

    for sheet_name, gid in SHEETS.items():
        url = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv&gid={gid}"
        df = pd.read_csv(url)

        # A, B, C 열만 사용
        df = df.iloc[:, :3]
        df.columns = ["색상개발일련번호", "승인명", "보관시편"]

        df["시트명"] = sheet_name
        dfs.append(df)

    return pd.concat(dfs, ignore_index=True)

# ===============================
# UI 기본 설정
# ===============================
st.set_page_config(
    page_title="색상 개발 검색",
    layout="centered"
)

st.title("🎨 색상 개발 검색")

query = st.text_input(
    "색상개발 일련번호 / 승인명 일부만 입력해도 검색됩니다",
    placeholder="예: YK-12 / WHITE / 070"
)

col1, col2 = st.columns([1, 5])
with col1:
    if st.button("🔄 새로고침"):
        st.cache_data.clear()
        st.experimental_rerun()

df = load_all_sheets()

# ===============================
# 검색 로직 (부분검색 통합)
# ===============================
if query:
    result = df[
        df["색상개발일련번호"].astype(str).str.contains(query, case=False, na=False) |
        df["승인명"].astype(str).str.contains(query, case=False, na=False)
    ]

    st.write(f"🔍 검색 결과: {len(result)}건")

    if result.empty:
        st.warning("일치하는 데이터가 없습니다.")
    else:
        for _, row in result.iterrows():
            card_html = dedent(f"""
            <div style="
                border:1px solid #ddd;
                border-radius:10px;
                padding:14px 16px;
                margin-bottom:14px;
                background-color:#ffffff;
                box-sizing:border-box;
                width:100%;
            ">
                <div style="
                    font-size:18px;
                    font-weight:600;
                    margin-bottom:8px;
                    word-break:break-word;
                ">
                    {row['승인명']}
                </div>

                <div style="
                    font-size:14px;
                    margin-bottom:4px;
                    word-break:break-word;
                ">
                    <b>색상개발 일련번호:</b> {row['색상개발일련번호']}
                </div>

                <div style="
                    font-size:14px;
                    margin-bottom:4px;
                    word-break:break-word;
                ">
                    <b>보관시편:</b> {row['보관시편']}
                </div>

                <div style="
                    font-size:12px;
                    color:#666;
                    word-break:break-word;
                ">
                    시트명: {row['시트명']}
                </div>
            </div>
            """)
            st.markdown(card_html, unsafe_allow_html=True)
