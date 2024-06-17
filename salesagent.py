import streamlit as st
import pandas as pd
import glob 
import re

from camera import get_cameras,apply_pattern,display_camera_table,edit_camera_number, edit_camera_environment
from instance import Instances
from property import Properties
from message  import Messages
from draw     import Draw
from ui_sidebar import sidebar

def update_selecting():
    if "brand_selector" not in st.session_state:
        st.session_state.selecting = st.session_state.base.pipe(apply_pattern,st.session_state.camera_pattern.upper())    
    else:
        st.session_state.selecting = st.session_state.base.pipe(apply_pattern,st.session_state.camera_pattern.upper(),st.session_state.brand_selector)    

def ui_init():
    # Define first state
    st.session_state.journey = "cam_pattern"
    # Import full camera data
    st.session_state.base      = pd.DataFrame().pipe(get_cameras)
    st.session_state.selecting = pd.DataFrame()
    st.session_state.selected  = pd.DataFrame()
    st.session_state.final     = pd.DataFrame()
    st.session_state.brands = st.session_state.base["Brand"].unique()
    # Initiate empty camera instances 
    st.session_state.instance = Instances()
#    st.session_state.instance_selecting = Instances(st.session_state.camera_base.df)
#    st.session_state.instance_selected = Instances(st.session_state.camera_base.df)
    # Get Properties and Messages from Cyanview data
    st.session_state.property = Properties()
    st.session_state.messages = Messages()
    # Initiate drawings
    st.session_state.draw = Draw()
    print("----> UI_INIT function EXECUTED")


# User Interface initialisation
if 'journey' not in st.session_state:
    ui_init()
# Set title
st.header('Cyanview Gear Selector V0.0')
st.logo("data/cyanview_logo_temp.png")
# Set sidebar
sidebar()
# Set tabs
cameraSelection, environmentSelection, tab3, tab4 = st.tabs(["Select Cameras","Select Environment" ,"Motivation", "Schema"])
# Tab1 : cameras selection
with cameraSelection :
    st.subheader("Setup Camera Pool")
    col1, col2 = st.columns([0.5,0.5])
    with col1:
        camera_pattern = st.text_input(label="Camera Pattern:", value="",key="camera_pattern",placeholder="Enter substring of camera name",on_change=update_selecting).upper()
    with col2:
        brand = st.selectbox("Select Brand:",st.session_state.brands,index=None,placeholder="Choose an option",key="brand_selector",on_change=update_selecting)
    selection = edit_camera_number(st.session_state.selecting)
    st.divider()
    st.subheader("Current Camera Pool")
    print("DUPLICATED:")
    print(f"Duplicated in session_state.base: {st.session_state.base.index[st.session_state.base.index.duplicated()]}")
    if isinstance(selection, pd.DataFrame):
        print(f"Duplicated in selection: {selection.index[selection.index.duplicated()]}")
    
    st.session_state.base.update(selection)
    st.session_state.selected = st.session_state.base[(st.session_state.base['Number'] > 0)]
    display_camera_table(st.session_state.selected)

with environmentSelection:
    if not st.session_state.selected.empty :
        st.subheader('Select Network and Lens Types:')
        blocks = {}
        for camera_type in st.session_state.property.cameraTypes:
            #filter instance dataframe by type
            selected_rows = st.session_state.selected.loc[st.session_state.selected['Type'] == camera_type]
            if not selected_rows.empty :
                blocks[camera_type] = edit_camera_environment(selected_rows,key=camera_type)
        #print("INSTANCE DES CAMERASxLENSxNETWORKxBASE APRES EDITION")
        st.session_state.final = pd.concat(list(blocks.values()))
    if st.button("Analyze"):
        pass
#        st.session_state.instance.debug_camerapool_to_csv(st.session_state.final) # DEBUG only
#        st.session_state.instance.create(st.session_state.final)
#        st.session_state.instance.analyze()

with tab3:
    if st.button("Motivation"):
        st.rerun()
    st.session_state.draw.mermaid()

with tab4:
    if st.button("Display Schematic"):
        st.rerun()
