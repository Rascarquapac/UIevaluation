import streamlit as st
import pandas as pd
from usecase.main import Usecase
from streamui import StreamUI
from pool     import Pool
from property import Properties
from message  import Messages

debug_pool_record = True
debug_pool_load   = True

# Set pool.step_match from user input… should be a Pool method
def update_selecting():
    pattern = st.session_state.camera_pattern.upper()
    if "brand_selector" not in st.session_state:
        st.session_state.pool.apply_pattern(pattern)
    else:
        brand = st.session_state.brand_selector
        st.session_state.pool.apply_pattern(pattern,brand)
    return
def sidebar(): 
     # Sidebar
    st.sidebar.header(("Workflow"))
    st.sidebar.markdown((
        """
    1. Set **Cameras** pool
    2. Set **IP Network** mediums
    3. Set **Lenses**
    4. **Refine** your use-case
    """))
    st.sidebar.header(("Outputs"))
    st.sidebar.markdown((
        """
    1. **Schema** of use-case, 
    2. List of equipment for quote
    3. Tips, attention points, explanations
    """
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

    st.sidebar.header(("About Cyanview"))
    st.sidebar.markdown((
        "[Cyanview](https://www.cyanview.com) is a company providing shading solutions for video productions."
    ))
    return 

def ui_init():
    # Define first state
    st.session_state.running = True
    # Import full camera data
    st.session_state.pool     = Pool()
    if debug_pool_load :
        st.session_state.pool.df = pd.read_pickle("./debug/debug_pool_df_init.pkl")
    st.session_state.usecase  = Usecase()
    st.session_state.property = Properties()
    st.session_state.messages = Messages()
    st.session_state.streamui = StreamUI()
    # Initiate drawings
    st.session_state.analyze_done = False

# User Interface initialisation
if 'running' not in st.session_state:
    ui_init()
# Set title
st.header('Cyanview Gear Simulator V0.0')
# not available in streamlit 1.34 … 
st.logo("images/logo.jpg")
# Set sidebar
sidebar()
# Set tabs
cameraSelection, networkSelection,lensSelection, motivations, mermaid,graphviz, test = st.tabs(["Cameras","IP Network" ,"Lens","Motivations", "Mermaid","Graphviz","TEST"])
with cameraSelection :
    st.subheader("Setup Camera Pool")
    col1, col2 = st.columns([0.5,0.5])
    with col1:
        brand = st.selectbox("Select Brand:",st.session_state.pool.brands,index=None,placeholder="Choose an option",key="brand_selector",on_change=update_selecting)
    with col2:
        camera_pattern = st.text_input(label="Camera Pattern:", value="",key="camera_pattern",placeholder="Enter substring of camera name",on_change=update_selecting).upper()
    # set pool.step_select from pool.step_match 
    ##test refacoring streamui ## st.session_state.pool.edit_camera_number()
    st.session_state.pool.pool_edit_camera_number(st.session_state.pool)
    st.divider()
    st.caption("Your Current Cameras Pool")
    ##test refacoring streamui ##  st.session_state.pool.display_selected()
    st.session_state.pool.pool_display_selected(st.session_state.pool)
    with st.expander("More info about selected cameras",expanded=False):
        message = st.session_state.messages.display(object=st.session_state.pool)
        st.write(message)

with networkSelection:
    if not st.session_state.pool.selected.empty :
        st.subheader('Select networks (optional):')
        ##test refacoring streamui ## st.session_state.pool.edit_camera_per_type('network')
        st.session_state.pool.pool_edit_camera_for_network(st.session_state.pool)
#    if st.button("Analyze",key="networkanalysis"):
#        st.session_state.usecase.debug_camerapool_to_csv(st.session_state.final) # DEBUG only
        if debug_pool_record :
            st.session_state.pool.df.to_pickle("./debug/debug_pool_df.pkl")
        print("salesagent->networkSelection->st.session_state.POOL.FINAL columns:\n",st.session_state.pool.final.columns)
        st.session_state.usecase.analyze(st.session_state.pool.final)
        if debug_pool_record :
            st.session_state.pool.final.to_pickle("./debug/debug_pool_df_final.pkl")
        st.session_state.analyze_done = True
        with st.expander("Required equipment for use case",expanded=False):
            message = st.session_state.messages.display(object=st.session_state.usecase)
            st.write(message)

with lensSelection:
    if not st.session_state.pool.selected.empty :
        st.subheader('Select Lens (optional):')
        ##test refacoring streamui ##  st.session_state.pool.edit_camera_per_type('lens')
        st.session_state.streamui.pool_edit_camera_for_lens(st.session_state.pool)
#    if st.button("Analyze",key="lensanalysis"):
#        st.session_state.usecase.debug_camerapool_to_csv(st.session_state.final) # DEBUG only
        if debug_pool_record :
            st.session_state.pool.df.to_pickle("./debug/debug_pool_df.pkl")
        st.session_state.usecase.analyze(st.session_state.pool.final)
        if debug_pool_record :
            st.session_state.pool.final.to_pickle("./debug/debug_pool_df_final.pkl")
        st.session_state.analyze_done = True

with motivations:
    if st.button("Motivation"):
        st.rerun()
with graphviz:
    if st.session_state.analyze_done:
        # GRAPHVIZ RENDERING
        st.write(st.session_state.usecase.draw_all())
with mermaid:
    if st.session_state.analyze_done:
        # MERMAID RENDERING
        svg_code = st.session_state.usecase.get_mermaid_code()
        mermaid_graph=st.session_state.usecase.graph_mermaid(svg_code)
        html = st.session_state.usecase.streamlit_mermaid(mermaid_graph)
        st.write(html, unsafe_allow_html=True)
with test:
    # if st.session_state.analyze_done:
        # code = st.session_state.usecase.get_mermaid_code()
        # svg_code = st.session_state.usecase.get_mermaid_code()
    svg_code = None
    mermaid_graph=st.session_state.usecase.graph_mermaid(svg_code)
    html = st.session_state.usecase.streamlit_mermaid(mermaid_graph)
    st.write(html, unsafe_allow_html=True)
