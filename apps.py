import streamlit as st
import pickle
import pandas as pd
import sys
import os
sys.path.append(os.path.abspath("apps.py"))  # Replace with actual folder

from extract_features import ExtractFeatures



@st.cache_resource
def get_model():
    """
    Loads the phishing URL detection model from a pickle file.
    This function reads and loads a pickled file containing the classifier.
    Returns:
        object: The loaded phishing URL detection model.
    Note:
        The model should be saved in a file named 'phishing_url_detector.pkl'.
        XGBoost module must be installed before using the file.
    """
    with open('phishing_url_detector.pkl', 'rb') as pickle_model:
        phishing_url_detector = pickle.load(pickle_model)
    return phishing_url_detector

st.title("Phishing Website Detector")
st.header("Are you sure you want to check sent the link?")

# Takes in user input
input_url = st.text_area("Put in your site link here: ")

if input_url != "":
    
    # Extracts features from the URL and converts it into a dataframe
    features_url = ExtractFeatures().url_to_features(url=input_url)
    features_dataframe = pd.DataFrame.from_dict([features_url])
    features_dataframe = features_dataframe.fillna(-1)
    features_dataframe = features_dataframe.astype(int)

    st.write("it is not phishing site!")
    st.cache_data.clear()
    prediction_str = ""

    # Predict outcome using extracted features
    try: 
        phishing_url_detector = get_model()
        prediction = phishing_url_detector.predict(features_dataframe)
        if prediction == int(True):
            prediction_str = 'Phishing Website. Do not click!'
        elif prediction == int(False):
            prediction_str = 'Not Phishing Website, stay safe!'
        else:
            prediction_str = ''
        st.write(prediction_str)
        st.write(features_dataframe)

    except Exception as e:
        print(e)
        st.error("stay safe!")

else:
    st.write("")



   
       
