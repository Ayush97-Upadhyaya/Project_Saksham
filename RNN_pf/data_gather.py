from elasticsearch import Elasticsearch
es = Elasticsearch([{'host': 'localhost', 'port': 9200}])
if es.ping():
    print('Yay Connect')
else:
    print('Awww it could not connect!')

res =es.search(index="log",doc_type="windows", body={"query":{"bool":{"must":[{"match_all":{}}],"must_not":[],"should":[]}},"from":0,"size":50000,"sort":[],"aggs":{}})
x=[]
df=[]
for hit in res['hits']['hits']:
    x.append(hit['_source'])
print(x)
df=json_normalize(x)

export_csv = df.to_csv (r'H:\PS2\RNN\data_rnn_train.csv', index = None, header=True)
