import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
import koreanize_matplotlib

# Streamlit 페이지의 아이콘이 왕관 모양에서 자동차 모양으로 바뀜 (<head> 태그에 들어가므로, 맨 위에 온다.)
st.set_page_config(
    page_title="Likelion AI School 자동차 연비 App",
    page_icon="🚗",
    layout="wide",
)

# 메인 페이지, 사이드 페이지 title 
st.markdown("# 자동차 연비 🚗")
st.sidebar.markdown("# 자동차 연비 🚗")

url = "https://raw.githubusercontent.com/mwaskom/seaborn-data/master/mpg.csv"
# data = pd.read_csv(url)

# uber.py를 참고하여 캐시에서 데이터를 불러 올 수 있도록 설정
@st.cache
def load_data(url):
    data = pd.read_csv(url)
    return data

data_load_state = st.text('Loading data...')
data = load_data(url)
data_load_state.text("Done! (using st.cache)")


# 연도 선택 기능 (최근연도가 맨 위에 오도록 reversed 로 정렬)
st.sidebar.header('User Input Features')
selected_year = st.sidebar.selectbox('Year',
   list(reversed(range(data.model_year.min(),data.model_year.max())))
   )

if selected_year > 0 :
   data = data[data.model_year == selected_year]


# 검색 기능
# Sidebar - origin
sorted_unique_origin = sorted(data.origin.unique())
selected_origin = st.sidebar.multiselect('origin', sorted_unique_origin, sorted_unique_origin)

if len(selected_origin) > 0:
   data = data[data.origin.isin(selected_origin)]
# data

st.dataframe(data)

# Streamlit 에서 제공하는 기능으로 그래프 그리기
st.line_chart(data["mpg"])

st.bar_chart(data["mpg"])

# matplotlib 으로 Seaborn 그래프 그리기
fig, ax = plt.subplots(figsize=(10,3))
# sns.barplot(data=data, x="origin", y="mpg").set_title("origin 별 자동차 연비")
# st.pyplot(fig)

sns.countplot(data=data, x="origin").set_title("지역별 자동차 연비 데이터 수")
st.pyplot(fig)


# plotly 로 그래프 그리기
pxh = px.histogram(data, x="origin", title="지역별 자동차 연비 데이터 수")
st.plotly_chart(pxh)

pxa = px.histogram(data, x= "origin", facet_col="cylinders", title="지역별 자동자 실린더 수") 
st.plotly_chart(pxa)



