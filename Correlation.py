import streamlit as st
import pandas as pd
import numpy as np
from streamlit.components.v1 import html

#cheeky js to navigate to other pages src: https://github.com/streamlit/streamlit/issues/4832
def nav_page(Sensitivity_Slider, timeout_secs=3):
    nav_script = """
        <script type="text/javascript">
            function attempt_nav_page(page_name, start_time, timeout_secs) {
                var links = window.parent.document.getElementsByTagName("a");
                for (var i = 0; i < links.length; i++) {
                    if (links[i].href.toLowerCase().endsWith("/" + page_name.toLowerCase())) {
                        links[i].click();
                        return;
                    }
                }
                var elasped = new Date() - start_time;
                if (elasped < timeout_secs * 1000) {
                    setTimeout(attempt_nav_page, 100, page_name, start_time, timeout_secs);
                } else {
                    alert("Unable to navigate to page '" + page_name + "' after " + timeout_secs + " second(s).");
                }
            }
            window.addEventListener("load", function() {
                attempt_nav_page("%s", new Date(), %d);
            });
        </script>
    """ % (Sensitivity_Slider, timeout_secs)
    html(nav_script)

st.title('Select Element and Correlation')

# create file uploader for csv only
file = st.file_uploader('Upload File', type='.csv')

# if file has been uploaded
if file is not None:
    # read csv file
    file = pd.read_csv(file)

    # remove unncessary columns
    file.drop(index = file.index[0], axis = 1, inplace = True)
    file.drop('SAMPLE', axis = 1, inplace = True)
    file.drop('Final pH', axis = 1, inplace = True)

    # create lists for elements and correlations types
    elements = list(file.columns.values)
    cor_types = ['pearson', 'spearman', 'kendall']

    # create dropdown menus for elements and correlation types
    element1 = st.selectbox('Select Main ELement', elements)
    cor_type1 = st.selectbox('Select Correlation Type', cor_types)

    # create button to analyse data
    next1 = st.button('Analyse')

    # if button has been pressed
    if next1:
        # Converts ppm to ppb
        ppm = []
        for element in file.columns:
            if file[element].iloc[0] == 'ppm':
                ppm.append(element)

        # convert to float
        for c in file.columns:
            file[c] = file[c].astype(float)

        # multiply ppm values by 1000 to so everythign becomes ppb
        for element in ppm:
            file[element] = file[element].apply(lambda x: x*1000)
        
        # set correlation type
        corr_matrix = file.corr(method=cor_type1, numeric_only = False)

        # function that correlates data
        def correlation(dataset, threshold, correlation):
            col_corr = set() # Set of all the names of correlated columns
            corr_matrix = dataset.corr(method=correlation, numeric_only = False)
            
            for i in range(len(corr_matrix.columns)):
                for j in range(i):
                    if abs(corr_matrix.iloc[i,j]) > threshold:
                        colname = corr_matrix.columns[i]
                        col_corr.add(colname)
            return col_corr
        
        # correlate data with initial 0.8 threshold
        col_corr = correlation(file, 0.8, cor_type1)

        # I don't quite understand these sections

        # # Converts col_corr from set to list
        # list_col_corr = list(col_corr)
        # # Put it into a dataframe
        # corr_df = file[list_col_corr]
        # # create matrix
        # corr_df_matrix = corr_df.corr(method=cor_type1, numeric_only = False)
        # dataFinal = corr_df_matrix[element1].sort_values(element1,ascending = True)

        # show data in dataframe table (replace with actual data later)
        dataFinal = corr_matrix[[element1]]
        st.dataframe(data=dataFinal, width=200, height=300)

        with st.form("slider_form"):
            # creates a sensitivity slider between 0 and 100 (values to two decimal points)
            sensitivity = st.slider('Sensitivity selection', 0.00, 100.00, 50.00)
            st.write("You have selected a sensitivy of ", sensitivity, '%')

            #button to confirm sensitivity selection
            next2 = st.form_submit_button("Visualise")

#button to go to page 2
with st.form("Go to Page 2 Button"):
    sensitivity_button = st.form_submit_button("Go to Page 2")
if sensitivity_button:
    nav_page("Sensitivity_Slider")

    