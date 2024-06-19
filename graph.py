import pandas  as pd
from instance import Instances
class Drawing:
    def __init__(self,name = 'Cyanview',label = 'Cyanview') -> None:
        self.name  = name
        self.label = label
        self.layers = []
    def build_cameras(self,instance):
        camera_types = instance.df['Type'].unique()
        strate = Strate(kind = 'cameras', name='Camera Pool',label = 'Camera Pool')
        self.layers.append(strate) 
        for camtype in camera_types:
            camtype_df = self.df[(self.df['Type'] == camtype)]
            cluster = Cluster(kind = 'cameras', name = camtype, label = camtype)
            strate.clusters[camtype] = cluster 
            for instance in camtype_df.index:
                cluster.nodes[instance] = Node(instance,instance)
    def build_devices(self,instance):
        camera_types = instance.df['Type'].unique()
        strate = Strate(kind = 'devices', name='Devices Pool',label = 'Devices Pool')
        connexion = Connection()
        self.layers.append(strate) 
        for camtype in camera_types:
            camtype_df = self.df[(self.df['Type'] == camtype)]
            cluster = Cluster(kind = 'devices', name = camtype, label = camtype)
            strate.clusters[camtype] = cluster 
            for instance in camtype_df.index:
                device = camtype_df.loc[instance,'Device']
                cable  = camtype_df.loc[instance,'Cable']                
                device_id = device + camtype
                cluster.nodes[device] = Node(device,device_id)
                connexion.edges[instance] = Edge(cable+"_"+instance,cable,device_id,instance)


        
class Strate:
    def __init__(self,kind = None, name = 'Cyanview',label = 'Cyanview') -> None:
        self.kind  = kind
        self.name  = name
        self.label = label
        self.graph_attr = {'rankdir':'RL' ,'size':'6,3','style':'filled','color':'lightyellow'}
        self.node_attr  = {'shape'  :'box',             'style':'filled','color':'lightcyan1'}
        self.edge_attr  = {'fontsize':'6pt'}
        self.clusters = {}
        self.json     = {}
class Cluster:
    def __init__(self,kind = None, name = 'Cyanview',label = 'Cyanview') -> None:
        self.kind  = kind
        self.name  = name
        self.label = label
        self.nodes = {}
        
class Node: 
    def __init__(self,name = 'Cyanview',label = 'Cyanview') -> None:
        self.name  = name
        self.label = label
        self.attr  = {}
class Connection:
    def __init__(self,left_strate=None,right_strate=None) -> None:
        self.left_strate = left_strate
        self.right_strate = right_strate
        self.edges = {}
class Edge:
    def __init__(self,name, label,origin,destination) -> None:
        self.name = name
        self.label = label
        self.origin      = origin
        self.destination = destination

if __name__ == "__main__":
    instance = Instances()
    instance.debug_csv_to_instancepool()
    drawing = Drawing()
    drawing.build()