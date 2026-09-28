import pandas as pd
import plotly.express as px
import streamlit as st

# 페이지 기본 설정
st.set_page_config(page_title="영화 데이터 그래프 도감 2 - 분포와 관계", layout="wide")

st.title("영화 데이터 그래프 도감 2 - 분포와 관계")


# 데이터 로드 및 전처리
@st.cache_data
def load_data():
    url = "https://raw.githubusercontent.com/greatsong/modudata/main/data/kobis_movies.csv"
    df = pd.read_csv(url)

    # 장르 전처리: 세로막대 기호(|)로 구분된 경우 첫 번째 장르만 추출
    df["genre"] = df["genre"].astype(str).apply(lambda x: x.split("|")[0].strip())

    return df


df = load_data()

st.markdown("---")

# 1. 장르별 영화 편수 (도넛 그래프)
st.subheader("1. 장르별 영화 편수 분포")

# 장르별 편수 집계
genre_counts = df["genre"].value_counts().reset_index()
genre_counts.columns = ["genre", "count"]

# Plotly 도넛 차트 생성
fig1 = px.pie(
    genre_counts,
    values="count",
    names="genre",
    hole=0.4,
    title="장르별 영화 편수 비율",
)

# 마우스오버(호버) 시 편수(value)와 비율(percent) 표시
fig1.update_traces(
    textinfo="percent+label",
    hovertemplate="<b>장르: %{label}</b><br>편수: %{value}편<br>비율: %{percent}",
)

st.plotly_chart(fig1, use_container_width=True)

# 그래프 해석 가이드 구역
with st.container():
    st.info(
        "💡 **이 그래프로 알 수 있는 것:** 개봉한 흥행 영화 중 가장 비중이 높은 주력 장르와 비주류 장르의 분포를 한눈에 비교해 볼 수 있습니다."
    )
