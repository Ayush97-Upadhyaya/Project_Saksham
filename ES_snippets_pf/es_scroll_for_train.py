from elasticSearch import ElasticSearch as esearch
from Threading import BoundedSemaphore, Thread
from ssl import create_default_context
import time
#import pandas as pd
import os
#import RNN file 

# # SSL certification + Connection
# context = create_default_context(cafile="path/to/cert.pem") 
# es = Elasticsearch(
#     ['localhost', 'otherhost'],
#     http_auth=('user', 'secret'),
#     scheme="https",
#     port=443,
#     ssl_context=context,
# )
#
#Same as above inline
es = Elasticsearch(
    [
        'http://user:secret@localhost:9200/',
        'https://user:secret@other_host:443/production'
    ],
    verify_certs=True
)

#get data
doc = {
        'size' : 10000,
        'query': {
            'match_all' : {}
       }
   }

big_batch_results = es.search(index='indexname', doc_type='typename', body=doc,scroll='1m')
size_batch = big_batch_results['hits']['total']
scrollId = big_batch_results['_scroll_id']

#pandas_df = pd.DataFrame(columns = []) #columns of file 

batch_list = []

for hit in big_batch_results['hits']['hits']:
	#pandas_df.append(hit, ignore_index = True)
	batch_list.append(hit)

#keras.train_batch
#model.save_weights('weights.h5')
#pandas_df.drop

while(size_batch>0):

		big_batch_results = es.scroll(scroll_id = scrollId, scroll = '2m')
		size_batch = big_batch_results['hits']['total']
		scrollId = big_batch_results['_scroll_id']
		del batch_list
		batch_list = []
		for hit in big_batch_results['hits']['hits']:
			#pandas_df = pd.DataFrame(hit, ignore_index = True, columns = [])
			batch_list.append(big_batch_results)
		#keras.train_batch with batch_list
		#model.save_weights('weights.h5')

 # st = “{0}_{1}_{2}_{3}”.format(a,b,c,d)   # Better for memory. Does not create temp strs 
 # st2 = a + ‘_’ + b + ‘_’ + c + ‘_’ + d # Creates temp strs at each concatenation, which are then interned
 ##__slots__ = (‘val1’, ‘val2’, ‘val3’, ‘val4’, ‘val5’, ‘val6’)