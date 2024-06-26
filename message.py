import csv
import re
from pool import Pool
from instance import Instances

class Messages():
    def __init__(self) -> None:
        self.dic={}
        self.load_messages()
        return
    def load_messages(self):
        def store(topic,subtopic,message):
            if topic not in self.dic : self.dic[topic]={}
            if subtopic not in self.dic[topic]: self.dic[topic][subtopic]={}
            self.dic[topic][subtopic]=message

        p  = re.compile("/\[(.*)\,(.*)\]")
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
                case 0: return "no"
                case 1|2: return "basic"
                case 3|4: return "nice"
                case 5: return "advanced"
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
                message += f"""
                The camera **{model}** ({reference}) offers a {control_message(controlcoverage)} control coverage.
                More information on cyanview support of the camera can be found on the [Cyanview support page for {model}]({supporturl}). The {brand} page for this camera is [{model}]({manufacturerurl}).

                """ 
        return(message)
if __name__ == "__main__":
    message=Messages()
    print(message.dic) 