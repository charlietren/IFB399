import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

st.title('Generate Report')

# st.write("You have entered", st.session_state["my_input"])

file = st.session_state["file"]
element1 = st.session_state["element1"]
threshold = st.session_state["threshold"]
cor_type1 = st.session_state["cor_type1"]

st.dataframe(data=file)

st.write("element1: " + element1)
st.write("threshold: " + str(threshold))


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


