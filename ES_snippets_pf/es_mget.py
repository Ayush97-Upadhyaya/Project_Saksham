from elasticSearch import ElasticSearch as esearch
from Threading import BoundedSemaphore, Thread
from ssl import create_default_context
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


Get_Batch_Data = BoundedSemaphore(1)
Data_feed_for_RNN = [][]


#Declare RNN
#Download and initialise weight matrix from ES
	

#Get Data thread (test on dataset thread.sleep required or not)
#####-------------------------------########
end_index_res = es.get(index = 'my_index', doc_type ='my_type', 'id' = end_index_id , realtime = True)

end_index = end_index_res['result']
list_of_ids = list(range(start_index,end_index))
start_index = end_index+1

batch_results = es.mget(index = 'my_index', doc_type ='my_type', 'id' = list_of_ids, realtime = True)

Get_Batch_Data.acquire()
total_results = batch_results['hits']['total']
Data_feed_for_RNN = batch_results
Get_Batch_Data.release()

#####-------------------------------########

#Rnn Algo Thread
#####-------------------------------########
Get_Batch_Data.acquire()
#Run Algo
Get_Batch_Data.release()
