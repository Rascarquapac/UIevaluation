from pprint import pprint
import pandas as pd
import streamlit as st
from streamlit_gsheets import GSheetsConnection
# Create a connection object
conn = st.connection("gsheets", type=GSheetsConnection)
# Read data from the Google Sheet
cam_df = conn.read(usecols=['Model','Reference','Protocol','Brand','ManufacturerURL','Remark',"CameraLensControl","LensMount"])
# Display the data
#st.dataframe(df)
pprint(cam_df)
# Create a connection object
conn = st.connection("protocols", type=GSheetsConnection)
# Read data from the Google Sheet
proto_df = conn.read(usecols=["Protocol","Brand","Type","Cable","SupportURL","Message",
                 "MaxDelayToComplete","ControlCoverage","Bidirectionnal"])
pprint(proto_df)
del proto_df['Brand']
pool_df = pd.merge(cam_df, proto_df, on = ['Protocol'],how = 'left').set_index('Model')
# Add missing columns
pool_df = pool_df.assign(Selected=False)
pool_df = pool_df.assign(Number=0)
pool_df = pool_df.assign(Lens='Fixed')
pool_df = pool_df.assign(Network='LAN Wired')
pool_df = pool_df.assign(Base='Fixed')
# Lens Properties
# pool_df = pool_df.assign(CameraLensSpecificity  = "TBD")
# pool_df = pool_df.assign(LensControlNeeds = "Nopip ineeds")
# pool_df = pool_df.assign(UserLensSpecificity  = "TBD")
# pool_df = pool_df.assign(LensMotorization = "TBD")	
# TODO : should assign values per camera group based on properties to get adhoc default

## To suppress ??
#df['Model'] = df.index
pool_df.to_csv("./picklized/Generated_CameraDetails.csv")

