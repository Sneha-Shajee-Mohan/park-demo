import os
import pickle
import streamlit as st
from dotenv import load_dotenv
from utils.b2 import B2
import matplotlib.pyplot as plt



# ------------------------------------------------------
#                      APP CONSTANTS
# ------------------------------------------------------
REMOTE_DATA = 'NPS.ipynbnational_parks.csv'


# ------------------------------------------------------
#                        CONFIG
# ------------------------------------------------------
load_dotenv()

# load Backblaze connection
b2 = B2(endpoint=os.environ['B2_ENDPOINT'],
        key_id=os.environ['B2_KEYID'],
        secret_key=os.environ['B2_APPKEY'])

# ------------------------------------------------------
#                        CACHING
# ------------------------------------------------------
@st.cache_data
def get_data():
#     # collect data frame of reviews and their sentiment
    b2.set_bucket(os.environ['B2_BUCKETNAME'])
    df = b2.get_df(REMOTE_DATA)
    
    return df



# ------------------------------------------------------
#                         APP
# ------------------------------------------------------
# ------------------------------
# PART 0 : Overview
# ------------------------------
st.title('National Parks Data')
st.subheader('Distribution of Parks by States')

st.subheader('This is a view of a subset of National park data ')
df_park = get_data()
st.write(df_park.sample(5))


st.subheader(' Visualization of park distribution across different states ')
state_counts = df_park['address_stateCode'].value_counts()
# st.bar_chart(state_counts)


plt.figure(figsize=(30,30 ))
st.set_option('deprecation.showPyplotGlobalUse', False)
plt.bar(state_counts.index, state_counts.values)
plt.xlabel('State',fontsize=25)
plt.ylabel('Number of National Parks',fontsize=25)
plt.title('Distribution of National Parks across Different States',fontsize=35)
plt.xticks(fontsize=18)
st.pyplot()

