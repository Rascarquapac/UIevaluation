import streamlit as st
import pandas as pd
import glob 
import re


# from camera import Cameras
from camera   import Camera
from instance import Instances
from instance import Properties
from analyze  import Analyze
from message  import Messages
from draw     import Draw
from ui_sidebar import sidebar

def ui_init():
    # Define first state
    st.session_state.journey = "cam_pattern"
    # Import full camera data
    st.session_state.camera_base = Camera()
    st.session_state.camera_base.get_csv()
    # Initiate empty camera sets for active selection ("selecting") and the selected ("selected")
    st.session_state.camera_selecting = Camera()
    st.session_state.camera_selected = Camera()
    # Initiate empty camera instances 
    st.session_state.instance = Instances(st.session_state.camera_base.df)
    st.session_state.instance_selecting = Instances(st.session_state.camera_base.df)
    st.session_state.instance_selected = Instances(st.session_state.camera_base.df)
    # Get Properties and Messages from Cyanview data
    st.session_state.property = Properties()
    st.session_state.messages = Messages()
    # Initiate drawings
    st.session_state.draw = Draw()

def camera_pattern_input():
    st.session_state.pattern = st.text_input(label="Camera Pattern:", value="",key="camera_pattern_input",placeholder="Enter substring of camera name").upper()
    return (st.session_state.pattern)


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
    col1, col2 = st.columns([0.5,0.5])
    with col1:
        if st.session_state.journey == "cam_pattern":
            camera_pattern = camera_pattern_input()
    with col2:
        if st.session_state.journey == "cam_pattern":
            brands= st.session_state.camera_base.df["Brand"].unique()
            print(brands)
            st.session_state.brand = st.selectbox("Select Brand:",brands,index=None,placeholder="Choose an option")
            brand = st.session_state.brand

    # User Interface : collect regular expression for camera matching
    if st.session_state.journey == "cam_pattern":
        # Display current camera selection if thre is one
        if len(st.session_state.camera_selected.df.index) != 0 :
            st.subheader("Current Selection of Cameras")
            # display_camera_table(st.session_state.camera_selected)
            st.session_state.camera_selected.display_camera_table()
            print("Cyaneval->/State=cam_pattern: Camera table displayed")
            if st.button("Set Connections"):
                st.session_state.journey = "properties_select"
                st.session_state.instance.camera_lens_init(st.session_state.camera_selected)
                st.rerun()
        # Check if pattern entered
        if st.session_state.pattern or st.session_state.brand :
            st.session_state.camera_selecting.df = st.session_state.camera_base.cameras_from_pattern(camera_pattern,brand)
            st.markdown("Please select the camera used in your use-case and set the number of cameras")
            print(st.session_state.camera_selecting.df)
            #edit_camera_table(st.session_state.camera_selecting)
            st.session_state.camera_selecting.edit_camera_table()
            ## Choose next states
            st.divider()
            if st.button("Add camera selection"):
                st.session_state.camera_selected.merge(st.session_state.camera_selecting,None)
                print("DEBUG: merge result: ")
                print(st.session_state.camera_selected.df)
                #display_camera_table(st.session_state.camera_selected)
                st.session_state.camera_selected.display_camera_table()
                st.rerun()
    elif st.session_state.journey == "properties_select":
        print("STREAMLITE STATE = properties_select")
        st.subheader('Selecting Properties for the cameras instances:')
        blocks = {}
        print("INSTANCE DES CAMERASxLENSxNETWORKxBASE AVANT EDITION")
        print(st.session_state.instance.df)
        for camera_type in st.session_state.property.cameraTypes:
            #filter instance dataframe by type
            selected_rows = st.session_state.instance.df.loc[st.session_state.instance.df['Type'] == camera_type]
            if not selected_rows.empty :
                st.session_state.instance_selecting.df = selected_rows 
                #display_camera_table(st.session_state.camera_selected)
                blocks[camera_type] = st.session_state.instance_selecting.edit_camera_table(key=camera_type)
        print("INSTANCE DES CAMERASxLENSxNETWORKxBASE APRES EDITION")
        print(st.session_state.instance_selected.merge(blocks))

        if st.button("Analyze the Use-case"):
            st.session_state.journey = "analyzing"
            st.rerun()
    elif st.session_state.journey == "analyzing":
        print("STREAMLITE STATE = analyzing")
        st.subheader('Analysis')
        analyze = Analyze(st.session_state.instance.df)
        st.subheader('Schematic')
        print("MERMAID CODE:",st.session_state.draw.test())
        st.session_state.draw.mermaid()

        if st.button("Go To Start"):
            st.session_state.journey = "cam_pattern"
            st.rerun()
    else:
        pass
with environmentSelection:
    st.subheader('Analysis')
    analyze = Analyze(st.session_state.instance.df)    

with tab3:
    if st.button("Motivation"):
        st.rerun()
    st.session_state.draw.mermaid()

with tab4:
    if st.button("Display Schematic"):
        st.rerun()
