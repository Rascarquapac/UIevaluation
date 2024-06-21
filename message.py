import csv
import re
class Messages():
    def __init__(self) -> None:
        self.dic={}
        self.load_messages()
        pass
    def load_messages(self):
        def store(context,state,name,message):
            if context not in self.dic : self.dic[context]={}
            if state not in self.dic[context]: self.dic[context][state]={}
            if name not in self.dic[context][state]: self.dic[context][state][name]={}
            self.dic[context][state][name]=message

        p  = re.compile("/\[(.*)\,(.*)\,(.*)\]")
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
                        store(context,state,name,message)
                        message = ""
                    result = p.search(line)
                    context = result.group(1)
                    state = result.group(2)
                    name = result.group(3)
                else:
                    message += line
                    # print("Keys: ",context, state,name)
                    # print("Message: ",message)
                line = reader.readline()
            # Store last message
            store(context,state,name,message)           
        return
    def cameras(self,df):
        pass        
if __name__ == "__main__":
    message=Messages()
    print(message.dic) 