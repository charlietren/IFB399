import streamlit as st
import pandas as pd
import numpy as np

import streamlit as st
import pandas as pd
import numpy as np

from streamlit.components.v1 import html

st.title('Select Element and Correlation')

file = st.file_uploader('Upload File', type='.csv')

if file is not None:
    file = pd.read_csv(file)

    file.drop(index = file.index[0], axis = 1, inplace = True)
    file.drop('SAMPLE', axis = 1, inplace = True)
    file.drop('Final pH', axis = 1, inplace = True)

    elements = list(file.columns.values)
    cor_types = ['Spearman', 'Pearson', 'Kendall']

    element1 = st.selectbox('Select Main ELement', elements)

    cor_type1 = st.selectbox('Select Correlation Type', cor_types)

with st.form("Go to Page 2 Button"):
    button_check1 = st.form_submit_button("Go to Page 2")

