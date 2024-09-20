import csv
import pandas as pd
import streamlit as st
from property import Properties
from cyancameralens import Lens
class Pool:
    def __init__(self) -> None:
        # self.df contains all camera lines with the number of camera selected (0 to …) 
        self.df     = pd.DataFrame()
        # self.step_match contains all the cameras from self.df matching a brand and a name pattern during a selection step
        self.step_match  = pd.DataFrame()
        # self.step_select contains the cameras selected by the user for the current selection step
        self.step_select = pd.DataFrame()
        # self.selected contains the full set of cameras selected by the user 
        self.selected  = pd.DataFrame()
        # the set of cameras selected splitted by blocks of cameras of the same type
        self.blocks  = {}
        self.final  = pd.DataFrame()
        self.pkl_cameras()
        self.add_lens_columns()
        print("POOL COLUMNS:",self.df.columns)
        #self.get_cameras()
        self.brands = self.df["Brand"].unique()

    def pkl_cameras(self):
        self.df = pd.read_pickle("./picklized/cameras.pkl")
        return
    def add_lens_columns(self):
        lens = Lens()
        def lensCategory(row):
            return lens.get_cameraLensCategory(row["Type"],row["LensMount"])
        self.df["CameraLensCategory"] = self.df.apply(lensCategory,axis=1)
        def user_lensControl(row):
            return lens.cameraLensInit(row["CameraLensCategory"])[0]
        def user_lensType(row):
            return lens.cameraLensInit(row["CameraLensCategory"])[1]
        def user_lensMotor(row):
            return lens.cameraLensInit(row["CameraLensCategory"])[2]
        self.df["lensControl"]= self.df.apply(user_lensControl,axis=1)
        self.df["lensType"]   = self.df.apply(user_lensType,axis=1)
        self.df["lensMotor"]  = self.df.apply(user_lensMotor,axis=1)
    # Select a camera list from pattern included in camera name, or its brand or its type
    def apply_pattern(self,camera_pattern="",brand="",camera_type=""):
        if camera_pattern != None and camera_pattern != "":
            pattern_selection = self.df.filter(like=camera_pattern,axis=0)
        else:
            pattern_selection = self.df
        if brand != None and brand != "":
            brand_query = f'Brand == "{brand}"'
            brand_selection = pattern_selection.query(brand_query)
        else:
            brand_selection = pattern_selection
        if camera_type != None and camera_type != "":
            brand_query = f'Type == "{camera_type}"'
            match = brand_selection.query(brand_query)
        else:
            match = brand_selection
        self.step_match = match
        # print('############ NEW SEARCH ###############')
        # print(self.df)
        # print(f'Search based on brand({brand}) and pattern ({camera_pattern})')
        # print(match)
        return 
    # User Interface for setting  cameras number
    def pool_edit_camera_number(self,pool):
        # Validate inputs
        if (len(pool.step_match.index) != 0): 
            pool.step_select = st.data_editor(
                pool.step_match,
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
                    "Reference": "Model",
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
                    # "Reference": None,
                    # "supportText": None,
                    "Protocol":None,
                    "Message":None,
                    "Type":None
                },
                disabled=['Selected','Reference','Cable','SupportURL','ManufacturerURL'],
                column_order=['Number','Reference','Brand','Cable','SupportURL','ManufacturerURL'],
                hide_index = True,
                use_container_width = True,
                key = "camera_number",
    #            on_change = st.rerun,
                )
            return(pool.step_select)
    # Displaying the result of the camera selection
    def pool_display_selected(self,pool):
        # Update the camera pool Dataframe with the number of camera selected on this step
        pool.df.update(pool.step_select)
        # Set the set of selected cameras
        pool.selected = pool.df[(pool.df['Number']>0)]
        # Trying to set properties of pool.selected for display
        pool.selected.style.set_properties(**{'background_color': 'lightgreen'})
        if (len(pool.selected.index) != 0):
            st.dataframe(
                pool.selected,
                column_config={
                    "Reference": "Model",
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
                    "Protocol":None,
                    "Message":None,
                    "Type":None
                },
                column_order=['Number','Brand','Reference','Cable','SupportURL','ManufacturerURL'],
                hide_index = True)
            return(pool.selected)
    # Edit the type of network selected
    def pool_edit_camera_for_network(self,pool):
        def edit_camera_network(df,key):
            if (len(df.index) != 0): 
                df = st.data_editor(
                    df,
                    column_config={
                        "Type": "Type",
                        "Reference": "Model",
                        'Number':st.column_config.NumberColumn(
                            "# Cams",
                            help="How much camera of this type in your use-case (0-15)?",
                            min_value=0,
                            max_value=15,
                            step=1,
                            default=0,
                            format="%d",
                        ),
                        'Network': st.column_config.SelectboxColumn(
                            "IP Network",
                            help="Select the IP network type",
                            width="small",
                            default = st.session_state.property.constraints[(key,'Network')][0],
                            options = st.session_state.property.constraints[(key,'Network')],
                            required=True),
                        'Base':  st.column_config.SelectboxColumn(
                            "Basement",
                            help="Base type",
                            width="small",
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
                        # "supportText": None,
                        "Message":None,
                        },
                    disabled=['Reference','Brand','Number','SupportURL'],
                    column_order=['Network','Reference','Brand','Number','SupportURL'],
                    hide_index = True,
                    use_container_width = True,
                    key = key+"_network",
        #            on_change = st.rerun,
                    )
                ## st.markdown(display)
                #print("\nDATAFRAME AFTER EDIT")
                #print(df)
                return(df)
        blocks = {}
        camera_types = pool.selected["Type"].unique()
        for camera_type in camera_types:
            #filter instance dataframe by type
            selected_rows = pool.selected.loc[pool.selected['Type'] == camera_type]
            if not selected_rows.empty :
                st.markdown(camera_type)
                blocks[camera_type] = edit_camera_network(selected_rows,key=camera_type)
        pool.final = pd.concat(list(blocks.values()))
        print("StreamUI->pool_edit_camera_for_network-> POOL.FINAL columns:\n",pool.final.columns)



if __name__  == "__main__":
    reader = Pool()
    reader.apply_pattern("","Sony","PTZ")
    #result = reader.pipe(get_cameras).pipe(apply_pattern,"CV","")
    print("\nRESULT:\n")
    print("Columns:\n",reader.df.columns)
    print("Dataframe:\n",reader.df)
    print("\nFiltered Dataframe:\n",reader.step_match)
