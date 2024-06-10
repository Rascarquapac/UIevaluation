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

def start_message():
    st.header('Cyanview resources for shading your use-case')
    display = "Before computing the Cyanview resources required we need to get a description of your use-case by following the following steps:\n"
    display += "- your camera types and number\n"
    display += "- optional lenses you want to control\n"
    display += "- production type you plan to do\n"
    st.markdown(display)

def camera_pattern_input():
    st.subheader("Add cameras to the current pool")
    st.markdown("Enter a camera pattern to match.")
    if st.session_state.reset_camera_pattern :
        st.session_state.pattern = st.text_input("Camera pattern", label_visibility="collapsed",value="",key="camera_pattern_input").upper()
        st.session_state.reset_camera_pattern = False
    else:
        st.session_state.pattern = st.text_input("Camera pattern", label_visibility="collapsed",key="camera_pattern_input").upper()
    return (st.session_state.pattern)


def advanced():
    # Sidebar
    st.sidebar.header(("About"))
    st.sidebar.markdown((
        "[Cyanview](https://www.cyanview.com) is a company providing shading solutions for video productions."
    ))

    st.sidebar.header(("Resources"))
    st.sidebar.markdown((
        """
    - [Support Documentation](https://support.cyanview.com)
    - [Website](https://www.cyanview.com)
    - [Presentation](https://www.cyanview.com/presentation)
    - [Blog](https://www.cyanview.com/blog) (How to master Streamlit for data science)
    """
    ))

    st.sidebar.header(("Deploy"))
    st.sidebar.markdown((
        "You can quickly deploy Streamlit apps using [Streamlit Community Cloud](https://streamlit.io/cloud) in just a few clicks."
    ))
    return 

# User Interface initialisation
if 'journey' not in st.session_state:
    # Define first state
    st.session_state.journey = "cam_pattern"
    st.session_state.reset_camera_pattern = False
    # Import cyanview data set
    st.session_state.cameras = Camera()
    st.session_state.cameras.get_csv()
    # Create the step object collecting user intput of one UI step
    st.session_state.step = Camera()
    # Create the result object collecting user intput on the whole UI steps
    st.session_state.result = Camera()
    # Reset or not the camera pattern_input
    print(st.session_state.cameras.df)
    st.session_state.instance = Instances(st.session_state.cameras.df)
    st.session_state.partial_instance = Instances(st.session_state.cameras.df)
    st.session_state.final_instance = Instances(st.session_state.cameras.df)
    st.session_state.property = Properties()
    st.session_state.draw = Draw()
    st.session_state.messages = Messages()

# Tittle
st.header('Cyanview Agent Configuration V0.0')
# Expander
with st.expander("**Quoting process and motivations**"):
    st.markdown(st.session_state.messages.dic['mainUI']['expander']['about'])

advanced()



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
        st.subheader("Current Selection of Cameras")
        # display_camera_table(st.session_state.result)
        st.session_state.result.display_camera_table()
        print("Cyaneval->/State=cam_pattern: Camera table displayed")
        if st.button("Set Connections"):
            st.session_state.journey = "properties_select"
            st.session_state.instance.camera_lens_init(st.session_state.result)
            st.rerun()
    # Display camera pattern selection
    camera_pattern = camera_pattern_input()
    # Check if pattern entered
    if st.session_state.pattern:
        st.session_state.step.df = st.session_state.cameras.cameras_from_pattern(camera_pattern)
        st.markdown("Please select the camera used in your use-case and set the number of cameras")
        print(st.session_state.step.df)
        #edit_camera_table(st.session_state.step)
        st.session_state.step.edit_camera_table()
        ## Choose next states
        if st.button("Add camera selection"):
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