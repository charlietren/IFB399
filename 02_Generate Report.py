import streamlit as st
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('agg')
import matplotlib.pyplot as plt
import seaborn as sns

import warnings
warnings.filterwarnings("ignore")

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

header_spacer1, header_1, header_spacer2 = st.columns((3, 6, 3))
with header_1:
    st.title('Generate Report')

# st.write("You have entered", st.session_state["my_input"])

file = st.session_state["file"]
element1 = st.session_state["element1"]
threshold = st.session_state["threshold"]
cor_type1 = st.session_state["cor_type1"]

# st.dataframe(data=file)
# st.write("element1: " + element1)
# st.write("threshold: " + str(threshold))

corr_matrix = file.corr(method=cor_type1, numeric_only = False)
dataFinal = corr_matrix[[element1]].sort_values(element1, ascending = True)

# Filter dataframe based on pos / neg correlation 
neg_corr_df = dataFinal[dataFinal[[element1]] < 0]
pos_corr_df = dataFinal[dataFinal[[element1]] >= threshold]

neg_corr_df.dropna(how = 'all', inplace = True)
neg_corr_df = neg_corr_df[[element1]]
pos_corr_df.dropna(how = 'all', inplace = True)
pos_corr_df = pos_corr_df[[element1]]

# Heatmap Plot#1

top5_pos_corr = pos_corr_df.sort_values(by = element1, ascending = False).reset_index()
top5_pos_corr.columns=['Feature','Correlation']
top5_pos_corr = top5_pos_corr.iloc[-6:-1]

top5_neg_corr = neg_corr_df.sort_values(by = element1, ascending = False).reset_index()
top5_neg_corr .columns=['Feature','Correlation']
top5_neg_corr = top5_neg_corr.iloc[-6:-1]

top5_neg_pos = pd.concat([top5_neg_corr, top5_pos_corr], axis = 0).reset_index()
top5_neg_pos = top5_neg_pos.drop('index', axis = 1)
columnNames = top5_neg_pos['Feature'].values
top5_neg_pos_corr_matrix = file[columnNames].corr(method = cor_type1, numeric_only = False)

st.subheader("1: Heatmap of top 5 Positive and Negative correlated elements")
fig=plt.figure(figsize=(15,8),facecolor='white')
sns.heatmap(top5_neg_pos_corr_matrix, annot = True, cmap = 'Greens')
st.pyplot(fig)
st.markdown("Based on the element, correlation type and threshold selected previously, we have generated a heatmap.The Correlation Heatmap provides a visually captivating representation of the relationships in the dataset, highlighting the top five elements exhibiting the highest positive and negative correlations.")
        
pos_corr_df = pos_corr_df.sort_values(by = element1, ascending = True).reset_index()
pos_corr_df.columns=['Feature','Correlation']
pos_corr_df = pos_corr_df.iloc[-11:-1]

st.subheader("2: Top 10 elements - Positive Correlation matched against selected element")
# palette = sns.color_palette("light:#5A9", as_cmap=True)
custom_palette = sns.color_palette("bright")     
fig=plt.figure(figsize=(15,8),facecolor='white')
ax0=fig.add_subplot(1,1,1)
ax0.grid(axis='y', color='gray', linestyle=':', dashes=(3,10))

palette=["mediumaquamarine" for i in range(16)]
barplot = sns.barplot(x='Correlation', y='Feature', data=pos_corr_df, palette = palette, zorder=3)
plt.bar_label(barplot.containers[0], fmt = '\n%.2f', label_type = 'center')

# Remove top and right borders
ax0.spines['top'].set_visible(False)
ax0.spines['right'].set_visible(False)

st.pyplot(fig)
st.markdown("The top 10 positively correlated barplot helps user to easily identify the elements with the strongest associations within the dataset based on element of the interest")

st.subheader("3: Top 10 elements - Negative Correlation matched against selected element")
# Top 10 Negative Correlation
neg_corr_df = neg_corr_df.sort_values(by = element1, ascending = False).reset_index()
neg_corr_df.columns=['Feature','Correlation']
neg_corr_df = neg_corr_df.iloc[-11:-1]

# Plotting with matplotlib
fig=plt.figure(figsize=(15,8),facecolor='white')

ax0=fig.add_subplot(1,1,1)
ax0.grid(axis='y', color='gray', linestyle=':', dashes=(3,10))

barplot = sns.barplot(x='Correlation', y='Feature', data=neg_corr_df, palette = palette)
plt.bar_label(barplot.containers[0], fmt = '\n%.2f', label_type = 'center')

# Remove top and right borders
ax0.spines['top'].set_visible(False)
ax0.spines['right'].set_visible(False)

# ax0.grid(axis='y', zorder=0, color='gray', linestyle=':', dashes=(3,10))
ax0.invert_xaxis()
st.pyplot(fig)
st.markdown("The top 10 negatively correlated barplot helps user to easily identify the elements with the strongest associations within the dataset based on the element of interest")

st.markdown("***")
st.markdown("The boxplot helps to offers a concise and informative summary of the top 5 positively and negatively correlated element's distribution. A brief description of how to read the boxplot is provided below:")
st.markdown("1. Median (Q2): The line within the box represents the median, which divides the data into two equal halves. It provides a measure of the central tendency, indicating the typical value around which the data is centered.")
st.markdown("2. Quartiles (Q1 and Q3): The box represents the interquartile range (IQR), which spans from the first quartile (Q1) to the third quartile (Q3). It contains the middle 50% of the data, offering insights into its spread and variability.")
st.markdown("3. Whiskers: The whiskers extend from the box to represent the data range. They typically encompass the data within 1.5 times the IQR. Observations outside this range are considered outliers and are depicted as individual data points.")
st.markdown("4. Outliers: Individual data points that fall outside the whiskers are plotted as distinct markers. Outliers may indicate extreme values or potential anomalies in the dataset.")


# Top 5 Positive Correlation Boxplot
st.subheader("4: Top 5 element - Positive Correlation Boxplot")
PosT5Elements = pos_corr_df['Feature'].iloc[-5:].values
fig=plt.figure(figsize=(15,8),facecolor='white')
sns.boxplot(data = file[PosT5Elements])
plt.xlabel('Element')
plt.ylabel('PPM')

plt.show()
st.pyplot(fig)

# Top 5 Negative Correlation Boxplot
st.subheader("5: Top 5 element - Negative Correlation Boxplot")
NegT5Elements = neg_corr_df['Feature'].iloc[-5:].values
fig=plt.figure(figsize=(15,8),facecolor='white')
sns.boxplot(data = file[NegT5Elements])
plt.xlabel('Element')
plt.ylabel('PPM')
st.pyplot(fig)
st.markdown("")