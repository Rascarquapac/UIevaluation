import pandas as pd
import csv
import pickle

class Properties():
    def __init__(self) -> None:
        self.pkl_properties()
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