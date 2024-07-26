import pandas as pd
from property import Properties
from mermaid.graph import Graph

# Built a dataframe wiht camera instances
class Usecase:
    def __init__(self) -> None:
        self.property = Properties()
        self.df = pd.DataFrame()
        return
    def setup(self,cameras_df=None):
        def dico(cameras_df):
            paths_dict = {}
            if not cameras_df.empty:
                for camera_index in cameras_df.index.to_list():
                    for i in range(int(cameras_df.loc[camera_index,'Number'])):
                        new_index = str(camera_index) + "_" + str(i) 
                        variables = []
                        variables.extend(cameras_df.loc[camera_index].tolist())
                        paths_dict[new_index] = list(variables)
            return (paths_dict)
        def columns():
            self.df.drop(columns=['SupportURL', 'ManufacturerURL','Remark','Selected','Message'], inplace=True)
            self.df['Camera_id'] = self.df.index
            self.df['Device']    = ""
            self.df['Device_id'] = ""
            self.df['Switch_id'] = ""
            self.df['RCP_id']    = ""
            self.df['Camgroup']  = ""
            self.df['RCPtype']   = ""
            self.df['LensTypes'] = "Unknown"
            self.df['LensMotorization'] = "No motorization"	
            self.df['ControlNeeds']= "No needs"
            #self.df['lens_id']=""
            return
        paths_dict = dico(cameras_df)
        self.df.index.name = 'Instance'     
        self.df = pd.DataFrame.from_dict(paths_dict, orient = 'index', columns = cameras_df.columns.values)
        columns()       
        return 
