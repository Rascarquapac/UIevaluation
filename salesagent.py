import streamlit as st
import pandas as pd
import glob 
import re

from camera import get_cameras,apply_pattern,display_camera_table,edit_camera_number, edit_camera_network,edit_camera_lens
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
    st.session_state.done = False
    st.session_state.code ="""
graph TD
    A --> B
"""
    print("----> UI_INIT function EXECUTED")


# User Interface initialisation
if 'journey' not in st.session_state:
    ui_init()
# Set title
st.header('Cyanview Gear Selector V0.0')
# not available in streamlit 1.34 … st.logo("data/cyanview_logo_temp.png")
# Set sidebar
sidebar()
# Set tabs
cameraSelection, networkSelection,lensSelection, motivations, mermaid,graphviz, test = st.tabs(["Cameras","Network" ,"Lens","Motivations", "Mermaid","Graphviz","TEST"])
# Tab1 : cameras selection
with cameraSelection :
    st.subheader("Setup Camera Pool")
    col1, col2 = st.columns([0.5,0.5])
    with col1:
        brand = st.selectbox("Select Brand:",st.session_state.brands,index=None,placeholder="Choose an option",key="brand_selector",on_change=update_selecting)
    with col2:
        camera_pattern = st.text_input(label="Camera Pattern:", value="",key="camera_pattern",placeholder="Enter substring of camera name",on_change=update_selecting).upper()
    selection = edit_camera_number(st.session_state.selecting)
    st.divider()
    st.caption("Your current cameras pool selection")
    print("DUPLICATED:")
    print(f"Duplicated in session_state.base: {st.session_state.base.index[st.session_state.base.index.duplicated()]}")
    if isinstance(selection, pd.DataFrame):
        print(f"Duplicated in selection: {selection.index[selection.index.duplicated()]}")
    st.session_state.base.update(selection)
    st.session_state.selected = st.session_state.base[(st.session_state.base['Number'] > 0)]
    st.session_state.selected.style.set_properties(**{'background_color': 'lightgreen'})
    display_camera_table(st.session_state.selected)
    with st.expander("More Info",expanded=False):
        message = st.session_state.messages.cameras(st.session_state.selected)
        st.write(message)

with networkSelection:
    if not st.session_state.selected.empty :
        st.subheader('Select networks (optional):')
        blocks = {}
        for camera_type in st.session_state.property.cameraTypes:
            #filter instance dataframe by type
            selected_rows = st.session_state.selected.loc[st.session_state.selected['Type'] == camera_type]
            if not selected_rows.empty :
                blocks[camera_type] = edit_camera_network(selected_rows,key=camera_type)
        print("INSTANCE DES CAMERASxLENSxNETWORKxBASE APRES EDITION")
        print("Camera types :",st.session_state.property.cameraTypes)
        print("Blocks: ",blocks)
        st.session_state.final = pd.concat(list(blocks.values()))
    if st.button("Analyze",key="networkanalysis"):
#        st.session_state.instance.debug_camerapool_to_csv(st.session_state.final) # DEBUG only
         st.session_state.instance.setup(st.session_state.final)        
         st.session_state.instance.analyze()
         st.session_state.done = True
with lensSelection:
    if not st.session_state.selected.empty :
        st.subheader('Select Lens (optional):')
        blocks = {}
        for camera_type in st.session_state.property.cameraTypes:
            #filter instance dataframe by type
            selected_rows = st.session_state.selected.loc[st.session_state.selected['Type'] == camera_type]
            if not selected_rows.empty :
                blocks[camera_type] = edit_camera_lens(selected_rows,key=camera_type)
        print("INSTANCE DES CAMERASxLENSxNETWORKxBASE APRES EDITION")
        print("Camera types :",st.session_state.property.cameraTypes)
        print("Blocks: ",blocks)
        st.session_state.final = pd.concat(list(blocks.values()))
    if st.button("Analyze",key="lensanalysis"):
#        st.session_state.instance.debug_camerapool_to_csv(st.session_state.final) # DEBUG only
         st.session_state.instance.setup(st.session_state.final)        
         st.session_state.instance.analyze()
         st.session_state.done = True

with motivations:
    if st.button("Motivation"):
        st.rerun()
with graphviz:
    if st.session_state.done:
        # GRAPHVIZ RENDERING
        st.write(st.session_state.instance.draw_all())
with mermaid:
    if st.session_state.done:
        # MERMAID RENDERING
        svg_code = st.session_state.instance.get_mermaid_code()
        mermaid_graph=st.session_state.instance.graph_mermaid(svg_code)
        html = st.session_state.instance.streamlit_mermaid(mermaid_graph)
        st.write(html, unsafe_allow_html=True)

with test:
    # if st.session_state.done:
        # code = st.session_state.instance.get_mermaid_code()
        # svg_code = st.session_state.instance.get_mermaid_code()
    svg_code = None
    mermaid_graph=st.session_state.instance.graph_mermaid(svg_code)
    html = st.session_state.instance.streamlit_mermaid(mermaid_graph)
    st.write(html, unsafe_allow_html=True)
        # mermaid = stmd.st_mermaid(st.session_state.code)
        # st.write(mermaid)
    # Create a connection object.
    # conn = st.connection("gsheets", type=GSheetsConnection)
    # df = conn.read(
    #     worksheet="Cameras",
    #     ttl=0, #ttl="10m",
    #     usecols=[0, 1],
    #     nrows=3,
    # )