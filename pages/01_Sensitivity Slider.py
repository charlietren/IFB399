import streamlit as st
import pandas as pd
import numpy as np

st.title('Sensitivity Slider')


file = st.file_uploader('Upload File', type='.csv')

if file is not None:
    file = pd.read_csv(file)

    file.drop(index = file.index[0], axis = 1, inplace = True)
    file.drop('SAMPLE', axis = 1, inplace = True)
    file.drop('Final pH', axis = 1, inplace = True)

    elements = list(file.columns.values)
    cor_types = ['Spearman', 'Pearson', 'Kendall']

    main_element = st.selectbox('Select Main ELement', elements)

    cor_type1 = st.selectbox('Select Correlation Type', cor_types)


#button to display selected csv file
with st.form("Show Table button"):
    show_table_button = st.form_submit_button("Show Table")
if show_table_button:
        st.write(file)

#creates a sensitivity slider between 0 and 100 (values to two decimal points)
sensitivity = st.slider('Sensitivity selection', 0.00, 100.00, 50.00)
st.write("You have selected a sensitivy of ", sensitivity, '%')

#button to confirm sensitivity selection
with st.form("Apply Sensitivity Selection Button"):
    sensitivity_button = st.form_submit_button("Apply Sensitivity Selection")

#button to display elements based on sensitivity analysis
if sensitivity_button:
    fields = elements
    dataframe = pd.read_csv('BR20279856_cleaned.csv', skipinitialspace=True, usecols=fields)
    st.write(dataframe.Ag)
    
#button to go to page 3
with st.form("Go to Page 3 Button"):
    sensitivity_button = st.form_submit_button("Go to Page 3")
