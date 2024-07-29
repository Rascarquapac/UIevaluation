import pandas as pd
from property import Properties
from ._draw    import init_graph,draw_all, graph_mermaid, get_mermaid_code, streamlit_mermaid
from ._network import converter_from_cable, device_from_network,camgroup_from_cameratype, device_id_from_device,switch_id_from_camgroup, rcptype_from_camgroup, rcp_id_from_camgroup, rcp_optimize
from ._quote   import rcp_count, cable_count, device_count
from ._lens    import lens_init
from ._debug   import debug_pool_to_csv, debug_csv_to_pool, debug_usecase_to_csv

global_debug_prefix = "base"
global_debug_pool_record = True
global_debug_pool_load   = False
global_debug_usecase_record = True
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
            #self.df['lens_id']=""
            return
        if not pool_df.empty:
            paths_dict = dataframe_to_dic(pool_df)
            self.df = dic_to_dataframe(paths_dict,pool_df)
            columns()       
        return 

    # Pipeline, from camera to control, establishing Cyaview gear requirements 
    def analyze(self,pool_df = None):
        if global_debug_pool_record : debug_pool_to_csv(pool_df,global_debug_prefix)
        if global_debug_pool_load   : pool_df = debug_csv_to_pool(global_debug_prefix)
        self.setup(pool_df)
        self.converter_from_cable()
        self.device_from_network()
        self.camgroup_from_cameratype()
        self.device_id_from_device()
        self.switch_id_from_camgroup()
        self.rcptype_from_camgroup()
        self.rcp_id_from_camgroup()
        self.rcp_optimize()
        self.rcp_count()
        self.cable_count()
        self.device_count()
        if global_debug_usecase_record: debug_usecase_to_csv(self.df,global_debug_prefix)
        print('########## RCPs :',self.rcps)
        print('########## DEVICES :',self.devices)
        print('########## CABLEs :',self.cables)

    # Network
    def converter_from_cable(self) : return converter_from_cable(self)
    def device_from_network(self) : return device_from_network(self)
    def camgroup_from_cameratype(self) : return camgroup_from_cameratype(self)
    def device_id_from_device(self) : return device_id_from_device(self)
    def switch_id_from_camgroup(self) : return switch_id_from_camgroup(self)
    def rcptype_from_camgroup(self) : return rcptype_from_camgroup(self)
    def rcp_id_from_camgroup(self) : return rcp_id_from_camgroup(self)
    def rcp_optimize(self) : return rcp_optimize(self)

    # Quotation
    def rcp_count(self) : return rcp_count(self)
    def cable_count(self) : return cable_count(self)
    def device_count(self) : return device_count(self)
    # Lens
    def lens_init(self) : return lens_init(self)

    # Graph generation
    def init_graph(self,name,rank='sink'):        return init_graph(self,name,rank)
    def draw_all(self): return draw_all(self)
    def graph_mermaid(self,code): return graph_mermaid(self,code)
    def get_mermaid_code(self): return get_mermaid_code(self)
    def streamlit_mermaid(self,mermaid_graph): return streamlit_mermaid(self,mermaid_graph)

if __name__ == "__main__":
    global_debug_prefix = "base"
    global_debug_pool_load = False
    global_debug_usecase_record = True
    usecase = Usecase()
    usecase.df.analyze()