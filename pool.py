import csv
import pandas as pd
import streamlit as st
from property import Properties
from lens import Lens
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

if __name__  == "__main__":
    reader = Pool()
    reader.apply_pattern("","Sony","PTZ")
    #result = reader.pipe(get_cameras).pipe(apply_pattern,"CV","")
    print("\nRESULT:\n")
    print("Columns:\n",reader.df.columns)
    print("Dataframe:\n",reader.df)
    print("\nFiltered Dataframe:\n",reader.step_match)
