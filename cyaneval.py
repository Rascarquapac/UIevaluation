import streamlit as st
import pandas as pd
import glob 
import re

# from camera import Cameras
from descriptor import Descriptor
from instance import Instances
from instance import Properties

def start_message():
    st.subheader('Cyanview resources for shading your use-case')
    display = "Before computing the Cyanview resources required we need to get a description of your use-case by following the following steps:\n"
    display += "- your camera types and number\n"
    display += "- optional lenses you want to control\n"
    display += "- production type you plan to do\n"
    st.markdown(display)

def camera_pattern_input():
    st.markdown("Please provide a text pattern describing your camera.")
    if st.session_state.reset_camera_pattern :
        st.session_state.pattern = st.text_input("Camera pattern", label_visibility="collapsed",value="",key="camera_pattern_input").upper()
        st.session_state.reset_camera_pattern = False
    else:
        st.session_state.pattern = st.text_input("Camera pattern", label_visibility="collapsed",key="camera_pattern_input").upper()
    return (st.session_state.pattern)

def advanced():
    with st.expander(("About the #30DaysOfStreamlit")):
        st.markdown((
            """
        The **#30DaysOfStreamlit** is a coding challenge designed to help you get started in building Streamlit apps.
        
        Particularly, you'll be able to:
        - Set up a coding environment for building Streamlit apps
        - Build your first Streamlit app
        - Learn about all the awesome input/output widgets to use for your Streamlit app
        """
        ))

    # Sidebar
    st.sidebar.header(("About"))
    st.sidebar.markdown((
        "[Streamlit](https://streamlit.io) is a Python library that allows the creation of interactive, data-driven web applications in Python."
    ))

    st.sidebar.header(("Resources"))
    st.sidebar.markdown((
        """
    - [Streamlit Documentation](https://docs.streamlit.io/)
    - [Cheat sheet](https://docs.streamlit.io/library/cheatsheet)
    - [Book](https://www.amazon.com/dp/180056550X) (Getting Started with Streamlit for Data Science)
    - [Blog](https://blog.streamlit.io/how-to-master-streamlit-for-data-science/) (How to master Streamlit for data science)
    """
    ))

    st.sidebar.header(("Deploy"))
    st.sidebar.markdown((
        "You can quickly deploy Streamlit apps using [Streamlit Community Cloud](https://streamlit.io/cloud) in just a few clicks."
    ))
    return 

advanced()


# User Interface initialisation
if 'journey' not in st.session_state:
    # Define first state
    st.session_state.journey = "start"
    # Import the data set
    st.session_state.db = Descriptor()
    st.session_state.db.get_csv()
    #st.session_state.db = Cameras()
    #st.session_state.db.camera_init()
    # Create the result object collecting user intput on the whole UI steps
    st.session_state.result = Descriptor()
    # Create the step object collecting user intput of one UI steps
    st.session_state.step = Descriptor()
    # Reset or not the camera pattern_input
    st.session_state.reset_camera_pattern = False
    print(st.session_state.db.df)
    st.session_state.instance = Instances(st.session_state.db.df)
    st.session_state.partial_instance = Instances(st.session_state.db.df)
    st.session_state.final_instance = Instances(st.session_state.db.df)
    st.session_state.property = Properties()
# User Inferface : initial state
if st.session_state.journey == "start":
    print("STREAMLITE STATE = start")
    reset_pattern = False
    start_message()
    if st.button("Start"):
        st.session_state.journey = "cam_pattern"
        st.rerun()
# User Interface : collect regular expression for camera matching
elif st.session_state.journey == "cam_pattern":
    print("STREAMLITE STATE = cam_pattern")
    # Display current camera selection if thre is one
    if len(st.session_state.result.df.index) != 0 :
        # display_camera_table(st.session_state.result)
        st.session_state.result.display_camera_table()
        print("Cyaneval->/State=cam_pattern: Camera table displayed")
        if st.button("Go to Properties Selector"):
            st.session_state.journey = "properties_select"
            st.session_state.instance.camera_lens_init(st.session_state.result)
            st.rerun()
    # Display camera pattern selection
    camera_pattern = camera_pattern_input()
    # Check if pattern entered
    if st.session_state.pattern:
        st.session_state.step.df = st.session_state.db.get_cameras(camera_pattern)
        st.markdown("Please select the camera used in your use-case and set the number of cameras")
        print(st.session_state.step.df)
        #edit_camera_table(st.session_state.step)
        st.session_state.step.edit_camera_table()
        ## Choose next states
        if st.button("Continue Camera Setup"):
            st.session_state.reset_camera_pattern = True
            st.session_state.result.merge(st.session_state.step,None)
            print("DEBUG: merge result: ")
            print(st.session_state.result.df)
            #display_camera_table(st.session_state.result)
            st.session_state.result.display_camera_table()
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
            st.session_state.partial_instance.df = selected_rows 
            #display_camera_table(st.session_state.result)
            blocks[camera_type] = st.session_state.partial_instance.edit_camera_table(key=camera_type)
    print("INSTANCE DES CAMERASxLENSxNETWORKxBASE APRES EDITION")
    print(st.session_state.final_instance.merge(blocks))
    if st.button("Go To Next cameras type"):
        st.session_state.journey = "network_select"
        st.rerun()
elif st.session_state.journey == "network_select":
    print("STREAMLITE STATE = network_select")
    st.subheader('Selecting Network')
    if st.button("Go To Start"):
        st.session_state.journey = "cam_pattern"
        st.rerun()
else:
    pass