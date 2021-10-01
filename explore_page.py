import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def shorten_categories(categories, cutoff):
    categorical_map = {}
    for i in range(len(categories)):
        if categories.values[i] >= cutoff:
            categorical_map[categories.index[i]] = categories.index[i]
        else:
            categorical_map[categories.index[i]] = "Other"
    return categorical_map


def clean_education(x):
    if "Bachelor’s degree" in x:
        return "Bachelor’s degree"
    if "Master’s degree" in x:
        return "Master’s degree"
    if "Professional degree" in x or "doctoral" in x:
        return "Post grad"
    return "Less than a Bachelor's degree"

def clean_experience(x):
    if x == 'More than 50 years':
        return 50
    if x == 'Less than 1 year':
        return 0.5
    return float(x)

@st.cache
def load_data():
    df = pd.read_csv('survey_results_public.csv')
    df = df[['Country', 'EdLevel', 'YearsCodePro', 'Employment', 'ConvertedCompYearly']]
    df = df.rename({'ConvertedCompYearly': 'Salary'}, axis=1)
    df1 = df.copy()
    df1.Salary = df['Salary'].fillna(df.Salary.median())
    df1 = df1[df1['Employment'] == "Employed full-time"]
    df1 = df1.drop("Employment", axis=1)
    df1['EdLevel'] = df1['EdLevel'].fillna("Bachelor’s degree (B.A., B.S., B.Eng., etc.)")
    list_year = df['YearsCodePro'].value_counts()[:8].index
    df1['YearsCodePro'] = df1['YearsCodePro'].fillna(np.random.choice(list_year))
    country_map = shorten_categories(df1.Country.value_counts(), 400)
    df1['Country'] = df1['Country'].map(country_map)
    df2 = df1[(df1['Salary'] >= 10000) & (df1['Salary'] <= 250000) & (df1['Country'] != "Other")]
    df2['YearsCodePro'] = df2['YearsCodePro'].apply(clean_experience)
    df2['EdLevel'] = df2['EdLevel'].apply(clean_education)

    return df2

df = load_data()

def show_explore_page():
    st.title("Explore Software Engineer Salaries")
    st.write(
        """
        ### Stack Overflow Developer Survey 2021
        """
    )
    data = df["Country"].value_counts()

    fig1, ax1 = plt.subplots()
    ax1.pie(data, labels=data.index, autopct='%1.1f%%', shadow=True, startangle=90)
    ax1.axis("equal")

    st.write("""#### Number of datapoint from different countries""")

    st.pyplot(fig1)

    st.write("""
        #### Mean salary based on countries
    """)

    data = df.groupby('Country')['Salary'].mean().sort_values(ascending=False)
    st.bar_chart(data)

    st.write("""
    #### Mean salary based on experience
    """)

    data = df.groupby("YearsCodePro")['Salary'].mean().sort_values(ascending=False)
    st.line_chart(data)
    