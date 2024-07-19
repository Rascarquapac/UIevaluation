import pandas as pd
from usecase import Usecase
################## DEBUG ############################
def debug_camerapool_to_csv(self,camerapool):
    if not camerapool.empty:
        camerapool.to_csv("./debug/camera_pool.csv")
def debug_camerapool_to_usecase(self):
    camera_df = pd.DataFrame()
    if self.df.empty:
        camera_df= pd.read_csv("./debug/camera_pool.csv")
        camera_df.set_index('Model', inplace=True)
        self.setup(camera_df)
def debug_instancepool_to_csv(self):
    if not self.df.empty:
        self.df.to_csv("./debug/instance_pool.csv")
def debug_csv_to_instancepool(self):
    if self.df.empty:
        self.df.read_csv("./debug/instance_pool.csv")

Usecase.debug_camerapool_to_csv = debug_camerapool_to_csv
Usecase.debug_camerapool_to_usecase = debug_camerapool_to_usecase
Usecase.debug_instancepool_to_csv = debug_instancepool_to_csv
Usecase.debug_csv_to_instancepool = debug_csv_to_instancepool
