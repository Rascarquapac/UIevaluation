import pandas as pd
from usecase import Usecase

################## ANALYZE #########################
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

def lens_init(self):
    self.df = pd.DataFrame.from_dict({
            'Camera Brand Motorized Lens':  [None, None], 
            'ENG Canon Lens': [None, 'CY-CBL-B4-01'],
            'ENG Fuji Lens': [None, 'CY-CBL-B4 et CY-CBL-FUJI-2'],
            'Cine Lens': ['external', 'CY-CBL-B4 et CY-CBL-FUJI-2'], 
            'Photo Lens': ['external', None]}, 
        orient = 'index')

Usecase.analyze = analyze
Usecase.device_from_cable   = device_from_cable
Usecase.device_from_network = device_from_network
Usecase.camgroup_from_cameratype=camgroup_from_cameratype
Usecase.device_id_from_device = device_id_from_device
Usecase.switch_id_from_camgroup = switch_id_from_camgroup
Usecase.rcptype_from_camgroup = rcptype_from_camgroup
Usecase.rcp_id_from_camgroup = rcp_id_from_camgroup
Usecase.rcp_optimize = rcp_optimize
Usecase.lens_init = lens_init