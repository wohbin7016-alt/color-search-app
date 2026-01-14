import streamlit as st
import pandas as pd

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

        df = df.iloc[:, :3]
        df.columns = ["색상개발일련번호", "승인명", "보관시편"]
        df["시트명"] = sheet_name

        dfs.append(df)

    return pd.concat(dfs, ignore_index=True)

# ===============================
# UI
# ===============================
st.set_page_config(page_title="색상 개발 검색", layout="centered")

st.title("🎨 색상 개발 검색")

query = st.text_input(
    "색상개발 일련번호 / 승인명 일부 검색",
    placeholder="예: YK-12 / WHITE / 070"
)

if st.button("🔄 데이터 새로고침"):
    st.cache_data.clear()
    st.experimental_rerun()

df = load_all_sheets()

# ===============================
# 검색
# ===============================
if query:
    result = df[
        df["색상개발일련번호"].astype(str).str.contains(query, case=False, na=False) |
        df["승인명"].astype(str).str.contains(query, case=False, na=False)
    ]

    st.markdown(f"### 🔍 검색 결과: {len(result)}건")

    if result.empty:
        st.warning("일치하는 데이터가 없습니다.")
    else:
        for _, row in result.iterrows():
            with st.container():
                st.markdown(f"#### {row['승인명']}")
                st.markdown(f"- **색상개발 일련번호:** {row['색상개발일련번호']}")
                st.markdown(f"- **보관시편:** {row['보관시편']}")
                st.markdown(f"- **시트명:** {row['시트명']}")
                st.divider()
