6
7
8
9
10
11
12
13
14
15
16
17
18
19
20
21
22
23
24
25

# univariate one step problem with lstm
from numpy import array
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM
from keras.preprocessing.sequence import TimeseriesGenerator
# define dataset
series = array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
# reshape to [10, 1]
n_features = 1
series = series.reshape((len(series), n_features))
# define generator
n_input = 3
generator = TimeseriesGenerator(series, series, length=n_input, batch_size=1)
# define modelH
model = Sequential()
model.add(LSTM(100, activation='relu', input_shape=(n_input, n_features)))
model.add(Dense(1))
model.compile(optimizer='adam', loss='mse')
# fit model
history = model.fit_generator(generator, epochs=100).history

model.evaluate_generator(generator)

# make a one step prediction out of sample
x_input = array([5,6,7]).reshape((1, n_input, n_features))
yhat = model.predict(x_input, verbose=0)
print(yhat)
