import streamlit as st
import pandas as pd
import numpy as np

st.title('Generate Report')

df = pd.read_csv("BR20279856_cleaned.csv")

dataCSV = st.file_uploader('Upload File', type='.csv')
dataCSV = pd.DataFrame(dataCSV)

list = dataCSV.columns
list2 = ['Spearman', 'Pearson', 'Kendall']

result = st.selectbox('Select Main ELement', list)

result1 = st.selectbox('Select Correlation Type', list2)

print(dataCSV.columns)



with st.form("Generate Report"):
    button_check2 = st.form_submit_button("Generate Report")
