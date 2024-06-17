import csv
import pandas as pd
import streamlit as st
from property import Properties

def get_cameras(df):
    cameras = pd.read_csv("./data/CyanviewDescriptor - Cameras.csv")
    cam_df  = pd.DataFrame(cameras)
    try:
        columns = cam_df.columns[cam_df.columns.duplicated(keep=False)]
        rows = cam_df.index[cam_df.index.duplicated(keep=False)]
        if not columns.empty :
            print("Duplicated Columns :\n",columns)
            raise Exception('Duplicated Columns in CyanviewDescriptor - Cameras.csv')
        if not rows.empty :
            print("Duplicated Rows :\n",rows)
            raise Exception('Duplicated Rows in CyanviewDescriptor - Cameras.csv')
    except Exception as e:
        print(str(e))
    protocols = pd.read_csv("./data/CyanviewDescriptor - CameraProtocols.csv")
    proto_df = pd.DataFrame(protocols)
    del proto_df['Brand']
    df = pd.merge(cam_df, proto_df, on = ['Protocol'],how = 'left').set_index('Model')
    # Add missing columns
    df = df.assign(Selected=False)
    df = df.assign(Number=0)
    df = df.assign(Lens='Fixed')
    df = df.assign(Network='LAN wired')
    df = df.assign(Base='Fixed')
    ## To suppress ??
    #df['Model'] = df.index
    df.to_csv("./data/Generated_CameraDetails.csv")
    return(df)

def apply_pattern(df, camera_pattern="",brand=""):
    if camera_pattern != None and camera_pattern != "":
        camera_selection = df.filter(like=camera_pattern,axis=0)
    else:
        camera_selection = df
    if brand != None and brand != "":
        brand_query = f'Brand == "{brand}"'
        selection = camera_selection.query(brand_query)
    else:
        selection = camera_selection
    #search_pattern = f'Model.str.contains(".*{camera_pattern}") and Brand == "{brand}"'
    #selection = df.query(search_pattern)
    return (selection)

def display_camera_table(df):
    print("DEBUG:cyaneval->display_camera_table ...")
    if (len(df.index) != 0):
        st.dataframe(
            df,
            column_config={
                "Model": "Model",
                'Number':st.column_config.NumberColumn(
                    "# of Cams",
                    help="How much camera of this type in your use-case (0-15)?",
                    min_value=0,
                    max_value=15,
                    step=1,
                    format="%d",
                ),
                "Brand": "Brand",
                "Cable": "Cable",
                "SupportURL": st.column_config.LinkColumn(
                    "Support URL",
                    help = "Reference in Cyanview Support Website",
                    validate = None,
#                            display_text = "\[(.*?)\]",
                    display_text = "Support Link",
                    max_chars = 30 ),
                "ManufacturerURL": st.column_config.LinkColumn(
                    "Brand URL",
                    help = "Reference on Brand website",
                    validate = None,
#                            display_text = "\[(.*?)\]",
                    display_text = "Brand link",
                    max_chars = 30 ),
                "Reference": None,
                "Protocol":None,
                "Message":None,
                "Type":None
            },
            column_order=['Model','Number','Cable','SupportURL','ManufacturerURL'],
            hide_index = True)
        return(df)

def edit_camera_number(df):
    # Validate inputs
    if (len(df.index) != 0): 
        df = st.data_editor(
            df,
            height = 200,
            column_config={
                'Number':st.column_config.NumberColumn(
                    "# of Cams",
                    help="How much camera of this type in your use-case (0-15)?",
                    min_value=0,
                    max_value=15,
                    step=1,
                    format="%d",
                ),
                "Model": "Model",
                "Brand": "Brand",
                "Cable": "Cable",
                "SupportURL": st.column_config.LinkColumn(
                    "Support URL",
                    help = "Reference in Cyanview Support Website",
                    validate = None,
#                            display_text = "\[(.*?)\]",
                    display_text = "Support Link",
                    max_chars = 30 ),
                "ManufacturerURL": st.column_config.LinkColumn(
                    "Brand URL",
                    help = "Reference on Brand website",
                    validate = None,
#                            display_text = "\[(.*?)\]",
                    display_text = "Brand link",
                    max_chars = 30 ),
                "Reference": None,
                # "supportText": None,
                "Protocol":None,
                "Message":None,
                "Type":None
            },
            disabled=['Selected','Model','Cable','SupportURL','ManufacturerURL'],
            column_order=['Number','Model','Brand','Cable','SupportURL','ManufacturerURL'],
            hide_index = True,
            use_container_width = True,
            key = "camera_number",
#            on_change = st.rerun,
            )
        ## st.markdown(display)
        #print("\nDATAFRAME AFTER EDIT")
        #print(df)
        return(df)

def edit_camera_environment(df,key):
    # Validate inputs
    print("--------------------->CONSTRAINTS")
    print(st.session_state.property.constraints)
    print("END OF ONSTRAINTS---------------->")
    if (len(df.index) != 0): 
        df = st.data_editor(
            df,
            column_config={
                    "Type": "Type",
                    "Model": "Model",
                    'Number':st.column_config.NumberColumn(
                        "# Cams",
                        help="How much camera of this type in your use-case (0-15)?",
                        min_value=0,
                        max_value=15,
                        step=1,
                        default=0,
                        format="%d",
                    ),
                    'Lens': st.column_config.SelectboxColumn(
                        "Lens",
                        help="Lens type",
                        width="medium",
                        options= st.session_state.property.constraints[(key,'Lens')],
                        required=True),
                    'Network':  st.column_config.SelectboxColumn(
                        "Network",
                        help="Select the network type",
                        width="medium",
                        options=st.session_state.property.constraints[(key,'Network')],
                        required=True),
                    'Base':  st.column_config.SelectboxColumn(
                        "Basement",
                        help="Base type",
                        width="medium",
                        options=st.session_state.property.constraints[(key,'Base')],
                        required=True),
                "Brand": "Brand",
                "Cable": "Cable",
                "SupportURL": st.column_config.LinkColumn(
                    "Support URL",
                    help = "Reference in Cyanview Support Website",
                    validate = None,
#                            display_text = "\[(.*?)\]",
                    display_text = "Support Link",
                    max_chars = 30 ),
                "ManufacturerURL": st.column_config.LinkColumn(
                    "Brand URL",
                    help = "Reference on Brand website",
                    validate = None,
#                            display_text = "\[(.*?)\]",
                    display_text = "Brand link",
                    max_chars = 30 ),
                "Reference": None,
                # "supportText": None,
                "Message":None,
            },
            disabled=['Selected','Model','Cable','SupportURL','ManufacturerURL'],
            column_order=['Type','Number','Model','Network','Lens','Base'],
            hide_index = True,
            use_container_width = True,
            key = key,
#            on_change = st.rerun,
            )
        ## st.markdown(display)
        #print("\nDATAFRAME AFTER EDIT")
        #print(df)
        return(df)


if __name__  == "__main__":
    reader = pd.DataFrame().pipe(get_cameras).pipe(apply_pattern,"CV","")
    #result = reader.pipe(get_cameras).pipe(apply_pattern,"CV","")
    print("RESULT:\n")
    print(reader)
