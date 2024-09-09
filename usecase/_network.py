import pandas as pd
from constants import CameraLensDevice

class DevicesStatus():
    def __init__(self):
        self.ci0      = {'current_instance':0,'consumed_connections':0,'max_connections':2  ,'instanciated':False,'name':"CI0"}
        self.rio      = {'current_instance':0,'consumed_connections':0,'max_connections':2  ,'instanciated':False,'name':"RIO"}
        self.rio_live = {'current_instance':0,'consumed_connections':0,'max_connections':2  ,'instanciated':False,'name':"RIO-LIVE"}
        self.rsbm     = {'current_instance':0,'consumed_connections':0,'max_connections':8  ,'instanciated':False,'name':"RSBM"}
        self.ip       = {'current_instance':0,'consumed_connections':0,'max_connections':100,'instanciated':False,'name':"IP"}
        # update devices status when changing camgroup
    def camgroup_update(self):
        for attribute, status in vars(self).items():
            if status['instanciated']:
                status['current_instance'] += 1
                status['consumed_connections'] = 0
            status['instanciated'] = False
    # A new camera row is processed, update the devices_status
    def get_device_id (self,device,fanout):
        device_status = self.__dict__[device]
        device_status['instanciated'] = True
        if (device_status['consumed_connections'] + fanout) <= device_status['max_connections']:
            # Change only the consumed_connections
            device_status['consumed_connections'] += fanout
        else:
            # Create a new instance and set consumed connections to row fanout
            device_status['consumed_connections'] = fanout
            device_status['current_instance']    += 1
        return (device_status["name"] + "_" + str(device_status['current_instance']))

################## ANALYZE #########################
# Select the converter for each camera and set it in "Device" index. A Specific column could be more appropriate
def device_from_camera_lens(self):
    # A cable type is already associated to the camera model
    # The function return "CI0" if a serial converter is required or "Passthru"
    def select(camera_cable,lens_cable,motor_cable):
        if lens_cable[0:7]     == "CY-CBL-" : return CameraLensDevice.RIO_LIVE.value
        elif motor_cable[0:7]  == "CY-CBL-" : return CameraLensDevice.RIO_LIVE.value
        elif camera_cable[0:7] == "CY-CBL-" : return CameraLensDevice.CI0.value
        else: pass
        # IP "passthrough" pseudo device
        match camera_cable:
            case "Ethernet-RJ45"  : return CameraLensDevice.IP.value
            case "USB-A-to-USB-C" : return CameraLensDevice.IP.value
            case "IP-to-USB-C"    : return CameraLensDevice.IP.value
            case "BM-SDI"         : return CameraLensDevice.IP.value
            case "JVC USB-to-IP"  : return CameraLensDevice.IP.value 
            case "XDCA back"      : return CameraLensDevice.IP.value 
            case _                : return CameraLensDevice.IP.value 
    self.df['Device'] = self.df.apply(lambda row: select(row['Cable'],row['LensCable'],row['MotorCable']), axis=1)
# Set the fanout of converter device
def device_fanout(self):
    # A cable type is already associated to the camera model
    # The function return "CI0" if a serial converter is required or "Passthru"
    def fanout(camera_cable,lens_cable,motor_cable):
        fanout = 0
        if camera_cable != "No cable" : fanout += 1
        if lens_cable   != "No cable" : fanout += 1
        if motor_cable  != "No cable" : fanout += 1
        # if lens_cable[0:7]   == "CY-CBL-" : fanout += 1
        # if camera_cable[0:7] == "CY-CBL-" : fanout += 1
        return fanout
    self.df['Fanout'] = self.df.apply(lambda row: fanout(row['Cable'],row['LensCable'],row['MotorCable']), axis=1)
# Select the device from network for each camera and set it in "Device" column.
def device_from_network(self):
    # Select the device from network associated to the camera
    def select(current_device,network,MaxDelayToComplete):
        assert current_device in [member.value for member in CameraLensDevice]
        #TODO: add a check between case values and contraints
        match network:
            case "LAN Wired" : return current_device
            case "LAN RF Halow"    :
                if  MaxDelayToComplete < 200:
                    return CameraLensDevice.RIO_LIVE.value
                else: 
                    return current_device
            case "LAN RF Mesh"    :
                if  MaxDelayToComplete < 200:
                    return CameraLensDevice.RIO_LIVE.value
                else: 
                    return current_device
            case "LAN RF WiFi"    :
                if  MaxDelayToComplete < 200:
                    return CameraLensDevice.RIO_LIVE.value
                else: 
                    return current_device
            case "P2P RF Pro Modem"    :
                if  MaxDelayToComplete < 200:
                    return CameraLensDevice.RIO_LIVE.value
                else: 
                    return current_device
            case "P2P RF Unidir"    :
                if  MaxDelayToComplete < 200:
                    return CameraLensDevice.RIO_LIVE.value
                else: 
                    return current_device
            case "WAN 4G 5G" : return CameraLensDevice.RIO.value
            case "P2MP UHF Video"  : return CameraLensDevice.RIO_LIVE.value
            case _           : return CameraLensDevice.UNDEFINED.value
        return
    self.df['Device'] = self.df.apply(lambda row: select(row['Device'],row['Network'],row['MaxDelayToComplete']), axis=1)
# Set the "Camgroup" column with the "Camtype" value: the camera groups are based on camera type 
def camgroup_from_cameratype(self):
    def select(camtype,network):
        return camtype
    self.df['Camgroup'] = self.df.apply(lambda row: select(row['Type'],row['Network']), axis=1)
# According to device fanout and the camera camgroup instanciate devices and add instance number
def device_id_from_device(self):
    devices_status = DevicesStatus()
    camgroups = self.df['Camgroup'].unique() 
    for camgroup in camgroups:
        # update_status(devices_status)
        camgroup_indexes  = self.df.loc[self.df['Camgroup'] == camgroup].index.tolist() 
        # print("Camgroup:",camgroup)
        for index in camgroup_indexes:
            device = self.df.loc[index,'Device']
            fanout = self.df.loc[index,'Fanout']
            self.df.loc[index,'Device_id'] = devices_status.get_device_id(device,fanout)
            print(f'usecase-->_network-->get_device_id->device_status=\n{devices_status.__dict__[device]}\n Fanout = {fanout}')
            value = (self.df.loc[index,'LensCable'],self.df.loc[index,'MotorCable'],self.df.loc[index,'LensMotor'])
            print(f'CABLES: {value}\n')
        # camgroup_update_status(devices_status)
        devices_status.camgroup_update()
            # print("    Device_id    : ",self.df.loc[index,'Device_id'])
            # print("    Device Status: ",devices_status)
# Add one switcher per camera group
def switch_id_from_camgroup(self):
    self.df['Switch_id'] = self.df.apply(lambda row: row['Camgroup'] + " Switch", axis=1)
# Select the RCP type based on the camera group
def rcptype_from_camgroup(self):
    def select(camgroup):
        match camgroup:
            case 'Slow Motion': return("RCP") 
            case 'Mini Camera': return("RCP") 
            case 'PTZ': return("RCP-J") 
            case 'Shoulder Camcorder': return("RCP-DUO-J") 
            case 'Handheld Camcorder': return("RCP-DUO-J") 
            case 'BBlock': return("RCP-DUO-J") 
            case 'Mirrorless': return("RCP-DUO-J") 
            case 'System': return("RCP-DUO-J") 
            case 'CineStyle': return("RCP-DUO-J") 
            case 'Unknown': return("RCP")
            case _: return("RCP")
        return
    self.df['RCPtype'] = self.df.apply(lambda row: select(row['Camgroup']), axis=1)    
# According to fanins in a camera group set RCP_instances
def rcp_id_from_camgroup(self):
    def get_rcp_id(rcps_status,RCPtype):
        try:
            (number,port,maxconnect,camgroup_instanciated) = rcps_status[RCPtype]
        except:
            print(f"RCP of type {RCPtype} not defined")
            raise
        camgroup_instanciated = True
        if port < maxconnect : 
            port += 1
        else : 
            number += 1
            port = 1
        rcps_status[RCPtype] = (number,port,maxconnect,camgroup_instanciated)
        return ("CY-" + RCPtype + "_" + str(number))
    
    rcps_status = {"RCP":(0,0,200,False),"RCP-J":(0,0,200,False),"RCP-DUO-J":(0,0,1,False)}
    camgroups   = self.df['Camgroup'].unique() 
    #self.df.to_csv('./debug_unknown_cameras.csv')
    for camgroup in camgroups:
        camgroup_indexes  = self.df.loc[self.df['Camgroup'] == camgroup].index.tolist() 
        for index in camgroup_indexes:
            self.df.loc[index,'RCP_id'] = get_rcp_id(rcps_status,self.df.loc[index,'RCPtype']) 
            value = self.df.loc[index,'RCP_id']
            print(f'!!!!RCP_ID: {value}')
        print(f"CAMGROUPS: {camgroup}, RCPS_STATUS: {rcps_status}")
        for key in rcps_status:
            (number,port,maxconnect,camgroup_instanciated) = rcps_status[key]
            if camgroup_instanciated :
                port = 0
                camgroup_instanciated = False
                number += 1
            rcps_status[key] = (number,port,maxconnect,camgroup_instanciated)
        print(f"END CAMGROUPS: {camgroup}, RCPS_STATUS: {rcps_status}")


        
# Optimize the number of RCPs required
def rcp_optimize(self):
    def get_rcptype_rcp_id(current_RCP,occurences):
        if current_RCP[0:12] == "CY-RCP-DUO-J": 
            rcptype = "CY-RCP-DUO-J"
            postfix = current_RCP[12:]
        elif current_RCP[0:8] == "CY-RCP-J":
            postfix =  current_RCP[8:]
            if occurences < 3 : 
                rcptype = "CY-RCP-DUO-J_"
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
            #??self.df.loc[index,'RCPtype'] = RCPtype 
