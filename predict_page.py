import streamlit as st
import pickle
import numpy as np

def load_model():
    with open('saved_model.pkl', 'rb') as f:
        data = pickle.load(f)
    return data

data = load_model()

regressor = data["model"]
le_country = data["le_country"]
le_education = data["le_education"]

def show_predict_page():
    st.title("Software Developer Salary Prediction")

    st.write("""### We need some information to predict the salary""")

    country = (
        'United States of America', 'Other', 'India', 'Germany',
       'United Kingdom of Great Britain and Northern Ireland', 'Canada',
       'France', 'Brazil', 'Australia', 'Spain', 'Netherlands', 'Italy',
       'Russian Federation', 'Poland', 'Sweden', 'China', 'Israel', 'Turkey',
       'Switzerland', 'Ukraine', 'Iran, Islamic Republic of...', 'Norway',
       'Pakistan', 'Mexico', 'Belgium', 'Austria', 'Denmark',
       'Czech Republic'
    )

    education = (
        "Less than a Bachelor's degree",
        "Bachelor’s degree",
        "Master’s degree",
        "Post grad",
    )

    country = st.selectbox(label="Country", options=country)
    education = st.selectbox(label="Education Level", options=education)
    experience = st.slider("Years of Experience", min_value=0, max_value=50, value=3)

    btn_clicked = st.button("Calculate Salary")
    if btn_clicked:
        X = np.array([[country, education, experience]])
        X[:, 0] = le_country.transform(X[:, 0])
        X[:, 1] = le_education.transform(X[:, 1])
        X = X.astype(float)

        salary = regressor.predict(X)

        st.subheader(f"The estimated salary is ${salary[0]:.2f}")

    