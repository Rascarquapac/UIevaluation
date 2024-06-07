import csv
import pandas as pd
import streamlit as st

class Descriptor():
    def __init__(self) -> None:
        self.df = pd.DataFrame()
        return
    
    def get_csv(self):
        self.set_cameras()


    def set_cameras(self):
        cameras_df = pd.read_csv("./data/CyanviewDescriptor - Cameras.csv")
        self.cameras_df = pd.DataFrame(cameras_df)
        print(self.cameras_df)
        cameraProtocols_df = pd.read_csv("./data/CyanviewDescriptor - CameraProtocols.csv")
        self.cameraProtocols_df = pd.DataFrame(cameraProtocols_df)
        del self.cameraProtocols_df['Brand']
        print(self.cameraProtocols_df)
        self.cameraDetails_df=pd.merge(self.cameras_df, self.cameraProtocols_df, on = ['Protocol'],how = 'left').set_index('Model')
                # Add missing columns
        self.cameraDetails_df = self.cameraDetails_df.assign(selected=False)
        self.cameraDetails_df = self.cameraDetails_df.assign(number=0)
        self.cameraDetails_df = self.cameraDetails_df.assign(lens='Fixed')
        self.cameraDetails_df = self.cameraDetails_df.assign(network='LAN wired')
        self.cameraDetails_df = self.cameraDetails_df.assign(base='Fixed')
        ## To suppress ??
        self.cameraDetails_df['Model'] = self.cameraDetails_df.index
        print(self.cameraDetails_df)
        self.cameraDetails_df.to_csv("./data/Generated_CameraDetails.csv")
        self.df = self.cameraDetails_df
        return 
    
    def get_cameras(self, camera_pattern):
        #filtered_df = df.filter(regex='^A', axis=0)
        #query = f"model.str.contains('.*{camera_pattern}')"
        #regularexp = f"'.*{camera_pattern}.*'"
        print("Camera Pattern = ",camera_pattern)
        selection = self.df.filter(like=camera_pattern,axis=0)
        #selection = self.df.filter(regex=regularexp,axis='Model')
        return(selection)

    def text_message(self):
        display=""
        if not self.df.empty: 
            display = "### The following compatible cameras match your description.\n"
            for index in self.df.index.to_list():
                row = self.df.loc[index]
                display += f"### Model {index}\n"
                display += f"+ Brand: {row['Brand']}\n"
                display += f"+ Cable: {row['Cable']}\n"
                display += f"+ Cyanview support: [{"Support URL"}]({row['SupportURL']})\n"
        return(display)
    
    def print_selected(self):
        print("database->display_selected: Displaying selected rows:\n")
        condition = self.df['selected'] == True
        if not condition.empty : 
            print(self.df[condition])
        else: 
            print(" No row match")
        return
    
    def merge(self,step,condition=None):
        print("DEBUG:database->merge():")
        print("\n\nRESULT DATAFRAME BEFORE MERGE:")
        print(self.df)
        print("\n\STEP DATAFRAME BEFORE MERGE:")
        print(step.df)
        step_df = step.df.copy()
        selected_df = step_df[(step_df['selected'] == True) & (step_df['number'] > 0)]
        print("\nSELECTED DATAFRAME BEFORE MERGE:")
        print(selected_df)
 
        if condition != None: query = condition
        else: query = f"selected == True"
        # Index defined so minimum length is 1 
        if self.df.empty:
            self.df = selected_df
        else:
            for step_index in selected_df.index.to_list():
                if step_index not in self.df.index:
                    # add new indexe
                    new_indexes = self.df.index.insert(0,step_index)
                    self.df = self.df.reindex(new_indexes)
                # add the row
                print("Index : ",step_index)
                print("LIGNE de RESULT")
                print(self.df.loc[step_index])
                print("LIGNE de STEP SELECTED")
                print(selected_df.loc[step_index])
                print("AFFECTATION")
                self.df.loc[step_index] = selected_df.loc[step_index]
        print("\n\nRESULT DATAFRAME AFTER MERGE:")
        print(self.df)

    def display_camera_table(self):
        print("DEBUG:cyaneval->display_camera_table ...")
        if (len(self.df.index) != 0):
            st.dataframe(
                self.df,
                column_config={
                    "selected": "Is Selected",
                    "number":st.column_config.NumberColumn(
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
#                    "supportText": None,
                    "Protocol":None,
                    "Message":None,
                    "Type":None
                },
                column_order=['selected','number','Model','Cable','SupportURL','ManufacturerURL'],
                hide_index = True)

    def edit_camera_table(self):
        # Validate inputs
        if (len(self.df.index) != 0): 
            display = self.text_message()
            self.df = st.data_editor(
                self.df,
                column_config={
                    "selected": "Is Selected",
                    "number":st.column_config.NumberColumn(
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
                disabled=['Model','SupportURL','ManufacturerURL'],
                column_order=['selected','number','Model','Cable','SupportURL','ManufacturerURL'],
                hide_index = True)
            ## st.markdown(display)
            print("\nDATAFRAME AFTER EDIT")
            print(self.df)
            self.print_selected()

if __name__  == "__main__":
    reader = Descriptor()