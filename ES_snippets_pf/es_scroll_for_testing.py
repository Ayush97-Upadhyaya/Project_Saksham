from elasticSearch import ElasticSearch as esearch
from Threading import BoundedSemaphore, Thread
from ssl import create_default_context
import time
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

#file read write Semaphore
file_wr_semaphore = BoundedSemaphore(1)

#open file for append + read
file_data = open("file_data.txt", "a+")


#Data Downloaded
data_download = 0
#####-------------------------------########
doc = {
        'size' : 10000,
        'query': {
            'match_all' : {}
       }
   }

big_batch_results = es.search(index='indexname', doc_type='typename', body=doc,scroll='1m')
size_batch = big_batch_results['hits']['total']
scrollId = big_batch_results['_scroll_id']

#Get Data Thread
#######################################
def get_data():
	print "Get Data Started"
	for hit in big_batch_results['hits']['hits']:
		file_wr_semaphore.acquire()
		file_data.write(hit)
		file_wr_semaphore.release()

	while(size_batch>0):
		big_batch_results = es.scroll(scroll_id = scrollId, scroll = '2m')
		size_batch = big_batch_results['hits']['total']
		scrollId = big_batch_results['_scroll_id']

		for hit in big_batch_results['hits']['hits']:
			file_wr_semaphore.acquire()
			file_data.write(hit)
			file_wr_semaphore.release()
#######################################

data_download = 1

#####-------------------------------########


last_read_char_pos = 0 #unlimited long if python 3.x otherwise max limit	
data_reading = 1
data_read_once_after_download = 0

##RNN thread
#####-------------------------------########
def train_rnn():
	print "train_rnn Started"
	while(data_reading):

		if(not data_download):
			file_wr_semaphore.acquire()
			file_data.seek(last_read_char_pos,0)
			data_line_for_training = file_data.readline()
			if not data_line_for_training:
				data_reading = 0
				break
			last_read_char_pos = file_data.tell()
			file_wr_semaphore.release()	

		elif data_download and not data_read_once_after_download :
			file_data.seek(last_read_char_pos,0)
			data_line_for_training = file_data.readline()
			if not data_line_for_training:
				data_reading = 0
				break
			last_read_char_pos = file_data.tell()
			data_read_once_after_download = 1
		
		else :
			data_line_for_training = file_data.readline()
			if not data_line_for_training:
				data_reading = 0
				break

		# Rnn algo with data_line_for_training
		# Anomaly
		# 	no 	=> continue
		# 	yes => add in faulty db 
					#spark
					# =>val df = Seq(String).toDF().coalesce(1)
					# // ======= Writing files
					# // Writing Dataframe as parquet file
					# df.write.mode(SaveMode.Overwrite).parquet(hdfs_master + "user/hdfs/wiki/testwiki")
					# // Writing Dataframe as csv file
					# df.write.mode(SaveMode.Overwrite).csv(hdfs_master + "user/hdfs/wiki/testwiki.csv")
		# 		=> remove from normal data
		# 		=> get user details
		# 		=> generate alert
#####-------------------------------########

get_data_thread = Threading.Thread(target = get_data)
train_rnn_thread = Threading.Thread(target = train_rnn)

get_data.start()		#start Get data thread
time.sleep(5)			#setup delay
train_rnn.start()		#start RNN thread


# upload on hadoop https://datascience.stackexchange.com/questions/13123/import-csv-file-contents-into-pyspark-dataframes