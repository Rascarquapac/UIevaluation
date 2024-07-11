import csv
import pandas as pd
import streamlit as st
from property import Properties

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
        #self.get_cameras()
        self.brands = self.df["Brand"].unique()

    def pkl_cameras(self):
        self.df = pd.read_pickle("cameras.pkl")
        return
    def get_cameras(self):
        cameras = pd.read_csv("./data/CyanviewDescriptor - Cameras.csv",usecols=['Model','Reference','Protocol','Brand','ManufacturerURL','Remark'])
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
        protocols = pd.read_csv("./data/CyanviewDescriptor - CameraProtocols.csv",usecols=["Protocol","Brand","Type","Cable","SupportURL","Message","MaxDelayToComplete","ControlCoverage","Bidrectionnal"])
        proto_df = pd.DataFrame(protocols)
        del proto_df['Brand']
        self.df = pd.merge(cam_df, proto_df, on = ['Protocol'],how = 'left').set_index('Model')
        # Add missing columns
        self.df = self.df.assign(Selected=False)
        self.df = self.df.assign(Number=0)
        self.df = self.df.assign(Lens='Fixed')
        self.df = self.df.assign(Network='LAN wired')
        self.df = self.df.assign(Base='Fixed')
        ## To suppress ??
        #df['Model'] = df.index
        self.df.to_csv("./data/Generated_CameraDetails.csv")
        return(self)
    def apply_pattern(self,camera_pattern="",brand=""):
        if camera_pattern != None and camera_pattern != "":
            camera_selection = self.df.filter(like=camera_pattern,axis=0)
        else:
            camera_selection = self.df
        if brand != None and brand != "":
            brand_query = f'Brand == "{brand}"'
            match = camera_selection.query(brand_query)
        else:
            match = camera_selection
        self.step_match = match
        return 
    def edit_camera_number(self):
        # Validate inputs
        if (len(self.step_match.index) != 0): 
            self.step_select = st.data_editor(
                self.step_match,
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
            return(self.step_select)
    def display_selected(self):
        # Update the camera pool Dataframe with the number of camera selected on this step
        self.df.update(self.step_select)
        # Set the set of selected cameras
        self.selected = self.df[(self.df['Number']>0)]
        # Trying to set properties of self.selected for display
        self.selected.style.set_properties(**{'background_color': 'lightgreen'})
        print("DEBUG:cyaneval->display_camera_table ...")
        if (len(self.selected.index) != 0):
            st.dataframe(
                self.selected,
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
            return(self.selected)
    def edit_camera_per_type(self,mode='network'):
        def edit_camera_network(df,key):
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
                    key = key+"_network",
        #            on_change = st.rerun,
                    )
                ## st.markdown(display)
                #print("\nDATAFRAME AFTER EDIT")
                #print(df)
                return(df)
        def edit_camera_lens(df,key):
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
                    key = key+"_lens",
        #            on_change = st.rerun,
                    )
                ## st.markdown(display)
                #print("\nDATAFRAME AFTER EDIT")
                #print(df)
                return(df)

        blocks = {}
        camera_types = self.selected["Type"].unique()
        for camera_type in camera_types:
            #filter instance dataframe by type
            selected_rows = self.selected.loc[self.selected['Type'] == camera_type]
            if not selected_rows.empty :
                if mode == 'network':
                    blocks[camera_type] = edit_camera_network(selected_rows,key=camera_type)
                elif mode == 'lens':
                    blocks[camera_type] = edit_camera_lens(selected_rows,key=camera_type)
                else:
                    raise("Mode of input should be 'network' or 'lens' ")
        self.final = pd.concat(list(blocks.values()))


if __name__  == "__main__":
    reader = Pool()
    reader.apply_pattern("CV","")
    #result = reader.pipe(get_cameras).pipe(apply_pattern,"CV","")
    print("RESULT:\n")
    print(reader.df)
