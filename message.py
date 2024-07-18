import csv
import re
import pickle
from pool import Pool
from instance import Instances

class Messages():
    def __init__(self) -> None:
        self.dic={}
        self.pkl_messages()
        #self.load_messages()
        return
    def pkl_messages(self):
        with open('./picklized/messages.pkl', 'rb') as file:
            self.dic = pickle.load(file)        
        return
    def load_messages(self):
        def store(topic,subtopic,message):
            if topic not in self.dic : self.dic[topic]={}
            if subtopic not in self.dic[topic]: self.dic[topic][subtopic]={}
            self.dic[topic][subtopic]=message

        p  = re.compile(r"/\[(.*)\,(.*)\]")
        message = ""
        with open('./data/Messages.md', 'r') as reader:
            line = reader.readline()
            print("Line: ",line)
            first_line = True
            while line != '':  # The EOF char is an empty string
                if line[0:2]== "/[":
                    if first_line:
                        # No message to store
                        first_line = False
                    else:
                        # Store currently collected message
                        store(topic,subtopic,message)
                        message = ""
                    result   = p.search(line)
                    topic    = result.group(1)
                    subtopic = result.group(2)
                else:
                    message += line
                    # print("Keys: ",context, state,name)
                    # print("Message: ",message)
                line = reader.readline()
            # Store last message
            store(topic,subtopic,message)           
        return
    def display(self,object=None, subtopic=""):
        if isinstance(object,Pool):
            return self.cameras(object.selected)
        elif isinstance(object,Instances):
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
            message = "No camera selected"
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
                message = self.dic['camera']['performance'].format(model=model,reference=reference,control=control_message(controlcoverage),
                                                                   supporturl=supporturl,brand=brand,manufacturerurl=manufacturerurl)
                if (df.loc[camera,'Bidrectionnal']) == "No":
                    message += ("\n" + self.dic['camera']['unidirectional'])
        return(message)
if __name__ == "__main__":
    message=Messages()
    print(message.dic) 