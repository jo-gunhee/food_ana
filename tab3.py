# tab3.py

import streamlit as st
import datetime
from tab1 import show_xlsx
import pandas as pd
import matplotlib.pyplot as plt
from tab1 import *


global df_tab1, df_tab2, df_tab3, df_tab4, file_name

def tab3_content():

    try:
        st.markdown("""---""")
        option = show_xlsx("분석할 데이터 선택")
        # option = "★231031.xlsx"
        if option is not None:
            file_name = "./result_xlsx/"+option

            tab1, tab2, tab3, tab4 = st.tabs(["전체", "품목수 월별", "카테고리별", "원료별"])
            dfs = pd.read_excel(file_name, sheet_name=["Sheet1", "2023년 품목수_월별", "2023년 카테고리별", "2023 원료별"])

            df_tab1, df_tab2, df_tab3, df_tab4 = dfs.values()
        
            with tab1:
                st.dataframe(df_tab1)
            with tab2:
                st.dataframe(df_tab2)
            with tab3:
                st.dataframe(df_tab3)
            with tab4:
                st.dataframe(df_tab4)

        # 기본 설정값
        st.markdown("""---""")
        st.header("분석 도구")
        col1, col2 = st.columns([2,1])
        item = col1.radio(
            "아이템 종류 선택 👇",
            ["제형별", "제조사별", "카테고리별", "원료별"], 
            horizontal=True
        )
        criterion = col2.radio(
            "시간 기준 선택 👇",
            ["전체", "년도별", "월별", "직접 선택"], 
            horizontal=True
        )
        if(criterion == "직접 선택"):
            start_date_str, finish_date_str = select_date(df_tab1)
        temp = st.radio(
                "제품 선택 👇",
                ["전체", "직접 선택"], 
                horizontal=True
            )
        


        # 데이터 프레임 가공
        selected_columns = df_tab1[["등록일", "제형","제품명", "제조사",
                        "기능성", "주원료","부원료", "기능성내용", "품목번호"]]
        selected_columns["등록일"] = pd.to_datetime(selected_columns["등록일"], format="%Y%m%d")
        selected_columns["연도"] = selected_columns["등록일"].dt.year
        selected_columns["월"] = selected_columns["등록일"].dt.month
        selected_columns["일"] = selected_columns["등록일"].dt.day
        selected_columns.loc[:, '날짜'] = pd.to_datetime(selected_columns['등록일'], format='%Y%m%d').dt.strftime('%Y-%m')


        # 아이템 종류 선택
        if(item == "제형별"):
            var = "제형"
        elif(item == "제조사별"):
            var = "제조사"
        elif(item == "카테고리별"):
            selected_columns = add_p3_in_df(selected_columns)
        elif(item == "원료별"):
            selected_columns = add_p4_in_df(selected_columns)
        
        # 제품 선택
        if(temp == "전체"):
            if(item == "카테고리별"):
                multi_select = ['기초영양소', '다이어트', '장건강', '뼈', '관절', '항산화', '혈행', '혈당', 
                                '면역', 'Mind 건강', 'Brain 건강', '눈', '간', '배변활동', '이너뷰티', 
                                '여성건강', '남성건강', '단백질']
            elif(item == "원료별"):
                multi_select = ["프로바이오틱스", "비타민미네랄","가르시니아","EPA및DHA","홍삼","밀크씨슬",
                                "칼마디","MSM / NAG","비타민C", "비오틴","비타민BC","눈 건강","프로폴리스",
                                "차전자피식이섬유","쏘팔메토/옥타코사놀","바나바잎추출","은행잎추출","콜라겐"]
            else:
                multi_select = list(selected_columns.groupby([var]).count()["등록일"].index)
        else: #직접 선택
            if(item == "카테고리별"):
                multi_select = st.multiselect('선택', ['기초영양소', '다이어트', '장건강', '뼈', '관절', '항산화', '혈행', 
                                                     '혈당', '면역', 'Mind 건강', 'Brain 건강', '눈', '간', '배변활동', 
                                                     '이너뷰티', '여성건강', '남성건강', '단백질'])
            elif(item == "원료별"):
                multi_select = st.multiselect('선택', ["프로바이오틱스", "비타민미네랄","가르시니아","EPA및DHA","홍삼","밀크씨슬",
                                "칼마디","MSM / NAG","비타민C", "비오틴","비타민BC","눈 건강","프로폴리스",
                                "차전자피식이섬유","쏘팔메토/옥타코사놀","바나바잎추출","은행잎추출","콜라겐"])
            else:
                multi_select = st.multiselect('선택', list(selected_columns.groupby([var]).count()["등록일"].index))

        
        # 기간 선택
        if(criterion == "전체"):
            # on = st.toggle('오름차순', value = True)
            tab1_c, tab2_c, tab3_c, tab4_c = st.tabs(["Area", "Bar", "Line", "Sicatter"])
            if((item == "카테고리별") or (item == "원료별")):
                chart_data = selected_columns[multi_select].sum()
            else:
                chart_data = selected_columns[selected_columns[var].isin(multi_select)]
                chart_data = chart_data.groupby([var]).count()["등록일"]
                chart_data.name = "합계"

            # if on:
            #     chart_data2 = chart_data.sort_values(ascending=True)
            # else:
            #     chart_data2 = chart_data.sort_values(ascending=False)

            st.write(chart_data)
            with tab1_c:
                st.area_chart(chart_data)
            with tab2_c:
                st.bar_chart(chart_data)
            with tab3_c:
                st.line_chart(chart_data)
            with tab4_c:
                st.scatter_chart(chart_data)
        
        elif(criterion == "년도별"):
            tab1_c, tab2_c, tab3_c, tab4_c = st.tabs(["Area", "Bar", "Line", "Sicatter"])
            if((item == "카테고리별") or (item == "원료별")):
                chart_data = selected_columns.groupby("연도")[multi_select].sum()
            else:
                chart_data = selected_columns[selected_columns[var].isin(multi_select)]
                chart_data = chart_data.groupby([var, "연도"]).size().unstack(fill_value=0).T.sort_index(axis=1)
            st.write(chart_data)

            with tab1_c:
                st.area_chart(chart_data)
            with tab2_c:
                st.bar_chart(chart_data)
            with tab3_c:
                st.line_chart(chart_data)
            with tab4_c:
                st.scatter_chart(chart_data)
            
        elif(criterion == "월별"):
            tab1_c, tab2_c, tab3_c, tab4_c = st.tabs(["Area", "Bar", "Line", "Sicatter"])
            if((item == "카테고리별") or (item == "원료별")):
                chart_data = selected_columns.groupby("월")[multi_select].sum()
            else:
                chart_data = selected_columns[selected_columns[var].isin(multi_select)]
                chart_data = chart_data.groupby([var, "월"]).size().unstack(fill_value=0).T
            st.write(chart_data)
            with tab1_c:
                st.area_chart(chart_data)
            with tab2_c:
                st.bar_chart(chart_data)
            with tab3_c:
                st.line_chart(chart_data)

            with tab4_c:
                st.scatter_chart(chart_data)
        
        elif(criterion == "직접 선택"):
            tab1_c, tab2_c, tab3_c, tab4_c = st.tabs(["Area", "Bar", "Line", "Sicatter"])

            if((item == "카테고리별") or (item == "원료별")):
                filtered_df = selected_columns[selected_columns["등록일"] >= start_date_str]
                filtered_df = filtered_df[filtered_df["등록일"] <= finish_date_str]
                pivot_data = filtered_df.groupby("날짜")[multi_select].sum()
                pass
            else:
                filtered_df = selected_columns[selected_columns["등록일"] >= start_date_str]
                filtered_df = filtered_df[filtered_df["등록일"] <= finish_date_str]
                chart_data = filtered_df[filtered_df[var].isin(multi_select)]
                chart_data2 = chart_data.groupby([var,"날짜"]).count()["등록일"]
                pivot_data = chart_data2.reset_index().pivot_table(index='날짜', columns=var, values='등록일', fill_value=0)
            st.write(pivot_data)
            with tab1_c:
                st.area_chart(pivot_data)
            with tab2_c:
                st.bar_chart(pivot_data)
            with tab3_c:
                st.line_chart(pivot_data)

            with tab4_c:
                st.scatter_chart(pivot_data)
                pass

        add_bottom_view()
    except UnboundLocalError:
        pass

def add_bottom_view():
    st.write("")
    st.write("")
    st.write("")
    st.write("")
    st.write("")
    st.write("")
    st.write("")
    st.write("")
    st.write("")
    st.write("")
    st.write("")
    st.write("")
    st.write("")
    st.write("")
    st.write("")
    st.write("")
    st.write("")
    st.write("")



def show_chart(chart_data, flag_num):
    tab1_c, tab2_c, tab3_c, tab4_c, tab5_c, tab6_c, tab7_c, tab8_c = st.tabs(["Area", "Bar", "Line", 
                        "Sicatter", "Matplotlib", "Altair", 
                        "Vega-Lite", "Plotly"])

    with tab1_c:
        pass
    with tab2_c:
        pass
    with tab3_c:
        pass
    with tab4_c:
        pass
    with tab5_c: 
        pass
    with tab6_c:
        pass
    with tab7_c:
        pass
    with tab8_c:
        pass




def select_date(df):
    min_date = df['등록일'].min()
    max_date = df['등록일'].max()

    col1, col2 = st.columns([2, 2])
    start_date = col1.date_input("시작 날짜를 선택하세요", pd.to_datetime(str(min_date), format='%Y%m%d'))
    end_date = col2.date_input("종료 날짜를 선택하세요", pd.to_datetime(str(max_date), format='%Y%m%d'))
    st.write("선택한 기간:", start_date, "부터", end_date)
    
    start_date_str = start_date.strftime("%Y%m%d")
    finish_date_str = end_date.strftime("%Y%m%d")
    return start_date_str, finish_date_str



def add_p3_in_df(dff):
    # 각 항목 열을 0으로 초기화
    p3 = ['기초영양소', '다이어트', '장건강', '뼈', '관절', '항산화', '혈행', '혈당', '면역', 
          'Mind 건강', 'Brain 건강', '눈', '간', '배변활동', '이너뷰티', '여성건강', '남성건강', '단백질']
    df_p3 = dff.copy()
    for col in p3:
        df_p3[col] = 0

    # 각 행을 반복하여 필요한 항목 열을 업데이트
    for i in range(len(df_p3)):
        row = df_p3.iloc[i]
        
        # 기초영양소
        if all(j not in str(row['기능성']) for j in gosi) and any(j in str(row['기능성']) for j in vita) and '제20' not in str(row['기능성']):
            df_p3.at[i, '기초영양소'] = 1

        # 다이어트
        if '체지방' in str(row['기능성내용']):
            df_p3.at[i, '다이어트'] = 1

        # 장건강
        if '장 건강' in str(row['기능성내용']) or '장건강' in str(row['기능성내용']):
            df_p3.at[i, '장건강'] = 1

        # 뼈
        if any(keyword in str(row['기능성내용']) for keyword in ['뼈 건강', '뼈건강', '뼈']) and any(keyword in str(row['기능성']) for keyword in ['칼슘', '망간', 'D', '마그네슘']):
            df_p3.at[i, '뼈'] = 1

        # 관절
        if '관절' in str(row['기능성내용']):
            df_p3.at[i, '관절'] = 1

        # 항산화
        if '항산화' in str(row['기능성내용']) and ('코엔자임' in str(row['기능성']) or '프로폴리스' in str(row['기능성'])):
            df_p3.at[i, '항산화'] = 1

        # 혈행
        if '혈행' in str(row['기능성내용']) or '오메가3' in str(row['기능성']) or '오메가 3' in str(row['기능성']):
            df_p3.at[i, '혈행'] = 1

        # 혈당
        if '혈당' in str(row['기능성내용']):
            df_p3.at[i, '혈당'] = 1

        # 면역력
        if (('면역력' in str(row['기능성내용']) or 
            '면역기능' in str(row['기능성내용'])) and 
            ('아연' not in str(row['기능성']) and '베타글로칸' not in str(row['기능성']) and 
            '알로에' not in str(row['기능성']) and '홍삼' not in str(row['기능성']))):
            df_p3.at[i, '면역'] = 1

        # Mind 건강
        if (('스트레스' in str(row['기능성내용']) or '수면' in str(row['기능성내용']) or 
            '긴장' in str(row['기능성내용']) or '피로' in str(row['기능성내용']))):
            df_p3.at[i, 'Mind 건강'] = 1

        # Brain 건강
        if '인지' in str(row['기능성내용']) or '기억' in str(row['기능성내용']):
            df_p3.at[i, 'Brain 건강'] = 1

        # 눈
        if '눈' in str(row['기능성내용']) and 'EPA' not in str(row['기능성']):
            df_p3.at[i, '눈'] = 1

        # 간
        if '간 건강' in str(row['기능성내용']) or '간' in str(row['기능성내용']):
            df_p3.at[i, '간'] = 1

        # 배변활동
        if '배변활동' in str(row['기능성내용']) or '배변' in str(row['기능성내용']):
            df_p3.at[i, '배변활동'] = 1

        # 이너뷰티
        if '보습' in str(row['기능성내용']) or '자외선' in str(row['기능성내용']):
            df_p3.at[i, '이너뷰티'] = 1

        # 여성건강
        if '여성' in str(row['기능성내용']) and '홍삼' not in str(row['기능성']):
            df_p3.at[i, '여성건강'] = 1

        # 남성건강
        if '남성' in str(row['기능성내용']) or '전립선' in str(row['기능성내용']):
            df_p3.at[i, '남성건강'] = 1

        # 단백질
        if '단백질' in str(row['주원료']):
            df_p3.at[i, '단백질'] = 1

    return df_p3


def add_p4_in_df(dff):

    # 각 항목 열을 0으로 초기화
    p4 = ["프로바이오틱스", "비타민미네랄", "가르시니아", "EPA및DHA", "홍삼", "밀크씨슬",
        "칼마디", "MSM / NAG", "비타민C", "비오틴", "비타민BC",
        "눈 건강", "프로폴리스", "차전자피식이섬유", "쏘팔메토/옥타코사놀", "바나바잎추출",
        "은행잎추출", "콜라겐"]

    # 복사본 생성
    df_p4 = dff.copy()

    # 각 열을 0으로 초기화
    for col in p4:
        df_p4[col] = 0

    for i in range(len(dff)):
        row = df_p4.iloc[i]

        # 프로바이오틱스
        if ((str(row["기능성"]).count("프로바이오틱스") >= 1) and
                (str(row["제품명"]).count("혼합") == 0) and
                (str(row["제품명"]).count("분말") == 0)):
            df_p4.at[i, "프로바이오틱스"] = 1

        # 비타민미네랄
        flag1 = False
        flag2 = False
        for j in gosi:
            if (str(row["주원료"]).count(j) >= 1):
                flag1 = True
                break

        for j in vita:
            if (str(row["주원료"]).count(j) >= 1):
                flag2 = True
                break

        if (not flag1 and flag2 and str(row["기능성"]).count("제20") == 0):
            df_p4.at[i, "비타민미네랄"] = 1

        # 가르시니아
        if (str(row["주원료"]).count("가르시니아") >= 1):
            df_p4.at[i, "가르시니아"] = 1

        # EPA및DHA
        if (str(row["주원료"]).count("EPA") >= 1 or str(row["주원료"]).count("DHA") >= 1 or
                str(row["주원료"]).count("오메가3") >= 1 or str(row["주원료"]).count("오메가 3") >= 1 or
                str(row["주원료"]).count("리놀렌산") >= 1 or str(row["주원료"]).count("IPA") >= 1):
            df_p4.at[i, "EPA및DHA"] = 1

        # 홍삼
        if (str(row["주원료"]).count("홍삼") >= 1):
            df_p4.at[i, "홍삼"] = 1

        # 밀크씨슬
        if (str(row["주원료"]).count("밀크씨슬") >= 1):
            df_p4.at[i, "밀크씨슬"] = 1

        # 칼마디
        if (str(row["주원료"]).count("칼슘") >= 1 or str(row["주원료"]).count("마그네슘") >= 1 or
                str(row["주원료"]).count("비타민D") >= 1 or str(row["주원료"]).count("비타민 D") >= 1):
            df_p4.at[i, "칼마디"] = 1

        # MSM / NAG
        if (str(row["주원료"]).count("엠에스엠") >= 1 or str(row["주원료"]).count("N-아세틸") >= 1 or
                str(row["주원료"]).count("MSM") >= 1 or str(row["주원료"]).count("NAG") >= 1 or
                str(row["주원료"]).count("N - 아세틸") >= 1):
            df_p4.at[i, "MSM / NAG"] = 1

        # 비타민C
        if (str(row["주원료"]).count("비타민C") >= 1 or str(row["주원료"]).count("비타민 C") >= 1):
            df_p4.at[i, "비타민C"] = 1

        # 비오틴
        if (str(row["주원료"]).count("비오틴") >= 1 or (str(row["주원료"]).count("비오틴") >= 1 and
                                                    str(row["주원료"]).count("판토텐산") >= 1)):
            df_p4.at[i, "비오틴"] = 1

        # 비타민BC
        cnt_bc = 0
        for j in bc:
            if (str(row["주원료"]).count(j) >= 1):
                cnt_bc += 1
        if (cnt_bc >= 2):
            df_p4.at[i, "비타민BC"] = 1

        # 눈 건강
        if (str(row["주원료"]).count("마리골드") >= 1 or str(row["주원료"]).count("지아잔틴") >= 1):
            df_p4.at[i, "눈 건강"] = 1

        # 프로폴리스
        if (str(row["주원료"]).count("프로폴리스") >= 1):
            df_p4.at[i, "프로폴리스"] = 1

        # 차전자피식이섬유
        if (str(row["주원료"]).count("차전자피") >= 1):
            df_p4.at[i, "차전자피식이섬유"] = 1

        # 쏘팔메토/옥타코사놀
        if (str(row["주원료"]).count("쏘팔메토") >= 1 or str(row["주원료"]).count("옥타코사놀") >= 1):
            df_p4.at[i, "쏘팔메토/옥타코사놀"] = 1

        # 바나바잎추출
        if (str(row["주원료"]).count("바나바") >= 1):
            df_p4.at[i, "바나바잎추출"] = 1

        # 은행잎추출
        if (str(row["주원료"]).count("은행잎") >= 1):
            df_p4.at[i, "은행잎추출"] = 1

        # 콜라겐
        if (str(row["주원료"]).count("콜라겐") >= 1):
            df_p4.at[i, "콜라겐"] = 1
    return df_p4


if __name__ == "__main__":
    tab3_content()