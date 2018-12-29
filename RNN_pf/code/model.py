from keras.preprocessing.sequence import TimeseriesGenerator
import preprocess

df=preprocess.one_hot_data()
#look_back=

train_data_gen = TimeseriesGenerator(train, train,
	length=look_back, sampling_rate=1,stride=1,
    batch_size=10)
test_data_gen = TimeseriesGenerator(test, test,
	length=look_back, sampling_rate=1,stride=1,
	batch_size=3)


model = Sequential()
model.add(LSTM(4, input_shape=(look_back, 1)))
model.add(Dense(1))
model.compile(loss='mean_squared_error', optimizer='adam')
history = model.fit_generator(train_data_gen, epochs=50).history
