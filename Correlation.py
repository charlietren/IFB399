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
# st.markdown(
#     """
# <style>
#     [data-testid="collapsedControl"] {
#         display: none
#     }
# </style>
# """,
#     unsafe_allow_html=True,
# )

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
    print(file)

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

        # creates a sensitivity slider between 0 and 100 (values to two decimal points)
        # sensitivity = st.slider('Sensitivity selection', 0.00, 100.00, 0.00)
        threshold = st.number_input('Threshold', min_value=0.0, max_value=0.99, value=0.0, step = 0.1)
        st.write("You have selected a threshold of ", threshold, '%')
        print(threshold)

        if "threshold" not in st.session_state:
            st.session_state["threshold"] = ""

        st.session_state["threshold"] = threshold
        # function that correlates data
        def correlation(dataset, correlation, threshold):
            col_corr = set() # Set of all the names of correlated columns
            corr_matrix = dataset.corr(method = correlation, numeric_only = False)
            
            for i in range(len(corr_matrix.columns)):
                for j in range(i):
                    if abs(corr_matrix.iloc[i,j]) > threshold:
                        colname = corr_matrix.columns[i]
                        col_corr.add(colname)
            return col_corr

        col_corr = correlation(file, cor_type1, threshold)
        
        # Converts col_corr from set to list
        list_col_corr = list(col_corr)
        # Put it into a dataframe
        corr_df = file[list_col_corr]
        print(corr_df)
        # create matrix
        corr_df_matrix = corr_df.corr(method = cor_type1, numeric_only = False)
        print(corr_df_matrix)    

        # Filter dataframe based on pos / neg correlation 
        neg_corr_df = corr_df_matrix[corr_df_matrix[[element1]] < 0]
        pos_corr_df = corr_df_matrix[corr_df_matrix[[element1]] >= 0]
        neg_corr_df.dropna(how = 'all', inplace = True)
        neg_corr_df = neg_corr_df[[element1]]
        pos_corr_df.dropna(how = 'all', inplace = True)
        pos_corr_df = pos_corr_df[[element1]]
        
        # if sensitivity has been chosen
        if threshold != 0.0:
            st.title('Visualisation Report')
            
            st.subheader('Plot #1 – Correlation Matrix:')
            # create heatmap
            figheat=plt.figure(figsize=(15,8),facecolor='white')
            sns.heatmap(corr_df_matrix, annot = True, cmap = 'Greens')
            st.pyplot(fig=figheat)
            st.markdown("Next, I performed EDA to gain insights into the asdhasdj.asdaijnkaksjajks")    
            # palette = sns.color_palette("light:#5A9", as_cmap=True)
            custom_palette = sns.color_palette("bright")
            pos_corr_df = pos_corr_df.sort_values(by = element1, ascending = True).reset_index()
            pos_corr_df.columns=['Feature','Correlation']

            st.subheader('Plot #2 – Positively correlated elements:')
            # create postive correlation bar graph
            # Correlation with selected variable
            figposbar=plt.figure(figsize=(15,8),facecolor='white')

            ax0=figposbar.add_subplot(1,1,1)
            ax0.grid(axis='y', color='gray', linestyle=':', dashes=(3,10))

            palette=["mediumaquamarine" for i in range(16)]
            # palette[2]='gold'
            # palette[4]='gold'
            barplot = sns.barplot(x='Correlation', y='Feature', data=pos_corr_df, palette = palette, zorder=3)
            plt.bar_label(barplot.containers[0], fmt = '\n%.2f', label_type = 'center')

            # Remove top and right borders
            ax0.spines['top'].set_visible(False)
            ax0.spines['right'].set_visible(False)

            # ax0.grid(axis='y', zorder=0, color='gray', linestyle=':', dashes=(3,10))
            # plt.title(f"Positive Correlation matched against {element1}")
            st.pyplot(fig=figposbar)
            st.markdown("Next, I performed EDA to gain insights into the asdhasdj.asdaijnkaksjajks") 

            st.subheader('Plot #3 – Negatively correlated elements:')
            # create negative correlation bar graph
            neg_corr_df = neg_corr_df.sort_values(by = element1, ascending = False).reset_index()
            neg_corr_df.columns=['Feature','Correlation']

            # Correlation with selected variable
            fignegbar=plt.figure(figsize=(15,8),facecolor='white')

            ax0=fignegbar.add_subplot(1,1,1)
            ax0.grid(axis='y', color='gray', linestyle=':', dashes=(3,10))

            # palette=["mediumaquamarine" for i in range(16)]
            # palette[2]='gold'
            # palette[4]='gold'
            barplot = sns.barplot(x='Correlation', y='Feature', data=neg_corr_df, palette = "Greens")
            plt.bar_label(barplot.containers[0], fmt = '\n%.2f', size = 14, label_type = 'center')

            # Remove top and right borders
            ax0.spines['top'].set_visible(False)
            ax0.spines['right'].set_visible(False)

            # ax0.grid(axis='y', zorder=0, color='gray', linestyle=':', dashes=(3,10))
            # plt.title(f"Negative Correlation matched against {element1}")
            ax0.invert_xaxis()
            st.pyplot(fig=fignegbar)


            st.subheader('Plot #4 – Top 5 positive correlated element boxplot:')
            # postive correlation boxplot
            PosT5Elements = pos_corr_df['Feature'].iloc[0:5].values

            figposbox, ax = plt.subplots()

            ax.boxplot(file[PosT5Elements])
            ax.set_xticklabels(PosT5Elements)
            ax.set_xlabel('Element')
            ax.set_ylabel('PPM')
            st.pyplot(fig=figposbox)
            
            st.subheader('Plot #5 Top 5 negative correlated element boxplot:')
            # negative correlation boxplot
            NegT5Elements = neg_corr_df['Feature'].iloc[0:5].values

            fignegbox, ax = plt.subplots()

            ax.boxplot(file[NegT5Elements])
            ax.set_xticklabels(NegT5Elements)
            ax.set_xlabel('Element')
            ax.set_ylabel('PPM')
            st.pyplot(fig=fignegbox)

            
                


        if "element1" not in st.session_state:
            st.session_state["element1"] = ""

        st.session_state["element1"] = element1
 
        # # if element is not in filtered columns, display error and list available elements
        # else:
        #     st.error('Please try another element', icon="🚨")
        #     st.error('Available elements:')
        #     st.error(corr_df_matrix.columns.values)
        
        

# #button to go to page 2
# with st.form("Go to Page 2 Button"):
#     sensitivity_button = st.form_submit_button("Go to Page 2")
# if sensitivity_button:
#     nav_page("Sensitivity_Slider")

    