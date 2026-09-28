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

# 첫 번째 그래프 해석 구역
with st.container():
    st.info(
        "💡 **이 그래프로 알 수 있는 것:** 개봉한 흥행 영화 중 가장 비중이 높은 주력 장르와 비주류 장르의 분포를 한눈에 비교해 볼 수 있습니다."
    )

st.markdown("---")

# 2. 장르 및 영화별 총 관객 수 (트리맵)
st.subheader("2. 장르별 영화 분포 및 총 관객 수")

# Plotly 트리맵 생성 (계층: 장르 > 영화명, 크기: 총 관객 수)
fig2 = px.treemap(
    df,
    path=[px.Constant("전체 영화"), "genre", "movieNm"],
    values="total_audi",
    title="장르 및 영화별 총 관객 수 분포",
    custom_data=["movieNm", "total_audi"],
)

# 마우스오버(호버) 시 영화명과 총 관객 수 표시
fig2.update_traces(
    hovertemplate="<b>영화명: %{customdata[0]}</b><br>총 관객 수: %{customdata[1]:,}명<extra></extra>"
)

st.plotly_chart(fig2, use_container_width=True)

# 두 번째 그래프 해석 구역
with st.container():
    st.info(
        "💡 **이 그래프로 알 수 있는 것:** 특정 장르 내에서 흥행을 주도한 대표 영화가 무엇인지, 장르 전체 흥행 규모에서 각 영화가 차지하는 비중을 알 수 있습니다."
    )

st.markdown("---")

# 3. 총 관객 수 분포 (히스토그램)
st.subheader("3. 총 관객 수 분포")

# 히스토그램 생성
fig3 = px.histogram(
    df,
    x="total_audi",
    nbins=20,
    title="총 관객 수 히스토그램",
    labels={"total_audi": "총 관객 수(명)"},
)

fig3.update_layout(yaxis_title="영화 수(편)")
fig3.update_traces(
    hovertemplate="<b>관객 수 구간: %{x}</b><br>영화 수: %{y}편<extra></extra>"
)

st.plotly_chart(fig3, use_container_width=True)

# 최다 관객 영화 계산
max_movie = df.loc[df["total_audi"].idxmax()]
max_movie_title = max_movie["movieNm"]
max_movie_audi = f"{max_movie['total_audi']:,}"

# 세 번째 그래프 해석 구역
with st.container():
    st.info(
        f"💡 **이 그래프로 알 수 있는 것:** 대다수의 영화가 **소규모 관객 구간(하위 구간)**에 밀집되어 있는 롱테일(Long Tail) 형태의 분포를 보입니다. "
        f"가장 많은 관객을 동원한 영화는 **'{max_movie_title}'** ({max_movie_audi}명)입니다."
    )

st.markdown("---")

# 4. 개봉일 스크린 수 vs 총 관객 수 (산점도)
st.subheader("4. 개봉일 스크린 수와 총 관객 수의 관계")

# 산점도 생성 (색상: 장르)
fig4 = px.scatter(
    df,
    x="first_scrn",
    y="total_audi",
    color="genre",
    hover_name="movieNm",
    title="개봉일 스크린 수 vs 총 관객 수",
    labels={
        "first_scrn": "개봉일 스크린 수(개)",
        "total_audi": "총 관객 수(명)",
        "genre": "장르",
    },
)

fig4.update_traces(
    hovertemplate="<b>영화명: %{hovertext}</b><br>개봉일 스크린 수: %{x:,}개<br>총 관객 수: %{y:,}명<extra></extra>"
)

st.plotly_chart(fig4, use_container_width=True)

# 네 번째 그래프 해석 구역
with st.container():
    st.info(
        "💡 **이 그래프로 알 수 있는 것:** 초기 스크린 확보 수(개봉일 스크린 수)가 많을수록 대체로 최종 관객 수가 높아지는 양의 상관관계를 확인해 볼 수 있습니다."
    )
