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
        self.df = pd.read_pickle("./picklized/cameras.pkl")
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
        protocols = pd.read_csv("./data/CyanviewDescriptor - CameraProtocols.csv",usecols=["Protocol","Brand","Type","Cable","SupportURL","Message","MaxDelayToComplete","ControlCoverage","Bidirectionnal"])
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
        print('############ NEW SEARCH ###############')
        print(self.df)
        print(f'Search based on brand({brand}) and pattern ({camera_pattern})')
        print(match)
        return 

if __name__  == "__main__":
    reader = Pool()
    reader.apply_pattern("CV","")
    #result = reader.pipe(get_cameras).pipe(apply_pattern,"CV","")
    print("RESULT:\n")
    print(reader.df)
