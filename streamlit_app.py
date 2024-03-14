import numpy as np
import altair as alt
import pandas as pd
import streamlit as st




# 读取上传的文件
def launchFilter(df):  
    oven_options = df['oven_type'].unique()
    oven_filter = st.sidebar.selectbox('Oven', oven_options, index=0)
    return oven_filter

def launchTable(df,oven_filter):  
# 筛选数据
    df_filtered = df[df['oven_type'] == oven_filter]
    st.dataframe(df_filtered.head(20))
    return df_filtered

def launchKpi(df_filtered):
    col1, col2, col3 = st.columns(3)
    diff_mean = df_filtered['predicted_temp_incr_time - real_time_incre_time'].mean()
    avg_predicted_temp_incr_time = df_filtered['predicted_temp_incr_time'].mean()
    avg_real_time_incr_time = df_filtered['real_time_incre_time'].mean()
    # 在每个列中显示一个kpi
    col1.metric("Avg of predict Delta", round(diff_mean, 1))
    col2.metric("Avg of predicted_temp_incr_time", round(avg_predicted_temp_incr_time,1))
    col3.metric("Avg of real_time_incr_time", round(avg_real_time_incr_time,1))

def launchLineChart(df_filtered):
    st.header('显示折线图')
    df_filtered = df_filtered.sort_values(by='data_time')
    x_axis = 'data_time'
    y_axis = 'predicted_temp_incr_time - real_time_incre_time'
    st.line_chart(data=df_filtered, x=x_axis, y=y_axis)


def main():
    # 导入数据 和 筛选数据 
    uploaded_file = st.file_uploader("上传 CSV 文件")
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        df = df[df['oven_type'].notna()]
        oven_filter = launchFilter(df)
        st.header('显示筛选后的数据')
        df_filtered = launchTable(df,oven_filter)
        st.header('计算KPI')
        launchKpi(df_filtered)
        launchLineChart(df_filtered)
    else:
        st.divider()


main()