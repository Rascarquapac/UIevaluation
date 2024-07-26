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


if __name__  == "__main__":
    test = Properties()
    test.pkl_properties()