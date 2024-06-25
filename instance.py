import pandas as pd
import graphviz as gv
from property import Properties
import base64
import mermaid as md
from mermaid.graph import Graph

# Built a dataframe wiht camera instances
class Instances:
    def __init__(self) -> None:
        self.property = Properties()
        self.df = pd.DataFrame()
        return
################## ANALYZE #########################
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
            #self.df['lens_id']=""
            return
        paths_dict = dico(cameras_df)
        self.df.index.name = 'Instance'     
        self.df = pd.DataFrame.from_dict(paths_dict, orient = 'index', columns = cameras_df.columns.values)
        columns()       
        return 
    def analyze(self):
        self.device_from_cable()
        self.device_from_network()
        self.camgroup_from_cameratype()
        self.device_id_from_device()
        self.switch_id_from_camgroup()
        self.rcptype_from_camgroup()
        self.rcp_id_from_camgroup()
        self.rcp_optimize()
        # self.lens()
        # self.base()
        # self.max_latency()
        # self.max_throughput()
        self.df.to_csv('./debug_anayzed_cameras.csv')
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
        def select(current_device,network,MaxDelayToComplete):
            match network:
                case "LAN wired" : return current_device
                case "LAN RF"    :
                    if  MaxDelayToComplete < 200:
                        return "RIO-Live"
                    else: 
                        return current_device
                case "WAN wired" : return "RIO"
                case "WAN RF"    : return "RIO"
                case "RF video"  : return "RIO-Live"
                case "WAN video" : return "RIO"
                case _           : return "Unlisted"
            return
        self.df['Device'] = self.df.apply(lambda row: select(row['Device'],row['Network'],row['MaxDelayToComplete']), axis=1)
    def camgroup_from_cameratype(self):
        def select(camtype,network):
            return camtype
        self.df['Camgroup'] = self.df.apply(lambda row: select(row['Type'],row['Network']), axis=1)
    def device_id_from_device(self):
        def update_status(devices_status):
            for key in devices_status:
                (number,port,maxconnect) = devices_status[key]
                devices_status[key]=(number+1,0,maxconnect)
            return
        def get_device_id(devices_status,device):
            try:
                (number,port,maxconnect) = devices_status[device]
            except:
                print(f"Device {device} not defined")
                raise
            if port < maxconnect : 
                port += 1
            else : 
                number += 1
                port = 1
            devices_status[device] = (number,port,maxconnect)
            return (device + "_" + str(number))
        devices_status = {"CI0":(-1,0,2),"RIO":(-1,0,1),"RIO-Live":(-1,0,1),"RSBM":(-1,0,1),"PassThru":(-1,0,100)}
        camgroups = self.df['Camgroup'].unique() 
        for camgroup in camgroups:
            update_status(devices_status)
            camgroup_indexes  = self.df.loc[self.df['Camgroup'] == camgroup].index.tolist() 
            # print("Camgroup:",camgroup)
            for index in camgroup_indexes:
                device = self.df.loc[index,'Device']
                self.df.loc[index,'Device_id'] = get_device_id(devices_status,device) 
                # print("    Device_id    : ",self.df.loc[index,'Device_id'])
                # print("    Device Status: ",devices_status)
    def switch_id_from_camgroup(self):
        self.df['Switch_id'] = self.df.apply(lambda row: row['Camgroup'] + " Switch", axis=1)
    def rcptype_from_camgroup(self):
        def select(camgroup):
            match camgroup:
                case 'Slow Motion': return("RCP") 
                case 'Mini Camera': return("RCP") 
                case 'PTZ': return("RCP-J") 
                case 'Shoulder Camcorder': return("RCP-DUO-J") 
                case 'Handheld Camcorder': return("RCP-DUO-J") 
                case 'Block': return("RCP-J") 
                case 'DSLR': return("RCP-DUO-J") 
                case 'System': return("RCP-DUO-J") 
                case 'Large Sensor': return("RCP-DUO-J") 
                case 'Any': return("RCP")
                case _: return("RCP")
            return
        self.df['RCPtype'] = self.df.apply(lambda row: select(row['Camgroup']), axis=1)    
    def rcp_id_from_camgroup(self):
        def get_rcp_id(rcps_status,RCPtype):
            try:
                (number,port,maxconnect) = rcps_status[RCPtype]
            except:
                print(f"RCP of type {RCPtype} not defined")
                raise
            if port < maxconnect : 
                port += 1
            else : 
                number += 1
                port = 1
            rcps_status[RCPtype] = (number,port,maxconnect)
            return ("CY-" + RCPtype + "_" + str(number))
        rcps_status = {"RCP":(0,0,200),"RCP-J":(0,0,200),"RCP-DUO-J":(0,0,1)}
        camgroups = self.df['Camgroup'].unique() 
        #self.df.to_csv('./debug_unknown_cameras.csv')
        for camgroup in camgroups:
            camgroup_indexes  = self.df.loc[self.df['Camgroup'] == camgroup].index.tolist() 
            for index in camgroup_indexes:
                self.df.loc[index,'RCP_id'] = get_rcp_id(rcps_status,self.df.loc[index,'RCPtype']) 
    def rcp_optimize(self):
        def get_rcptype_rcp_id(current_RCP,occurences):
            if current_RCP[0:12] == "CY-RCP-DUO-J": 
                rcptype = "CY-RCP-DUO-J"
                postfix = current_RCP[12:]
            elif current_RCP[0:8] == "CY-RCP-J":
                postfix =  current_RCP[8:]
                if occurences < 3 : 
                    rcptype = "CY-RCP-DUO-J"
                elif occurences < 5 :
                    rcptype = "CY-RCP-QUATTRO-J"
                elif occurences < 9 :
                    rcptype = "CY-RCP-OCTO-J"
                else:
                    rcptype = current_RCP
            elif current_RCP[0:6] == "CY-RCP":
                postfix =  current_RCP[6:]
                if occurences < 3 :
                    rcptype = "CY-RCP-DUO"
                elif occurences < 5 :
                    rcptype = "CY-RCP-QUATTRO"
                elif occurences < 9 :
                    rcptype = "CY-RCP-OCTO"
                else:
                    rcptype = current_RCP
            else: 
                rcptype = current_RCP
                postfix = ""
            return((rcptype,rcptype+postfix))
        rcp_ids = self.df['RCP_id'].unique() 
        for rcp_id in rcp_ids:
            occurences = self.df['RCP_id'].value_counts().get(rcp_id, 0) 
            rcp_indexes  = self.df.loc[self.df['RCP_id'] == rcp_id].index.tolist() 
            for index in rcp_indexes:
                (RCPtype, RCP_id)=get_rcptype_rcp_id(rcp_id,occurences)
                self.df.loc[index,'RCP_id'] = RCP_id 
                self.df.loc[index,'RCPtype'] = RCPtype 
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
            self.setup(camera_df)
    def debug_instancepool_to_csv(self):
        if not self.df.empty:
            self.df.to_csv("./data/instance_pool.csv")
    def debug_csv_to_instancepool(self):
        if self.df.empty:
            self.df.read_csv("./data/instance_pool.csv")
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
#################### DRAW ###########################
    def draw_all(self):
        top   = self.init_graph("Cyanview")
        top.attr(rankdir='RL', size='20,6',style='filled',color='lightyellow',label='Cyanview Gear')
        ####### DRAW CAMERAS & DEVICES ##############
        camgroups = self.df['Camgroup'].unique() 
        for camgroup in camgroups:
            camgroup_indexes  = self.df.loc[self.df['Camgroup'] == camgroup].index.tolist() 
            venue = self.init_graph(camgroup,'source')
            for index in camgroup_indexes:
                camera_id = self.df.loc[index,'Camera_id'] 
                device_id = self.df.loc[index,'Device_id'] 
                cable     = self.df.loc[index,'Cable']
                device    = self.df.loc[index,'Device']
                venue.node(name=camera_id,label=camera_id)
                venue.node(name=device_id,label=device)
                venue.edge(camera_id+":w",device_id+":e",cable)
            top.subgraph(venue)
        ###### DRAW SWITCHES #######################
        # croom = self.init_graph("Control",'sink')
        switches = self.df['Switch_id'].unique() 
        for switch in switches:
            switch_df  = self.df.loc[self.df['Switch_id'] == switch]
            device_ids = switch_df['Device_id'].unique()
            # croom.node(name=switch,label=switch)
            top.node(name=switch,label=switch)
            for device_id in device_ids:
                top.edge(device_id+":w",switch+":e","Ethernet Link")
        ####### DRAW RCPS ########################
        rcps = self.df['RCP_id'].unique() 
        for rcp in rcps:
            switch_df  = self.df.loc[self.df['RCP_id'] == rcp]
            switch  = switch_df['Switch_id'].unique()[0]
            RCPtype = switch_df['RCPtype'].unique()[0]
            top.node(name=rcp,label=RCPtype)
            top.edge(switch+":w",rcp+":e","Ethernet Link")
        # top.subgraph(croom)
        self.top =top
        return(top)
    def get_mermaid_code(self):
        def clean(code):
            return(code.replace(' ', ''))
        mermaid_code = ''
        mermaid_code = 'graph RL\n'
        ####### DRAW CAMERAS & DEVICES ##############
        camgroups = self.df['Camgroup'].unique() 
        for camgroup in camgroups:
            camgroup_indexes  = self.df.loc[self.df['Camgroup'] == camgroup].index.tolist() 
            mermaid_code+= 'subgraph ' + camgroup + "\n"
            for index in camgroup_indexes:
                camera_id = self.df.loc[index,'Camera_id'] 
                device_id = self.df.loc[index,'Device_id'] 
                cable     = self.df.loc[index,'Cable']
                device    = self.df.loc[index,'Device']
                mermaid_code += clean(camera_id)+ '{{"' + clean(camera_id) + ' fa:fa-camera-retro"}}---|'+clean(cable) +'|'+clean(device_id)+'\n'
            mermaid_code += 'end\n'
        ###### DRAW SWITCHES #######################
        # croom = self.init_graph("Control",'sink')
        mermaid_code += 'subgraph "Control Room" \n'
        switches = self.df['Switch_id'].unique() 
        for switch in switches:
            switch_df  = self.df.loc[self.df['Switch_id'] == switch]
            device_ids = switch_df['Device_id'].unique()
            # croom.node(name=switch,label=switch)
            for device_id in device_ids:
                mermaid_code += clean(device_id) + ' --- |Ethernet|' + clean(switch) + '\n'
        ####### DRAW RCPS ########################
        rcps = self.df['RCP_id'].unique() 
        for rcp in rcps:
            switch_df  = self.df.loc[self.df['RCP_id'] == rcp]
            switch  = switch_df['Switch_id'].unique()[0]
            RCPtype = switch_df['RCPtype'].unique()[0]
            mermaid_code += clean(switch) + ' --- |Ethernet|' + clean(rcp) + '\n'
        mermaid_code += 'end\n'
        return(mermaid_code)
    def graph_mermaid(self,code):
        if code == None :
            mermaid_code = """
            graph RL
            subgraph Mini Camera
            AtomOne4K_0{{"AtomOne4K_0 fa:fa-camera-retro"}}---|CY-CBL-6P-DCHIP-02|CI0_0
            AtomOne4K_1{{"AtomOne4K_1 fa:fa-camera-retro"}}---|CY-CBL-6P-DCHIP-02|CI0_0
            AtomOne4K_2{{"AtomOne4K_2 fa:fa-camera-retro"}}---|CY-CBL-6P-DCHIP-02|CI0_1
            AtomOne4K_3{{"AtomOne4K_3 fa:fa-camera-retro"}}---|CY-CBL-6P-DCHIP-02|CI0_1
            CV225_0{{"CV225_0 fa:fa-camera-retro"}}---|CY-CBL-6P-PFAN|CI0_2
            CV225_1{{"CV225_1 fa:fa-camera-retro"}}---|CY-CBL-6P-PFAN|CI0_2
            end
            subgraph PTZ
            AW-HE130_0{{"AW-HE130_0 fa:fa-camera-retro"}}---|Ethernet-RJ45|PassThru_1
            AW-HE130_1{{"AW-HE130_1 fa:fa-camera-retro"}}---|Ethernet-RJ45|PassThru_1
            AW-HE130_2{{"AW-HE130_2 fa:fa-camera-retro"}}---|Ethernet-RJ45|PassThru_1
            AW-HE130_3{{"AW-HE130_3 fa:fa-camera-retro"}}---|Ethernet-RJ45|PassThru_1
            BRC-H800_0{{"BRC-H800_0 fa:fa-camera-retro"}}---|Ethernet-RJ45|RIO_1
            BRC-H800_1{{"BRC-H800_1 fa:fa-camera-retro"}}---|Ethernet-RJ45|RIO_2
            end
            subgraph Shoulder Camcorder
            PXW-500_0{{"PXW-500_0 fa:fa-camera-retro"}}---|CY-CBL-SONY-8P-03|RIO-Live_2
            PXW-500_1{{"PXW-500_1 fa:fa-camera-retro"}}---|CY-CBL-SONY-8P-03|RIO-Live_3
            PXW-500_2{{"PXW-500_2 fa:fa-camera-retro"}}---|CY-CBL-SONY-8P-03|RIO-Live_4
            PXW-500_3{{"PXW-500_3 fa:fa-camera-retro"}}---|CY-CBL-SONY-8P-03|RIO-Live_5
            end
            subgraph DSLR
            Alpha7Mark4_0{{"Alpha7Mark4_0 fa:fa-camera-retro"}}---|USB-A-to-USB-C|PassThru_3
            FX3_0{{"FX3_0 fa:fa-camera-retro"}}---|USB-A-to-USB-C|PassThru_3
            end
            subgraph Large Sensor
            Burano_0{{"Burano_0 fa:fa-camera-retro"}}---|Ethernet-RJ45|RIO_5
            Burano_1{{"Burano_1 fa:fa-camera-retro"}}---|Ethernet-RJ45|RIO_6
            end
            subgraph "Control Room" 
            CI0_0 --- |Ethernet|MiniCameraSwitch
            CI0_1 --- |Ethernet|MiniCameraSwitch
            CI0_2 --- |Ethernet|MiniCameraSwitch
            PassThru_1 --- |Ethernet|PTZSwitch
            RIO_1 --- |Ethernet|PTZSwitch
            RIO_2 --- |Ethernet|PTZSwitch
            RIO-Live_2 --- |Ethernet|ShoulderCamcorderSwitch
            RIO-Live_3 --- |Ethernet|ShoulderCamcorderSwitch
            RIO-Live_4 --- |Ethernet|ShoulderCamcorderSwitch
            RIO-Live_5 --- |Ethernet|ShoulderCamcorderSwitch
            PassThru_3 --- |Ethernet|DSLRSwitch
            RIO_5 --- |Ethernet|LargeSensorSwitch
            RIO_6 --- |Ethernet|LargeSensorSwitch
            MiniCameraSwitch --- |Ethernet|CY-RCP-OCTO_0
            PTZSwitch --- |Ethernet|CY-RCP-OCTO-J_0
            ShoulderCamcorderSwitch --- |Ethernet|CY-RCP-DUO-J_0
            ShoulderCamcorderSwitch --- |Ethernet|CY-RCP-DUO-J_1
            ShoulderCamcorderSwitch --- |Ethernet|CY-RCP-DUO-J_2
            ShoulderCamcorderSwitch --- |Ethernet|CY-RCP-DUO-J_3
            DSLRSwitch --- |Ethernet|CY-RCP-DUO-J_4
            DSLRSwitch --- |Ethernet|CY-RCP-DUO-J_5
            LargeSensorSwitch --- |Ethernet|CY-RCP-DUO-J_6
            LargeSensorSwitch --- |Ethernet|CY-RCP-DUO-J_7
            end            
            """
        else:
            mermaid_code = code
        graph = Graph('example-flowchart',mermaid_code)
        mermaid_graph  = md.Mermaid(graph)
        return(mermaid_graph)
    def streamlit_mermaid(self,mermaid_graph):
        def render_svg(svg):
            b64 = base64.b64encode(svg.encode('utf-8')).decode('utf-8')
            html = r'<img src="data:image/svg+xml;base64,%s"/>' % b64
            return (html)
        svg_html = mermaid_graph._repr_html_()
        result = render_svg(svg_html) 
        return(result)
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

if __name__ == "__main__":
    instance = Instances()
    instance.debug_camerapool_to_instancepool()    
    instance.analyze()
    instance.draw_all()
    instance.top.render(filename='top_draw_all', format='svg')
    mermaid_code = instance.get_mermaid_code()
    print(mermaid_code)
    graph = instance.graph_mermaid(mermaid_code)
    instance.streamlit_mermaid(graph)
