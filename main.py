import pandas as pd
import streamlit as st

st.set_page_config(page_title='人相占い')
st.markdown('#### 人相占い')

@st.cache_data
def read_data(file):
    df = pd.read_excel(file)  # index　ナンバー不要　index_col=0

    return df 

file = '人相占い.xlsx'
df = read_data(file)

#*****部位1******
parts_list1 = list(df['部位1'].unique()) #np arrayからlistへ
parts_list1.insert(0, '--選択してください--')
parts1 = st.selectbox(
        '部位:',
        parts_list1,
        key='parts1'   
    ) 

if parts1 != '--選択してください--':
    df_parts1 = df[df['部位1']==parts1]

    parts_list2 = list(df_parts1['部位3'].unique()) #np arrayからlistへ
    parts_list2.insert(0, '--選択してください--')
    parts2 = st.selectbox(
            '部位（詳細）:',
            parts_list2,
            key='parts2'   
        )
    if parts1 != '--選択してください--':    
        df_parts2 = df_parts1[df_parts1['部位3']==parts2]    

        condition_list = list(df_parts2['特徴'].unique())
        condition_list.insert(0, '--選択してください--')
        condition = st.selectbox(
                '特徴',
                condition_list,
                key='cond1'   
            ) 

        df_parts_cond = df_parts2[df_parts2['特徴']==condition]

        st.table(df_parts_cond['性格/運命/未来'])

else:
    st.stop()

def clear_cache():
    read_data = st.empty()

st.sidebar.button("Update Program",on_click=clear_cache)

