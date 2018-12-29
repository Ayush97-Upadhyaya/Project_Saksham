from elasticsearch import Elasticsearch
_es = Elasticsearch([{'host': 'localhost', 'port': 9200}])
if _es.ping():
    print('Yay Connect')
else:
    print('Awww it could not connect!')

res = _es.get(index="test",doc_type="1",id="kahNL2cBqmVQe9oY-NdY")
print(res['_source'])
