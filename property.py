import pandas as pd
import csv
import pickle

class Properties():
    def __init__(self) -> None:
        self.pkl_properties()
        # self.get_options()
        # self.get_constraints()
        #BEGIN: No more used …
        self.cameraTypes  = ['Slow Motion','Mini Camera','PTZ','Shoulder Camcorder',
                              'Handheld Camcorder','Block','DSLR','System','Large Sensor','Unknown'] 
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
        #END: No more used ...

    def pkl_properties(self):
        with open('./picklized/properties.pkl', 'rb') as file:
            properties = pickle.load(file)        
        self.options     = properties["options"]
        self.constraints = properties["constraints"]   
        return

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
            # print(f'Processed {line_count} lines.')
            # print(self.options)
            # for key in self.options:
                # print("\n\n",key," : ",self.options[key])

    def get_constraints(self):
        self.constraints = {}
        constraints_df = pd.read_csv("./data/CyanviewDescriptor - Constraints.csv",header = [0,1])
        self.constraints_df = pd.DataFrame(constraints_df)
        constraints_dict = self.constraints_df.to_dict()
        for key,dico in constraints_dict.items():
            # print("\nRow Dict: ", dico)
            listFromDict = []
            for index,value in dico.items():
                if not (value != value):
                    listFromDict.append(value)
            # print("Row list: ",listFromDict)
            constraints_dict[key] = listFromDict.copy()
        self.constraints = constraints_dict
        # print(list(constraints_dict.keys()))
        # print(constraints_dict[('Slow Motion', 'Network')])
        # print(constraints_dict)



if __name__  == "__main__":
    test = Properties()
    test.get_constraints()