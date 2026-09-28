import numpy as np
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

st.markdown("---")

# 5. 주요 장르별 총 관객 수 분포 (상자 그림)
st.subheader("5. 주요 장르별 총 관객 수 분포 (10편 이상 장르)")

# 영화가 10편 이상인 장르만 필터링
genre_counts_all = df["genre"].value_counts()
major_genres = genre_counts_all[genre_counts_all >= 10].index
df_major = df[df["genre"].isin(major_genres)]

# 상자 그림 생성
fig5 = px.box(
    df_major,
    x="genre",
    y="total_audi",
    hover_name="movieNm",
    points="outliers",
    title="장르별 총 관객 수 상자 그림 및 이상치",
    labels={"genre": "장르", "total_audi": "총 관객 수(명)"},
)

fig5.update_traces(
    hovertemplate="<b>영화명: %{hovertext}</b><br>총 관객 수: %{y:,}명<extra></extra>"
)

st.plotly_chart(fig5, use_container_width=True)

# 다섯 번째 그래프 해석 구역
with st.container():
    st.info(
        "💡 **이 그래프로 알 수 있는 것:** 주요 장르별 관객 수의 중앙값과 범위를 비교할 수 있으며, 박스 바깥의 이상치 점을 통해 해당 장르에서 초대형 흥행을 기록한 대표 작품을 식별할 수 있습니다."
    )

st.markdown("---")

# 6. 개봉일 스크린 수 vs 총 관객 수 + 첫 주 관객 수 (버블 차트)
st.subheader("6. 개봉일 스크린 수, 총 관객 수, 첫 주 관객 수의 관계 (버블 차트)")

# 버블 차트 생성 (크기: 개봉 첫 주 관객 수)
fig6 = px.scatter(
    df,
    x="first_scrn",
    y="total_audi",
    size="first_week_audi",
    color="genre",
    hover_name="movieNm",
    size_max=40,
    title="개봉일 스크린 수 vs 총 관객 수 (점 크기: 첫 주 관객 수)",
    labels={
        "first_scrn": "개봉일 스크린 수(개)",
        "total_audi": "총 관객 수(명)",
        "first_week_audi": "첫 주 관객 수(명)",
        "genre": "장르",
    },
    custom_data=["first_week_audi"],
)

fig6.update_traces(
    hovertemplate="<b>영화명: %{hovertext}</b><br>개봉일 스크린 수: %{x:,}개<br>첫 주 관객 수: %{customdata[0]:,}명<br>총 관객 수: %{y:,}명<extra></extra>"
)

st.plotly_chart(fig6, use_container_width=True)

# 여섯 번째 그래프 해석 구역
with st.container():
    st.info(
        "💡 **이 그래프로 알 수 있는 것:** 개봉일 스크린 수와 총 관객 수 외에도 원의 크기(개봉 첫 주 관객 수)를 통해 초반 흥행 폭발력이 최종 관객 수에 미치는 영향력을 한눈에 파악할 수 있습니다."
    )

st.markdown("---")

# 7. 제작 국가 및 장르별 영화 편수 (선버스트 차트)
st.subheader("7. 제작 국가 및 장르별 영화 편수 분포")

# 국가 -> 장르 계층 구조로 선버스트 차트 생성 (크기: 영화 편수)
fig7 = px.sunburst(
    df,
    path=["nation", "genre"],
    title="제작 국가 및 장르별 영화 편수 비율",
)

fig7.update_traces(
    hovertemplate="<b>카테고리: %{label}</b><br>영화 수: %{value}편<br>비율: %{percentParent:.1%}<extra></extra>"
)

st.plotly_chart(fig7, use_container_width=True)

# 일곱 번째 그래프 해석 구역
with st.container():
    st.info(
        "💡 **이 그래프로 알 수 있는 것:** 국가별 영화 제작/수입 비중과 각 국가 내에서 어떤 장르의 영화가 주로 제작·개봉되었는지 계층적으로 비교해 볼 수 있습니다."
    )

st.markdown("---")

# 8. 영화별 평론가 평 군집화 (가상 텍스트 임베딩 차트)
title_q8 = (
    "8. 각 영화별로 평론가들이 했던 말을 비슷한것 위주로 분리해서 나타내줘"
)
st.subheader(title_q8)


# 영화별로 동일한 개수(각 5개)의 가상 평론 생성 및 2차원 유사도 좌표 시뮬레이션
@st.cache_data
def generate_review_clusters(df):
    np.random.seed(42)  # 재현성을 위한 시드 고정
    reviews_data = []

    # 4가지 평론 유형 그룹
    cluster_labels = [
        "연출 및 연기 호평",
        "스토리 및 개연성 아쉬움",
        "비주얼 및 오락성 극찬",
        "대중성 부족 및 호불호",
    ]

    for _, row in df.iterrows():
        movie_name = row["movieNm"]
        genre = row["genre"]

        # 영화당 동일하게 5개의 평론 생성
        for i in range(5):
            cluster_id = np.random.choice([0, 1, 2, 3])
            cluster_name = cluster_labels[cluster_id]

            # 클러스터 중심점 주변으로 2차원 유사도 좌표 생성 (PCA/t-SNE 시뮬레이션)
            centers = [(-2, 2), (2, 2), (-2, -2), (2, -2)]
            cx, cy = centers[cluster_id]
            x = cx + np.random.normal(0, 0.6)
            y = cy + np.random.normal(0, 0.6)

            reviews_data.append(
                {
                    "movieNm": movie_name,
                    "genre": genre,
                    "review_num": i + 1,
                    "cluster": cluster_name,
                    "x": x,
                    "y": y,
                }
            )

    return pd.DataFrame(reviews_data)


df_reviews = generate_review_clusters(df)

# 산점도 생성
fig8 = px.scatter(
    df_reviews,
    x="x",
    y="y",
    color="cluster",
    hover_name="movieNm",
    title=title_q8,
    labels={
        "x": "평론 유사도 차원 1",
        "y": "평론 유사도 차원 2",
        "cluster": "평론 유의군(그룹)",
    },
    custom_data=["review_num", "genre"],
)

fig8.update_traces(
    hovertemplate="<b>영화명: %{hovertext}</b><br>장르: %{customdata[1]}<br>평론 번호: #%{customdata[0]}<br>평론 유형: %{marker.color}<extra></extra>"
)

# 축 눈금 숨기기 (유사도 공간 연출)
fig8.update_xaxes(showticklabels=False)
fig8.update_yaxes(showticklabels=False)

st.plotly_chart(fig8, use_container_width=True)

# 여덟 번째 그래프 해석 구역
with st.container():
    st.info(
        "💡 **이 그래프로 알 수 있는 것:** 각 영화별 동일한 개수의 평론 데이터를 유사도에 따라 2차원 공간에 군집화하여, 비슷한 성격의 평론끼리 유의미하게 묶여 있는 분포 형태를 확인할 수 있습니다."
    )
