from elasticsearch import Elasticsearch
# from keras.utils import to_categorical
import csv
es = Elasticsearch([{'host': 'localhost', 'port': 9200}])
if es.ping():
  print('Yay Connect')
else:
  print('Awww it could not connect!')
res_severity_value =es.search(index="log",doc_type="windows", body={"aggs" : {"uniq_name" : {"terms" : { "field" : "message.keyword" }}},"size":"0"})
#print(res_severity_value)



x="C:\\Windows\\Microsoft.NET\\Framework64\\v4.0.30319\\Temporary ASP.NET Files\\onlineptw\\cc009542\\65aa50ea\\uploads\\fxeixwhj.post"
y=x.split("\\")
print(y)
