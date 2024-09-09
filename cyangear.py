import pandas as pd
from cyancameralens import CameraLens
from cyanglue import *
from cyanmedium import Medium
from cyanrcp import *
class Cyangear():
    def __init__(self) -> None:
        self.df = pd.DataFrame()
        self.dic= {}
        pass
    # Setup Cyangear dataframe from Pool dataframe
    def set_dataframe(self,pool_df = None):
        # Create a dictionnary from the Pool dataframe with 
        #     key = instance name based on dataframe index
        #     data = dataframe row retlated to the index as a list
        def dataframe_to_dic(pool_df):
            paths_dict = {}
            if not pool_df.empty:
                for camera_index in pool_df.index.to_list():
                    for i in range(int(pool_df.loc[camera_index,'Number'])):
                        new_index = str(camera_index) + "_" + str(i) 
                        variables = []
                        variables.extend(pool_df.loc[camera_index].tolist())
                        paths_dict[new_index] = list(variables)
            return (paths_dict)
        # Create a dataframe from dictionnary   
        def dic_to_dataframe(paths_dict,pool_df):
            df = pd.DataFrame.from_dict(paths_dict, orient = 'index', columns = pool_df.columns.values)
            df.index.name = 'Instance'     
            return(df)
        # Suppress and add columns
        def columns():
            # Suppressunused column
            self.df.drop(columns=['SupportURL', 'ManufacturerURL','Remark','Selected','Message'], inplace=True)
            # Add result columns storing the results of protocol analyse
            self.df['Camera_id'] = self.df.index
            self.df['Device']    = ""
            self.df['Device_id'] = ""
            self.df['Switch_id'] = ""
            self.df['RCP_id']    = ""
            self.df['Camgroup']  = ""
            self.df['RCPtype']   = ""
            self.df['Fanout']    = 0
            # Add result columns storing the results of lens analyse
            self.df['LensCable']  = ""
            self.df['MotorCable'] = ""
            self.df['LensMotor']  = ""
            # Not to be done here
            # self.df['LensTypes'] = ""

            #self.df['lens_id']=""
            return
        if not pool_df.empty:
            paths_dict = dataframe_to_dic(pool_df)
            self.df = dic_to_dataframe(paths_dict,pool_df)
            columns()       
        return 
    def set_objects_dic(self):
        for index in self.df.index.to_list():
            df_row = self.df.loc[index]
            cameralens = CameraLens(index,df_row["Reference"],df_row["Protocol"],df_row["Cable"])
            glue   = GlueTBD() 
            medium = Medium()
            rcp    = RCP_TBD()
            self.dic[index]= (cameralens,glue,medium,rcp)
    def analyze_object(self,pool_df = None):
        self.set_dataframe(pool_df)
        self.set_objects_dic()
        # self.lens_cable()
        # # IP or serial converter
        # self.device_from_camera_lens()
        # #
        # self.device_fanout()
        # self.device_from_network()
        # self.camgroup_from_cameratype()
        # self.device_id_from_device()
        # self.switch_id_from_camgroup()
        # self.rcptype_from_camgroup()
        # self.rcp_id_from_camgroup()
        # print("Columns in Usecase dataframe (usecase.df): ",self.df.columns)
        # self.rcp_optimize()
        # self.rcp_count()
        # self.cable_count()
        # self.device_count()
        # if global_debug_usecase_record: debug_usecase_to_csv(self.df,global_debug_prefix)
        # print('########## RCPs :',self.rcps)
        # print('########## DEVICES :',self.devices)
        # print('########## CABLEs :',self.cables)
        pass