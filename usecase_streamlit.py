import pandas as pd 
import streamlit as st
from usecase import Usecase 
################## STREAMLIT #######################       
def display_camera_table(self):
    print("DEBUG:cyaneval->display_camera_table ...")
    if (len(self.df.index) != 0):
        st.dataframe(
            self.df,
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
                'Lens': "Lens Type",
                'Network': None,
                'Base': None,
                "SupportURL": None,
                "ManufacturerURL": None,
                "Reference": None,
                #"supportText": None,
                "Protocol":None,
                "Message":None,
                "Type":None
            },
            column_order=['Reference','Instance','Network','Lens','Base'],
            hide_index = True)
def edit_camera_table(self,key='1'):
    # Validate inputs
    if (len(self.df.index) != 0): 
        # display = self.text_message()
        self.df = st.data_editor(
            self.df,
            key = key,
            column_config={
                'Instance': "Instance",
                'Number':st.column_config.NumberColumn(
                    "# Cams",
                    help="How much camera of this type in your use-case (0-15)?",
                    min_value=0,
                    max_value=15,
                    step=1,
                    default=0,
                    format="%d",
                ),
                "Reference": "Model",
                'Lens': st.column_config.SelectboxColumn(
                    "Lens",
                    help="Lens type",
                    width="medium",
                    options= self.property.constraints[(key,'Lens')],
                    required=True),
                'Network':  st.column_config.SelectboxColumn(
                    "Network",
                    help="Select the network type",
                    width="medium",
                    options=self.property.constraints[(key,'Network')],
                    required=True),
                'Base':  st.column_config.SelectboxColumn(
                    "Basement",
                    help="Base type",
                    width="medium",
                    options=self.property.constraints[(key,'Base')],
                    required=True),
                "Brand": None,
                "Cable": None,
                "SupportURL": None,
                "ManufacturerURL": None,
                "Reference": None,
                #"supportText": None,
                "Protocol":None,
                "Message":None,
                "Type":None
            },
            disabled=['Instance','Reference','Number','Cable'],
            column_order=['Reference','Instance','Network','Lens','Base'],
            hide_index = True)
        ## st.markdown(display)
        print("\nDATAFRAME AFTER EDIT")
        print(self.df)
        # self.print_selected()
        return (self.df)

def merge(self,blocks):
    self.df = pd.DataFrame()
    self.df = pd.concat(list(blocks.values()))
    return(self.df)    

Usecase.display_camera_table = display_camera_table
Usecase.edit_camera_table = edit_camera_table
Usecase.merge = merge
