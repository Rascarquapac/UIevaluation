import re
import pickle 
from pool import Pool
from message import Messages
import pandas as pd

def codify_cameras():
    cameras = pd.read_csv("./data/CyanviewDescriptor - Cameras.csv",usecols=['Model','Reference','Protocol','Brand','ManufacturerURL','Remark'])
    cam_df  = pd.DataFrame(cameras)
    try:
        columns = cam_df.columns[cam_df.columns.duplicated(keep=False)]
        rows = cam_df.index[cam_df.index.duplicated(keep=False)]
        if not columns.empty :
            print("Duplicated Columns :\n",columns)
            raise Exception('Duplicated Columns in CyanviewDescriptor - Cameras.csv')
        if not rows.empty :
            print("Duplicated Rows :\n",rows)
            raise Exception('Duplicated Rows in CyanviewDescriptor - Cameras.csv')
    except Exception as e:
        print(str(e))
    protocols = pd.read_csv("./data/CyanviewDescriptor - CameraProtocols.csv",usecols=["Protocol","Brand","Type","Cable","SupportURL","Message","MaxDelayToComplete","ControlCoverage","Bidrectionnal"])
    proto_df = pd.DataFrame(protocols)
    del proto_df['Brand']
    pool_df = pd.merge(cam_df, proto_df, on = ['Protocol'],how = 'left').set_index('Model')
    # Add missing columns
    pool_df = pool_df.assign(Selected=False)
    pool_df = pool_df.assign(Number=0)
    pool_df = pool_df.assign(Lens='Fixed')
    pool_df = pool_df.assign(Network='LAN wired')
    pool_df = pool_df.assign(Base='Fixed')
    ## To suppress ??
    #df['Model'] = df.index
    pool_df.to_csv("./data/Generated_CameraDetails.csv")
    return (pool_df)

def codify_messages():
    message_dic = {}
    def store(topic,subtopic,message):
        if topic not in message_dic : message_dic[topic]={}
        if subtopic not in message_dic[topic]: message_dic[topic][subtopic]={}
        message_dic[topic][subtopic]=message

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
        return (message_dic)

def codify():
    df  = codify_cameras()
    df.to_pickle("cameras.pkl")

    dic = codify_messages()
    with open('messages.pkl', 'wb') as file:
        pickle.dump(dic, file)
if __name__ == "__main__":
    codify()
    