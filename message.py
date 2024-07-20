import csv
import re
import pickle
from pool import Pool
from usecase import Usecase

class Messages():
    def __init__(self) -> None:
        self.dic={}
        self.pkl_messages()
        return
    def pkl_messages(self):
        with open('./picklized/messages.pkl', 'rb') as file:
            self.dic = pickle.load(file)        
        return
    def display(self,object=None, subtopic=""):
        if isinstance(object,Pool):
            return self.cameras(object.selected)
        elif isinstance(object,Usecase):
            search_topic    = "instance"
            search_subtopic = "general" if subtopic == "" else subtopic
            message = self.dic[search_topic][search_subtopic]
            return(message)
        else:
            return("No Information for unknown object")
    def cameras(self,df):
        def control_message(controlLevel):
            match controlLevel:
                case 0: return "no control"
                case 1|2: return "a basic control"
                case 3|4: return "a good control"
                case 5: return "an advanced control"
                case _: return "to be defined"
        message = ""
        if df.empty:
            message = ""
        else:
            print(df)
            print(df.columns)
            for camera in df.index.to_list():
                model = camera
                reference = df.loc[camera,'Reference']
                controlcoverage = df.loc[camera,"ControlCoverage"]
                supporturl = df.loc[camera,"SupportURL"]
                brand = df.loc[camera,"Brand"]
                manufacturerurl = df.loc[camera,"ManufacturerURL"]
                message += self.dic['camera']['performance'].format(model=model,reference=reference,control=control_message(controlcoverage),
                                                                   supporturl=supporturl,brand=brand,manufacturerurl=manufacturerurl)
                message += "\n"
                if (df.loc[camera,'Bidirectionnal']) == "No":
                    message += ("\n" + self.dic['camera']['unidirectional'])
        return(message)
if __name__ == "__main__":
    message=Messages()
    print(message.dic) 