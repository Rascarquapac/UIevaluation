import pandas as pd
from property import Properties
from mermaid.graph import Graph

# Built a dataframe with one line per camera instance
class Usecase:
    def __init__(self) -> None:
        self.property = Properties()
        self.df = pd.DataFrame()
        return
    # Setup Usecase dataframe from Pool dataframe
    def setup(self,pool_df = None):
        # Create a dictionnary from the Pool dataframe
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
        paths_dict = dataframe_to_dic(pool_df)
        self.df = dic_to_dataframe(paths_dict,pool_df)
        columns()       
        return 
