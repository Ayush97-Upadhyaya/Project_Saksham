import csv
import pandas
import es_
from pandas.io.json import json_normalize


list_obj=['timestamp','source','category','Channel','EventID','EventType','message','ProcessName','ObjectName','LogonProcessName','SeverityValue']


list_obj_=['source','category','Channel','EventType','message','ProcessName','ObjectName','LogonProcessName',]


# def one_hot_data():
source={}
category={}
Channel={}
EventType={}
message={}
ProcessName={}
ObjectName={}
LogonProcessName={}
for field_agg in list_obj_:
    with open(field_agg+'.csv', newline='') as myFile:
        reader = csv.reader(myFile)
        for row in reader:
            # print(row)
            if field_agg=='source':
                if row[0]:
                    source.update({row[0]:row[1]})
                else:
                    source.update({"s":row[1]})
            elif field_agg=='category':
                if row[0]:
                    category.update({row[0]:row[1]})
                else:
                    category.update({"c":row[1]})
            elif field_agg=='Channel':
                Channel.update({row[0]:row[1]})
            elif field_agg=='message':
                message.update({row[0]:row[1]})
            elif field_agg=='ProcessName':
                ProcessName.update({row[0]:row[1]})
            elif field_agg=='ObjectName':
                # print({row[0]:row[1]})
                ObjectName.update({row[0]:row[1]})
            elif field_agg=='LogonProcessName':
                LogonProcessName.update({row[0]:row[1]})
            elif field_agg=='EventType':
                EventType.update({row[0]:row[1]})

# # print(asd)
# print(ObjectName)
results = es_.get_es_all()
dff=json_normalize(results)
df=dff[list_obj].fillna(dff.mean())

cols_name=dff.columns.values
df_len = df.shape

df.to_csv("df.csv")

for i in range(0,df_len[0]):
    t=df.at[i,"timestamp"]
    tft=t.split(' ')
    print(tft)
    df.at[i,"timestamp"]=tft[1]
    for field_agg in list_obj_:
        # print(field_agg)
        x=df.at[i,field_agg]
        #x=x.lower()
        #print('x : '+x)
        if field_agg=='source':
            df.at[i,field_agg]=source[x]
        elif field_agg=='category':
            df.at[i,field_agg]=category[x]
        elif field_agg=='Channel':
            df.at[i,field_agg]=Channel[x]
        elif field_agg=='message':
            df.at[i,field_agg]=message[x]
        elif field_agg=='ProcessName':
            df.at[i,field_agg]=ProcessName[x]
        elif field_agg=='ObjectName':
            # y=x.split("\\")
            # key_y=""
            # for i in range(0,len(y)):
            #     if i==0:
            #         key_y=key_y+y[i]
            #     else:
            #         key_y=key_y+str("\"")+y[i]
            df.at[i,field_agg]=ObjectName[x]
        elif field_agg=='LogonProcessName':
            df.at[i,field_agg]=LogonProcessName[x]
        elif field_agg=='EventType':
            df.at[i,field_agg]=EventType[x]
l3 = [x for x in list_obj if x not in list_obj_]
for i in range(0,df_len[0]):
    for z in l3:
        t=df.at[i,z]
        df.at[i,z]=int(t)
    for j in cols_name:
        if df.at[i,j]:
            continue
        else:
            df.at[i,j]=''

# print(df)
    # return df
