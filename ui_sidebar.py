import streamlit as st
from message  import Messages

def sidebar(): 
     # Sidebar
    st.sidebar.header(("Cyanview gear selection process"))
    display = "Get Cyanview gear from a use-case:\n"
    display += "1 Set cameras pool\n"
    display += "\n"
    display += "3 Get a connection scheme \n"
    display += "4 Get motivations of sele \n"
    st.sidebar.markdown((
        """
    1. Set cameras pool
    2. Set cameras environment
    3. Get the connection schema
    4. Get motivations for selection
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
