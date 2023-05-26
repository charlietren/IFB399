import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

for k, v in st.session_state.items():
    st.session_state[k] = v


from streamlit.components.v1 import html

from streamlit_extras.switch_page_button import switch_page

# #cheeky js to navigate to other pages src: https://github.com/streamlit/streamlit/issues/4832
# def nav_page(Sensitivity_Slider, timeout_secs=3):
#     nav_script = """
#         <script type="text/javascript">
#             function attempt_nav_page(page_name, start_time, timeout_secs) {
#                 var links = window.parent.document.getElementsByTagName("a");
#                 for (var i = 0; i < links.length; i++) {
#                     if (links[i].href.toLowerCase().endsWith("/" + page_name.toLowerCase())) {
#                         links[i].click();
#                         return;
#                     }
#                 }
#                 var elasped = new Date() - start_time;
#                 if (elasped < timeout_secs * 1000) {
#                     setTimeout(attempt_nav_page, 100, page_name, start_time, timeout_secs);
#                 } else {
#                     alert("Unable to navigate to page '" + page_name + "' after " + timeout_secs + " second(s).");
#                 }
#             }
#             window.addEventListener("load", function() {
#                 attempt_nav_page("%s", new Date(), %d);
#             });
#         </script>
#     """ % (Sensitivity_Slider, timeout_secs)
#     html(nav_script)


st.set_page_config(
    page_title="Multipage App",
    initial_sidebar_state="collapsed"
)

# Hide Sidebar 
st.markdown(
     """
 <style>
     [data-testid="collapsedControl"] {
         display: none
     }
 </style>
 """,
     unsafe_allow_html=True,
)

# Title
st.title('Select Element and Correlation')

# create file uploader for csv only
file = st.file_uploader('Upload File', type='.csv')

if "file" not in st.session_state:
    st.session_state["file"] = ""

# if file has been uploaded
if file is not None:
    # read csv file
    if file is not None:
        file = pd.read_csv(file)

    # Saves uploaded file to be used in other session states
    st.session_state["file"] = file

    # Data Preprocessing 
    # Converts ppm to ppb
    ppm = []

    for element in file.columns:
        if file[element].iloc[0] == 'ppm':
            ppm.append(element)
    
    # remove unncessary columns
    file.drop(index = file.index[0], axis = 1, inplace = True)
    file.drop('SAMPLE', axis = 1, inplace = True)
    file.drop('Final pH', axis = 1, inplace = True)

    for c in file.columns:
        file[c] = file[c].astype(float)

    # multiply ppm values by 1000 to so everythign becomes ppb
    for element in ppm:
        file[element] = file[element].apply(lambda x: x*1000)

    # create lists for elements and correlations types
    elements = ['Choose'] + list(file.columns.values)
    cor_types = ['Choose', 'pearson', 'spearman', 'kendall']

    # create dropdown menus for elements and correlation types
    element1 = st.selectbox('Select Element Of Interest', elements)
    cor_type1 = st.selectbox('Select Correlation Type', cor_types)

    # if element has been chosen
    if element1 != 'Choose' and cor_type1 != 'Choose':
        
        # set correlation type
        corr_matrix = file.corr(method=cor_type1, numeric_only = False)

        # # if element is the filtered columns
        # if element1 in corr_df_matrix.columns:

        # new title
        st.title('Select Correlation Threshold')

        # sort matrix
        # dataFinal = corr_df_matrix[[element1]].sort_values(element1, ascending = True)
        dataFinal = corr_matrix[[element1]].sort_values(element1, ascending = True)

        # show data in dataframe table (replace with actual data later)
        st.dataframe(data=dataFinal, width=200, height=300)
        # st.dataframe(data=dataFinal, width=200, height=300)

        # creates a sensitivity slider between 0 and 100 (values to two decimal points)
        # sensitivity = st.slider('Sensitivity selection', 0.00, 100.00, 0.00)
        threshold = st.number_input('Threshold', min_value=0.0, max_value=0.99, value=0.0, step = 0.1)
        st.write("You have selected a threshold of ", threshold, '%')

        if "threshold" not in st.session_state:
            st.session_state["threshold"] = ""

        st.session_state["threshold"] = threshold
        

        generate_report = st.button("Generate Report!")
        if generate_report:
            switch_page("Generate Report")
       
        if "element1" not in st.session_state:
            st.session_state["element1"] = ""

        st.session_state["element1"] = element1

        if "cor_type1" not in st.session_state:
            st.session_state["cor_type1"] = ""

        st.session_state["cor_type1"] = cor_type1
        
        if "file" not in st.session_state:
            st.session_state["file"] = ""

        st.session_state["file"] = file
    
        # if element is not in filtered columns, display error and list available elements
        # else:
        #     st.error('Please try another element', icon="🚨")
        #     st.error('Available elements:')
        #     st.error(corr_df_matrix.columns.values)
        
        

# #button to go to page 2
# with st.form("Go to Page 2 Button"):
#     sensitivity_button = st.form_submit_button("Go to Page 2")
# if sensitivity_button:
#     nav_page("Sensitivity_Slider")

    
