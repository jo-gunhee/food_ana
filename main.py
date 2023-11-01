# main.py

import streamlit as st
from tab1 import tab1_content
from tab2 import tab2_content
from tab3 import tab3_content
from tab4 import tab4_content




# 타이틀 설정
st.title("식품안전나라 데이터 분석")

# 탭 메뉴 설정
# tabs = ["식품안전 나라 데이터", "분석 페이지", "해외 데이터", "연도별 추이 분석"]
tabs = ["식품안전 나라 데이터", "분석 페이지"]

selected_tab = st.radio("메뉴", tabs)


# 선택된 탭에 따라 해당 모듈의 내용을 표시
if selected_tab == "식품안전 나라 데이터":
    tab1_content()

elif selected_tab == "해외 데이터":
    tab2_content()

elif selected_tab == "분석 페이지":
    tab3_content()

elif selected_tab == "연도별 추이 분석":
    tab4_content()

