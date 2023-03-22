import pandas as pd
import streamlit as st

import os
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

st.set_page_config(page_title='人相占い')
st.markdown('#### 人相占い')

#current working dir
cwd = os.path.dirname(__file__)

#**********************gdriveからエクセルファイルのダウンロード・df化

# Google Drive APIを使用するための認証情報を取得する
creds_dict = st.secrets["gcp_service_account"]
creds = service_account.Credentials.from_service_account_info(creds_dict)

# Drive APIのクライアントを作成する
#API名（ここでは"drive"）、APIのバージョン（ここでは"v3"）、および認証情報を指定
service = build("drive", "v3", credentials=creds)

# 指定したファイル名を持つファイルのIDを取得する
#Google Drive上のファイルを検索するためのクエリを指定して、ファイルの検索を実行します。
# この場合、ファイル名とMIMEタイプを指定しています。
file_name = "人相占い.xlsx"
query = f"name='{file_name}' and mimeType='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'"
#指定されたファイルのメディアを取得
results = service.files().list(q=query).execute()
items = results.get("files", [])

if not items:
    st.warning(f"No files found with name: {file_name}")
else:
    # ファイルをダウンロードする
    file_id = items[0]["id"]
    file = service.files().get(fileId=file_id).execute()
    file_content = service.files().get_media(fileId=file_id).execute()

    # ファイルを保存する
    file_path = os.path.join(cwd, file_name)
    with open(file_path, "wb") as f:
        f.write(file_content)

path_file = os.path.join(cwd, '人相占い.xlsx')
df = pd.read_excel(
    path_file, sheet_name='Sheet1')


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



