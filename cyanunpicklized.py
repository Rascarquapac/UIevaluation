import pandas as pd
import pickle
# Extract picklized data and recreate objects
class Unpicklize:
    def __init__(self) -> None:
        self.cameras_df = pd.read_pickle("./picklized/cameras.pkl")
        with open('./picklized/properties.pkl', 'rb') as file:
            properties = pickle.load(file)        
        self.options     = properties["options"]
        self.constraints = properties["constraints"]   
        with open('./picklized/messages.pkl', 'rb') as file:
            self.messages_dic = pickle.load(file)        
        return
