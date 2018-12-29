import pandas as pd
from elasticsearch import Elasticsearch

df = pd.read_csv(filepath_or_buffer = "ten_servers_six_hours.csv")
#timestamp = 0
#source = 1
#level - 26
#Channel = 11
#SeverityValue=56
t=[]
s=[]
l=[]
ch=[]
sv=[]
m=[]
list_obj=['EventReceivedTime','source','Category','Channel','EventID','EventType','message','ProcessName','ObjectName','LogonProcessName','SeverityValue']

t = df[['EventReceivedTime']].values
s = df[['source']].values
evt_id = df[['EventID']].values
m = df[['message']].values
ch = df[['Channel']].values
sv = df[['SeverityValue']].values
cat = df[['Category']].values
evt_type=df[['EventType']].values
p_name=df[['ProcessName']].values
o_name=df[['ObjectName']].values
lpn=df[['LogonProcessName']].values
#print(m)
es = Elasticsearch([{'host': 'localhost', 'port': 9200}])
if es.ping():
    print('Yay Connect')
else:
    print('Awww it could not connect!')

for i in range(0,len(t)):
    print(cat[i][0])
    if pd.isnull(cat[i][0]):
        cat[i][0]='  '
    es.index(index='log', doc_type='windows', id=i, body={'timestamp':str(t[i][0]),'LogonProcessName':str(lpn[i][0]), 'ObjectName':str(o_name[i][0]),'EventID':str(evt_id[i][0]),'EventType':str(evt_type[i][0]),'ProcessName':str(p_name[i][0]),'source': s[i][0], 'message':m[i][0],'category':cat[i][0],'Channel':ch[i][0],'SeverityValue':str(sv[i][0])  })
