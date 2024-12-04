import pandas as pd
import streamlit as st
from streamlit_gsheets import GSheetsConnection
import csv
import re
import pickle 
import pandas as pd
import os
import requests
import sys
from pprint import pprint

class Camera():
    def __init__(self,update=True,debug=False):
        self.df       = self.camera(update)
        self.pool_df = self.pool()
        self.brand_df = self.df["Brand"].unique()
        self.type_df  = self.df["Type"].unique()
        self.step_match  = pd.DataFrame()
        # self.step_select contains the cameras selected by the user for the current selection step
        self.step_select = pd.DataFrame()
        # self.selected contains the full set of cameras selected by the user 
        self.selected    = pd.DataFrame()
        # the set of cameras selected splitted by blocks of cameras of the same type

    def camera(self,update):
        def gsheet_camera():
            conn = st.connection("cameras", type=GSheetsConnection)
            cam_df = conn.read(usecols=[
                'Model','Reference','Protocol','Brand','ManufacturerURL','Remark',"CameraLensControl","LensMount"])        
            conn = st.connection("protocols", type=GSheetsConnection)
            proto_df = conn.read(usecols=[
                "Protocol","Brand","Type","Cable","SupportURL","Message","MaxDelayToComplete","ControlCoverage","Bidirectionnal"])
            # PROFILE THE CAMERA POOL
            del proto_df['Brand']
            # LEFT JOIN FOR COMBINING CAMERAS AND PROTOCOLS DATA
            camera_df = pd.merge(cam_df, proto_df, on = ['Protocol'],how = 'left').set_index('Model')
            return camera_df
        if update:
            cameras_df = gsheet_camera()
            cameras_df.to_pickle("./picklized/x_cameras.pkl")
        else:
            try:
                camera_df = pd.read_pickle("./picklized/x_cameras.pkl")
            except:
                cameras_df = self.gsheet_camera()
                cameras_df.to_pickle("./picklized/x_cameras.pkl")
        return(cameras_df)
    def pool(self):
        pool_df = self.df.copy()
        # ADD COLUMNS 
        pool_df = pool_df.assign(Selected=False)
        pool_df = pool_df.assign(Number=0)
        return pool_df

    def apply_pattern(self,camera_pattern="",brand="",camera_type=""):
        if camera_pattern != None and camera_pattern != "":
            pattern_selection = self.pool_df.filter(like=camera_pattern,axis=0)
        else:
            pattern_selection = self.pool_df
        if brand != None and brand != "":
            brand_query = f'Brand == "{brand}"'
            brand_selection = pattern_selection.query(brand_query)
        else:
            brand_selection = pattern_selection
        if camera_type != None and camera_type != "":
            type_query = f'Type == "{camera_type}"'
            match = brand_selection.query(type_query)
        else:
            match = brand_selection
        self.step_match = match
        # print('############ NEW SEARCH ###############')
        # print(self.df)
        # print(f'Search based on brand({brand}) and pattern ({camera_pattern})')
        # print(match)
        return 
    # User Interface for setting  cameras number
    def edit_number(self,pool):
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
                key = "x_camera_number",
    #            on_change = st.rerun,
                )
            return(pool.step_select)
    # Displaying the result of the camera selection
    def display_selected(self,pool):
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
    def purgatory(self):
        # ADD COLUMNS WITH DEFAULT VALUE
        pool_df = pool_df.assign(Selected=False)
        pool_df = pool_df.assign(Number=0)
        pool_df = pool_df.assign(Lens='Fixed')
        pool_df = pool_df.assign(Network='LAN Wired')
        pool_df = pool_df.assign(Base='Fixed')
        # SAVE AS FILE
        pool_df.to_csv("./picklized/Generated_CameraDetails.csv")
        return pool_df

if __name__ == "__main__":
    camera = Camera()
    pprint(camera.df)
 
