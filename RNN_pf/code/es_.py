
from elasticsearch import Elasticsearch

def get_es_all():
    es = Elasticsearch([{'host': 'localhost', 'port': 9200}])
    if es.ping():
      print('Yay Connect')
    else:
      print('Awww it could not connect!')

    results = es.search(index="log",doc_type="windows", body={"query":{"bool":{"must":[{"match_all":{}}],"must_not":[],"should":[]}},"from":0,"size":10000,"sort":[],"aggs":{}})
    # {"timestamp":{"order":"desc"}}
    x=[]
    for i in results['hits']['hits']:
        x.append(i['_source'])
    del(results)
    return x
