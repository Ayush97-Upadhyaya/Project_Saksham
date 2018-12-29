from elasticsearch import Elasticsearch
# from keras.utils import to_categorical
import csv
es = Elasticsearch([{'host': 'localhost', 'port': 9200}])
if es.ping():
  print('Yay Connect')
else:
  print('Awww it could not connect!')
#
# {"properties":{"message":{"type":"text","fielddata":true,"fields": {
#             "raw" : {
#               "type": "string",
#               "index": "not_analyzed"
#             }},"source":{"type":"text","fielddata":true,"fields": {
#             "raw" : {
#               "type": "string",
#               "index": "not_analyzed"
#             }},"category":{"type":"text","fielddata":true,"fields": {
#             "raw" : {
#               "type": "string",
#               "index": "not_analyzed"
#             }},"Channel":{"type":"text","fielddata":true,"fields": {
#             "raw" : {
#               "type": "string",
#               "index": "not_analyzed"
#             }},"EventType":{"type":"text","fielddata":true,"fields": {
#             "raw" : {
#               "type": "string",
#               "index": "not_analyzed"
#             }},"ProcessName":{"type":"text","fielddata":true,"fields": {
#             "raw" : {
#               "type": "string",
#               "index": "not_analyzed"
#             }},"ObjectName":{"type":"text","fielddata":true,"fields": {
#             "raw" : {
#               "type": "string",
#               "index": "not_analyzed"
#             }},"LogonProcessName":{"type":"text","fielddata":true,"fields": {
#             "raw" : {
#               "type": "string",
#               "index": "not_analyzed"
#             }}}}
# {"properties":
#     {"message":
#         {
#         "type":"text",
#         "fielddata":true,
#          "fields":{
#             "raw" : {
#               "type": "string",
#               "index": "not_analyzed"
#               }
#             }
# }
# }
# }

list_obj=['source','category','Channel','EventType','message','ProcessName','ObjectName','LogonProcessName',]
for field_agg in list_obj:

    res_severity_value =es.search(index="log",doc_type="windows", body={"aggs" : {"uniq_name" : {"terms" : { "field" : (field_agg+".keyword"),"size":"10000" }}},"size":"10000"})
    messages_=[]
    for result in res_severity_value['aggregations']['uniq_name']['buckets']:
        # sv_count.append(result['doc_count'])
        messages_.append(result['key'])
        # if field_agg=='category':
            # print("message : "+str(messages_))
    encode_={}
    len_msg = len(messages_)
    for i in messages_:
        encode=[]
        for j in range(0,len_msg):
            if i==messages_[j]:
                encode.append(1)
            else:
                encode.append(0)
        encode_.update({i:encode})
    #print(encode_)
    ########WWWWWWWWWWW
    with open(field_agg+'.csv', 'w', newline='') as outfile:
        writer = csv.writer(outfile)
        for i,j in encode_.items():
            # print(i)
            # print(j)
            writer.writerow([i,j])
