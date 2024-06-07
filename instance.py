import streamlit as st
import pandas as pd
import csv

class Instances:
    def __init__(self,df=None) -> None:
        self.df = pd.DataFrame(df)
        self.columns_name = df.columns.values
        self.df.index.name = 'instance'     
        self.property = Properties()   
        return 

    def camera_lens_init(self,cameras):
        print("################### DEBUG CAMERA_LENS_INIT#######################")
        print("CAMERAS DATAFRAME")
        print(cameras.df)
        camera_lens_dict = {}
        print("List of cameras",cameras.df.index.to_list())
        if not cameras.df.empty:
            for camera_index in cameras.df.index.to_list():
                print("NUMBER VALUE:---> ", cameras.df.loc[camera_index,'number'],)
                for i in range(int(cameras.df.loc[camera_index,'number'])):
                    new_index = camera_index + "_" + str(i) 
                    print(new_index)
                    print(cameras.df.loc[camera_index])
                    variables = []
                    variables.extend(cameras.df.loc[camera_index].tolist())
                    # variables.extend(['Fixed','Wired Lan','Fixed'])
                    print(variables)
                    #camera_lens_dict[new_index] = [camera_index].extend(variables)
                    camera_lens_dict[new_index] = list(variables)
            self.df = pd.DataFrame.from_dict(camera_lens_dict, orient = 'index', columns = self.columns_name)
            self.df.index.name = 'instance'        


        print("\n\nCAMERA LENS DATAFRAME :")
        print(self.df)

    def lens_init(self):
        self.df = pd.DataFrame.from_dict({
                'Camera Brand Motorized Lens':  [None, None], 
                'ENG Canon Lens': [None, 'CY-CBL-B4-01'],
                'ENG Fuji Lens': [None, 'CY-CBL-B4 et CY-CBL-FUJI-2'],
                'Cine Lens': ['external', 'CY-CBL-B4 et CY-CBL-FUJI-2'], 
                'Photo Lens': ['external', None]}, 
            orient = 'index')
        
    def display_camera_table(self):
        print("DEBUG:cyaneval->display_camera_table ...")
        if (len(self.df.index) != 0):
            st.dataframe(
                self.df,
                column_config={
                    "selected": "Is Selected",
                    "number":st.column_config.NumberColumn(
                        "# of Cams",
                        help="How much camera of this type in your use-case (0-15)?",
                        min_value=0,
                        max_value=15,
                        step=1,
                        format="%d",
                    ),
                    "Model": "Model",
                    "Brand": "Brand",
                    "Cable": "Cable",
                    "lens": "Lens Type",
                    "network": None,
                    "base": None,
                    "SupportURL": None,
                    "ManufacturerURL": None,
                    "Reference": None,
                    #"supportText": None,
                    "Protocol":None,
                    "Message":None,
                    "Type":None
                },
                column_order=['Model','instance','network','lens','base'],
                hide_index = True)

    def edit_camera_table(self,key='1'):
        # Validate inputs
        if (len(self.df.index) != 0): 
            # display = self.text_message()
            self.df = st.data_editor(
                self.df,
                key = key,
                column_config={
                    "instance": "Instance",
                    "number":st.column_config.NumberColumn(
                        "# Cams",
                        help="How much camera of this type in your use-case (0-15)?",
                        min_value=0,
                        max_value=15,
                        step=1,
                        default=0,
                        format="%d",
                    ),
                    "Model": "Model",
                    "lens": st.column_config.SelectboxColumn(
                        "Lens",
                        help="Lens type",
                        width="medium",
                        options= self.property.constraints[(key,'Lens')],
                        required=True),
                    "network":  st.column_config.SelectboxColumn(
                        "Network",
                        help="Select the network type",
                        width="medium",
                        options=self.property.constraints[(key,'Network')],
                        required=True),
                    "base":  st.column_config.SelectboxColumn(
                        "Basement",
                        help="Base type",
                        width="medium",
                        options=self.property.constraints[(key,'Base')],
                        required=True),
                    "Brand": None,
                    "Cable": None,
                    "selected": None,
                    "SupportURL": None,
                    "ManufacturerURL": None,
                    "Reference": None,
                    #"supportText": None,
                    "Protocol":None,
                    "Message":None,
                    "Type":None
                },
                disabled=['selected','number','cable'],
                column_order=['Model','instance','network','lens','base'],
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

class Properties():
    def __init__(self) -> None:
        self.get_options()
        self.get_constraints()
        self.cameraTypes  = ['Slow Motion','Mini Camera','PTZ','Shoulder Camcorder',
                              'Handheld Camcorder','Block','DSLR','System','Large Sensor'] 
        self.description = {
            'Slow Motion': {
                'lenses'  : ["Fixed","B4 ENG"],
                'networks': self.options["NetworkTypes"],
                'bases'   : self.options["BaseTypes"]},
            'Mini Camera': {
                'lenses'  : ["Fixed","Internal","Camera integrated"],
                'networks': self.options["NetworkTypes"],
                'bases'   : self.options["BaseTypes"]},
            'PTZ': {
                'lenses'  : ["Internal"],
                'networks': self.options["NetworkTypes"],
                'bases'   : self.options["BaseTypes"]},
            'Shoulder Camcorder': {
                'lenses'  : ['Fixed',"Camera integrated"],
                'networks': self.options["NetworkTypes"],
                'bases'   : self.options["BaseTypes"]},
            'Handheld Camcorder': {
                'lenses'  : ['Fixed',"Camera integrated"],
                'networks': self.options["NetworkTypes"],
                'bases'   : self.options["BaseTypes"]},
            'Block': {
                'lenses'  : ['Fixed',"B4 ENG","Camera integrated"],
                'networks': self.options["NetworkTypes"],
                'bases'   : self.options["BaseTypes"]},
            'DSLR': {
                'lenses'  : ['Fixed',"Camera integrated"],
                'networks': self.options["NetworkTypes"],
                'bases'   : self.options["BaseTypes"]},
            'System': {
                'lenses'  : ["Camera integrated"],
                'networks': self.options["NetworkTypes"],
                'bases'   : self.options["BaseTypes"]},
            'Large Sensor': {
                'lenses'  : self.options["LensTypes"],
                'networks': self.options["NetworkTypes"],
                'bases'   : self.options["BaseTypes"]},
            }
        print(self.options)

    def get_options(self):
        self.options = {}
        with open('./data/CyanviewDescriptor - Options.csv', mode='r') as csv_file:
            #csv_reader = csv.reader(csv_file, delimiter=',')
            csv_reader = csv.reader(csv_file)
            line_count = 0
            for row in csv_reader:
                if line_count == 0:
                    baseKeys = row
                elif line_count == 1:
                    suffixKeys = row
                    self.keyOrder = []
                    self.columnsNumber = len(row)
                    for i in range(self.columnsNumber):
                        key = baseKeys[i] + suffixKeys[i]
                        self.options[key]=[]
                        self.keyOrder.append(key)
                else:
                    for i in range(len(row)):
                        if row[i] != "":
                            self.options[self.keyOrder[i]].append(row[i])
                line_count += 1
            print(f'Processed {line_count} lines.')
            print(self.options)
            for key in self.options:
                print("\n\n",key," : ",self.options[key])

    def get_constraints(self):
        self.constraints = {}
        constraints_df = pd.read_csv("./data/CyanviewDescriptor - Constraints.csv",header = [0,1])
        self.constraints_df = pd.DataFrame(constraints_df)
        constraints_dict = self.constraints_df.to_dict()
        for key,dico in constraints_dict.items():
            print("\nRow Dict: ", dico)
            listFromDict = []
            for index,value in dico.items():
                if not (value != value):
                    listFromDict.append(value)
            print("Row list: ",listFromDict)
            constraints_dict[key] = listFromDict.copy()
        self.constraints = constraints_dict
        print(list(constraints_dict.keys()))
        print(constraints_dict[('Slow Motion', 'Network')])
        print(constraints_dict)



if __name__  == "__main__":
    test = Properties()
    test.get_constraints()