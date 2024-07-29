import graphviz as gv
import base64
import mermaid as md
from   mermaid.graph import Graph

#################### DRAW WITH GRAVVIZ ###########################
def init_graph(self,name,rank='sink'):
    graph = gv.Graph(name='cluster_' + name)
    graph.attr(rankdir='RL', size='6,3',style='filled',color='lightyellow',label=name,rank=rank)
    graph.node_attr.update(style='filled',shape= 'box',color='lightcyan1')
    graph.edge_attr.update(fontsize='8pt')
    return(graph)
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
        RCPtype    = switch_df['RCPtype'].unique()[0]
        switches  = switch_df['Switch_id'].unique()
        for switch in switches:
            top.node(name=rcp,label=RCPtype)
            top.edge(switch+":w",rcp+":e","Ethernet Link")
    # top.subgraph(croom)
    self.top =top
    return(top)
#################### DRAW WITH MERMAID ###########################
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
        switches  = switch_df['Switch_id'].unique()
        for switch in switches:
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

