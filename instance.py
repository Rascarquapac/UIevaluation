import pandas as pd
import graphviz as gv
from property import Properties

# Built a dataframe wiht camera instancesIntanes
class Instances:
    def __init__(self) -> None:
        self.df = pd.DataFrame()
        self.property = Properties()  
        self.active = False
        return 

    def create(self,cameras_df):
        self.columns_name = cameras_df.columns.values
        self.df.index.name = 'Instance'     

        print("################### DEBUG CAMERA_LENS_INIT#######################")
        print("CAMERAS DATAFRAME")
        print(cameras_df)
        camera_lens_dict = {}
        print("List of cameras",cameras_df.index.to_list())
        if not cameras_df.empty:
            for camera_index in cameras_df.index.to_list():
                print("NUMBER VALUE:---> ", cameras_df.loc[camera_index,'Number'],)
                for i in range(int(cameras_df.loc[camera_index,'Number'])):
                    new_index = str(camera_index) + "_" + str(i) 
                    print(new_index)
                    print(cameras_df.loc[camera_index])
                    variables = []
                    variables.extend(cameras_df.loc[camera_index].tolist())
                    # variables.extend(['Fixed','Wired Lan','Fixed'])
                    print(variables)
                    #camera_lens_dict[new_index] = [camera_index].extend(variables)
                    camera_lens_dict[new_index] = list(variables)
            self.df = pd.DataFrame.from_dict(camera_lens_dict, orient = 'index', columns = self.columns_name)
            self.df.index.name = 'Instance'        
        self.df.drop(columns=['SupportURL', 'ManufacturerURL','Remark','Unnamed: 6','Unnamed: 7','Selected','Message'], inplace=True)

        print("\n\nCAMERA LENS DATAFRAME :")
        print(self.df)
################## CANDIDATES #######################
    def lens_init(self):
        self.df = pd.DataFrame.from_dict({
                'Camera Brand Motorized Lens':  [None, None], 
                'ENG Canon Lens': [None, 'CY-CBL-B4-01'],
                'ENG Fuji Lens': [None, 'CY-CBL-B4 et CY-CBL-FUJI-2'],
                'Cine Lens': ['external', 'CY-CBL-B4 et CY-CBL-FUJI-2'], 
                'Photo Lens': ['external', None]}, 
            orient = 'index')
    def init_graph(self,name,rank='sink'):
        graph = gv.Graph(name='cluster_' + name)
        graph.attr(rankdir='RL', size='6,3',style='filled',color='lightyellow',label=name,rank=rank)
        graph.node_attr.update(style='filled',shape= 'box',color='lightcyan1')
        graph.edge_attr.update(fontsize='8pt')
        return(graph)
################## STREAMLIT #######################       
    def display_camera_table(self):
        print("DEBUG:cyaneval->display_camera_table ...")
        if (len(self.df.index) != 0):
            st.dataframe(
                self.df,
                column_config={
                    "Model": "Model",
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
                column_order=['Model','Instance','Network','Lens','Base'],
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
                    "Model": "Model",
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
                disabled=['Instance','Model','Number','Cable'],
                column_order=['Model','Instance','Network','Lens','Base'],
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
################## DEBUG ############################
    def debug_camerapool_to_csv(self,camerapool):
        if not camerapool.empty:
            camerapool.to_csv("./data/camera_pool.csv")
    def debug_camerapool_to_instancepool(self):
        camera_df = pd.DataFrame()
        if self.df.empty:
            camera_df= pd.read_csv("./data/camera_pool.csv")
            camera_df.set_index('Model', inplace=True)
            self.create(camera_df)
    def debug_instancepool_to_csv(self):
        if not self.df.empty:
            self.df.to_csv("./data/instance_pool.csv")
    def debug_csv_to_instancepool(self):
        if self.df.empty:
            self.df.read_csv("./data/instance_pool.csv")
################## ANALYZE ############################
    def analyze(self):
        self.device_from_cable()
        self.device_from_network()
        # self.lens()
        # self.base()
        # self.max_latency()
        # self.max_throughput()
        print("###########-> DATAFRAME LAN_wired: ")
        print(self.df)
        print(self.df[['Type','Network','Cable','Device']])    
    def device_from_cable(self):
        def select(cable):
            match cable:
                case cable if cable[0:7] == "CY-CBL-" : return "CI0"
                case "Ethernet-RJ45"  : return "PassThru"
                case "USB-A-to-USB-C" : return "PassThru"
                case "IP-to-USB-C"    : return "PassThru"
                case "BM-SDI"         : return "PassThru"
                case "JVC USB-to-IP"  : return "PassThru" 
                case "XDCA back"      : return "PassThru" 
                case _                : return "PassThru" 
        self.df['Device'] = self.df.apply(lambda row: select(row['Cable']), axis=1)
    def device_from_network(self):
        def select(current_device,network):
            match network:
                case "LAN wired" : return current_device
                case "LAN RF"    : return current_device
                case "WAN wired" : return "RIO"
                case "WAN RF"    : return "RIO"
                case "RF video"  : return "RIO-Live"
                case "WAN video" : return "RIO"
                case _           : return "Unlisted" 
        self.df['Device'] = self.df.apply(lambda row: select(row['Device'],row['Network']), axis=1)
#################### DRAW  ############################
    def draw_instances(self):
        top   = self.init_graph("Cyanview")
        switchers = []
        for camtype in self.property.options['CameraTypes']:
            camtype_df = self.df[(self.df['Type'] == camtype)]
            if not camtype_df.empty:
                print("Camera Type: ", camtype)
                venue = self.init_graph(camtype,'source')
                switcher_name = "Switcher_" + camtype 
                for instance in camtype_df.index:
                    device = camtype_df.loc[instance,'Device']
                    cable  = camtype_df.loc[instance,'Cable']
                    device_id = device + camtype
                    # print("    Instance = ",instance)
                    # print("    Device   = ",device)
                    # print("    Cable    = ",cable)
                    venue.node(name=instance,label=instance)
                    venue.node(name=device_id,label=device)
                    venue.edge(instance,device_id,cable)
                    switchers.append((device_id,switcher_name))
                top.subgraph(venue)
                print(switchers)
        croom = self.init_graph("Control",'sink')
        for edge in switchers:
            (device_id,switcher_id) = edge
            croom.node(name=switcher_id,label=switcher_id)
            croom.edge(device_id,switcher_id,"Ethernet Link")
        top.subgraph(croom)
        return(top)
                

