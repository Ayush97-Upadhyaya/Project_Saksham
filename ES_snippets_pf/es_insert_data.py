from elasticsearch import Elasticsearch
es = Elasticsearch([{'host': 'localhost', 'port': 9200}])
if es.ping():
    print('Yay Connect')
else:
    print('Awww it could not connect!')
name_list=['a','b','c','d','e','f','g','h','i','j']
occupation_list=['a0','b0','c0','d0','e0','f0','g0','h0','i0','j0']
test_list=['a1','b1','c1','d1','e1','f1','g1','h1','i1','j1']
#
for i in range(0,10):
    element={
        'name':name_list[i],
        'occupation':occupation_list[i],
        'id':i,
        'test':test_list[i]
    }
    print(i)
    print(element)
    es.index(index="test",doc_type="1", body=element)

res =es.search(index="test",doc_type="1", body={"query":{"bool":{"must":[{"match_all":{}}],"must_not":[],"should":[]}},"from":0,"size":100,"sort":[],"aggs":{}})
x=[]
for hit in res['hits']['hits']:
    x.append(hit['_source'])
print(x)

# es.delete_by_query(index="test",doc_type="1",body={
#
#     "query": {
#         "bool": {
#             "must": [
#                 {
#                     "term": {
#                         "test.keyword": 'Adnan '
#
#                     }
#                 }
#             ],
#             # "must_not": [ ],
#             # "should": [ ]
#         }
#     },
#     # "from": 0,
#      "size": 10,
#     # "sort": [ ],
#     # "aggs": { }
#
#     })
