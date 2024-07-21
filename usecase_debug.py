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

def debug_usecase(self,debug_mode= None):
    print('DEBUG_MODE: ',debug_mode)
    if debug_mode == None: 
        pass
    elif debug_mode == "save_usecase_seed":
        self.df.to_csv('./debug/debug_df_before_analyze.csv')
    elif debug_mode == "save_usecase_result":
        self.df.to_csv('./debug/debug_df_after_analyze.csv')
    elif debug_mode == "setup_usecase":
        self.df.read_csv("./debug/debug_df_before_analyze.csv")
    else:
        print('UNSUPPORTED DEBUG MODE: ',debug_mode)
    return

Usecase.debug_camerapool_to_csv = debug_camerapool_to_csv
Usecase.debug_camerapool_to_usecase = debug_camerapool_to_usecase
Usecase.debug_usecase = debug_usecase
