import streamlit as st
import pandas as pd
import numpy as np
from streamlit.components.v1 import html

#cheeky js to navigate to other pages src: https://github.com/streamlit/streamlit/issues/4832
def nav_page(Generate_Report, timeout_secs=3):
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
    """ % (Generate_Report, timeout_secs)
    html(nav_script)


st.title('Sensitivity Slider')

next = st.button("Sensitivity Slider")
if next:
    switch_page("Sensitivity Slider")

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
    dataframe = pd.read_csv('BR20279856_cleaned.csv', skipinitialspace=True, usecols=elements)
    st.write(dataframe.Ag)
    
#button to go to page 3
with st.form("Go to Page 3 Button"):
    sensitivity_button = st.form_submit_button("Go to Page 3")
if sensitivity_button:
    nav_page("Generate_Report")
