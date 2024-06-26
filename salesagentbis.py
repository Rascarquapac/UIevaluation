import streamlit as st
import pandas as pd
import glob 
import re

from pool import Pool
from instance import Instances
from property import Properties
from message  import Messages
from draw     import Draw
from ui_sidebar import sidebar

# Set pool.step_match from user input… should be a Pool method
def update_selecting():
    pattern = st.session_state.camera_pattern.upper()
    if "brand_selector" not in st.session_state:
        st.session_state.pool.apply_pattern(pattern)
    else:
        brand = st.session_state.brand_selector
        st.session_state.pool.apply_pattern(pattern,brand)
    return
def ui_init():
    # Define first state
    st.session_state.running = True
    # Import full camera data
    st.session_state.pool     = Pool()
    st.session_state.instance = Instances()
    st.session_state.property = Properties()
    st.session_state.messages = Messages()
    # Initiate drawings
    st.session_state.analyze_done = False

# User Interface initialisation
if 'running' not in st.session_state:
    ui_init()
# Set title
st.header('Cyanview Gear Selector V0.0')
# not available in streamlit 1.34 … st.logo("data/cyanview_logo_temp.png")
# Set sidebar
sidebar()
# Set tabs
cameraSelection, networkSelection,lensSelection, motivations, mermaid,graphviz, test = st.tabs(["Cameras","Network" ,"Lens","Motivations", "Mermaid","Graphviz","TEST"])
with cameraSelection :
    st.subheader("Setup Camera Pool")
    col1, col2 = st.columns([0.5,0.5])
    with col1:
        brand = st.selectbox("Select Brand:",st.session_state.pool.brands,index=None,placeholder="Choose an option",key="brand_selector",on_change=update_selecting)
    with col2:
        camera_pattern = st.text_input(label="Camera Pattern:", value="",key="camera_pattern",placeholder="Enter substring of camera name",on_change=update_selecting).upper()
    # set pool.step_select from pool.step_match 
    st.session_state.pool.edit_camera_number()
    st.divider()
    st.caption("Your Current Cameras Pool")
    st.session_state.pool.display_selected()
    with st.expander("More info about selected cameras",expanded=False):
        message = st.session_state.messages.display(object=st.session_state.pool)
        st.write(message)

with networkSelection:
    if not st.session_state.pool.selected.empty :
        st.subheader('Select networks (optional):')
        st.session_state.pool.edit_camera_per_type('network')
        with st.expander("More Info about selection",expanded=False):
            message = st.session_state.messages.display(object=st.session_state.instance, subtopic="")
            st.write(message)

    if st.button("Analyze",key="networkanalysis"):
#        st.session_state.instance.debug_camerapool_to_csv(st.session_state.final) # DEBUG only
         st.session_state.instance.setup(st.session_state.pool.final)        
         st.session_state.instance.analyze()
         st.session_state.analyze_done = True
with lensSelection:
    if not st.session_state.pool.selected.empty :
        st.subheader('Select Lens (optional):')
        st.session_state.pool.edit_camera_per_type('lens')
    if st.button("Analyze",key="lensanalysis"):
#        st.session_state.instance.debug_camerapool_to_csv(st.session_state.final) # DEBUG only
         st.session_state.instance.setup(st.session_state.pool.final)        
         st.session_state.instance.analyze()
         st.session_state.analyze_done = True

with motivations:
    if st.button("Motivation"):
        st.rerun()
with graphviz:
    if st.session_state.analyze_done:
        # GRAPHVIZ RENDERING
        st.write(st.session_state.instance.draw_all())
with mermaid:
    if st.session_state.analyze_done:
        # MERMAID RENDERING
        svg_code = st.session_state.instance.get_mermaid_code()
        mermaid_graph=st.session_state.instance.graph_mermaid(svg_code)
        html = st.session_state.instance.streamlit_mermaid(mermaid_graph)
        st.write(html, unsafe_allow_html=True)

with test:
    # if st.session_state.analyze_done:
        # code = st.session_state.instance.get_mermaid_code()
        # svg_code = st.session_state.instance.get_mermaid_code()
    svg_code = None
    mermaid_graph=st.session_state.instance.graph_mermaid(svg_code)
    html = st.session_state.instance.streamlit_mermaid(mermaid_graph)
    st.write(html, unsafe_allow_html=True)