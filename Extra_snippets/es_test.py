from elasticsearch import Elasticsearch
es = Elasticsearch([{'host': 'localhost', 'port': 9200}])
if es.ping():
    print('Yay Connect')
else:
    print('Awww it could not connect!')



res =es.search(index="log",doc_type="windows", body={"query":{"wildcard" : { "timestamp" : "2018-12-05T03:54:58*" }},"from":0,"size":10,"aggs":{}})
len_total=res['hits']['total']
print(len_total)
x=[]
for hit in res['hits']['hits']:
    x.append(hit['_source'])
