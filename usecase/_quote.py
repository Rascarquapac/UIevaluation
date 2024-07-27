# Count RCPs of each type for quoting
import pandas as pd

def rcp_count(self):
    self.rcps = {}
    rcp_ids = self.df['RCP_id'].unique()
    for rcp_id in rcp_ids:
        rcp_index  = self.df.loc[self.df['RCP_id'] == rcp_id].index.tolist()[0]
        rcp_type   = self.df.loc[rcp_index,'RCPtype']
        if rcp_type not in self.rcps: 
            self.rcps[rcp_type] = 1
        else:
            self.rcps[rcp_type] += 1
# Count Cables for quoting
def cable_count(self):
    self.cables = {}
    cable_types = self.df['Cable'].unique()
    for cable_type in cable_types:
        self.cables[cable_type] = self.df['Cable'].tolist().count(cable_type)
# Count devices for quoting
def device_count(self):
    self.devices = {}
    device_ids = self.df['Device_id'].unique()
    for device_id in device_ids:
        device_index  = self.df.loc[self.df['Device_id'] == device_id].index.tolist()[0]
        device_type   = self.df.loc[device_index,'Device']
        if device_type not in self.devices: 
            self.devices[device_type] = 1
        else:
            self.devices[device_type] += 1

