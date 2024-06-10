## From a descriptor dataframe analyse requirements and provide text, FAQ links and graphs
import pandas as pd
from instance import Instances
from camera import Camera

class Analyze():
    def __init__(self,df) -> None:
        print("###########-> DATAFRAME TO ANAYZE:")
        print(df)
        self.df = df
        self.devices = {
            "cio":[],
            "rio_live":[],
            "rio":[],
            "rsbm":[],
            "nio":[],
            "tally":[],
            "rcp":[],
            }
        # Uncomment to get a test file… and rename it to InstanceDataframe.csv when created
        # self.df.to_csv("./data/selected_cameras.csv")
        self.cameraTypes  = ['Slow Motion','Mini Camera','PTZ','Shoulder Camcorder',
                              'Handheld Camcorder','Block','DSLR','System','Large Sensor']         
        self.df['Device'] = ""
        self.df['Connected'] = False
        #instance= Instances(df)
        #instance.display_camera_table()
        self.consume_ci0()
        self.consume_rio_live()
        self.consume_rio()
        self.consume_rsbm()
        self.consume_tally()
        self.consume_rcp()

    def consume_ci0(self):
        pass
    def consume_rio_live(self):
        pass
    def consume_rio(self):
        pass
    def consume_rsbm(self):
        pass
    def consume_nio(self):
        pass
    def consume_tally(self):
        pass
    def consume_rcp(self):
        pass
    def add_IPconverter(self):
        def ipinterface(network='LAN wired',cable='Ethernet-RJ45',maxlatency='medium'):
            if network == 'LAN wired' :
                if cable[0:7] == "CY-CBL-" :
                    return("CI0")
                else:
                    return("PassThru")
            elif network == 'LAN RF' :
                ## Ccheck dealy sensistivity of camera to decide RIO-Live or CI0
                if cable[0:7] == "CY-CBL-" :
                    return("CI0")
                else:
                    return("PassThru")
            elif network == "WAN wired":
                return["RIO"]
            else:
                return ("CHECK")
 
        print("###########-> DATAFRAME LAN_wired: ")
        print(self.df)
        types  = self.df['Type'].unique()
        print("Unique values in Type columns:", types)
        self.df['Device'] = self.df.apply(lambda row: ipinterface(row['Network'],row['Cable']), axis=1)
        print(self.df[['Instance','Model','Type','Network','Cable','Device']])    

    def gear_number(self):
        for cameraType in self.cameraTypes:
            devices = self.df.apply(lambda row: 1 if (row['Type'] == cameraType and row['Device'] == "CI0") else 0, axis=1)
            print("# of devices of type ",cameraType,": ", devices.sum())
    def reference_explanation(self):
        # store in a  dict with camera Model as key the standard explanation for this choice 
        # Can be done in set_IP_Interface…
        pass

if __name__ == "__main__":
    df = pd.read_csv("./data/InstanceDataframe.csv")
    print(df)
    analyze = Analyze(df)
    analyze.add_IPconverter()    
    analyze.gear_number()