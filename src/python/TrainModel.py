from tensorflow.keras.models import Sequential, save_model, load_model
from tensorflow.keras.layers import LSTM, Dense, Reshape, InputLayer, GRU
from tensorflow.keras.optimizers import RMSprop, Adam
from tensorflow.keras.callbacks import TensorBoard, EarlyStopping, ReduceLROnPlateau
from numpy import genfromtxt
from datetime import datetime
from timeit import default_timer as timer
import os
import io
from tensorflow import lite
import matplotlib.pyplot as plt

date = str(datetime.now()).replace(':', '_')


# model.save(''+date+'/model'+date+'.h5')

# predt = predictions*(maxval-minval)+minval
# print(Y[0][0]*(maxval-minval)+minval,predt[0][0])
# ax.scatter(X,Y, predt)
# model2=load_model(''+date+'/model'+date+'.h5')
# model2=super1.get_model()
# model2.load_weights(''+date+'/model'+date+'.h5')
# model2.summary()


class KerasModel():
	model = None

	def get_model(self):
		if self.model:
			return self.model

		model = Sequential()
		model.add(InputLayer(input_shape=(30,)))
		# model.add(Reshape((1, 30)))

		# model.add(LSTM(50, return_sequences=True))
		# model.add(LSTM(50, return_sequences=False))

		# model.add(GRU(25))

		model.add(Dense(70, activation='relu'))
		model.add(Dense(40, activation='relu'))
		model.add(Dense(25, activation='sigmoid'))

		model.add(Dense(1, activation='linear'))

		optimizer1 = Adam(lr=0.001)
		# optimizer1 = RMSprop(lr=.0001)
		model.compile(loss='mae', optimizer=optimizer1,
		metrics=[])
		self.model = model
		return model

	def plot_graph(self):
		#Y.shape
		# predt.shape
		#x = X[:, :1]
		# plt.style.use()
		#fig, ax = plt.subplots(nrows=2, ncols=2)
		print(ax)
		#ax.plot(x, Y, 'k--')
		# ax.plot(x,predt)
		#ax.set_xlabel('Original')
		#ax.set_ylabel('Predicted')
		#plt.savefig(''+date+'/plot'+date+'.png')
		# plt.show()
		# plt.legend()

	def predictions(self,cryptoname):

		predictions = model.predict(X)

		print(predictions[0][0]*(maxval-minval)+minval)
		print(predictions[1][0]*(maxval-minval)+minval)
		print(predictions[2][0]*(maxval-minval)+minval)
		print(predictions[3][0] * (maxval - minval) + minval)

		x = []
		y = []
		for i in range(len(X)):
			x.append(X[i][-1])
			y.append(predictions[i][0])

		print(x,y)

		p1 = plt.plot(range(len(X)),x)
		p2 = plt.plot(range(len(X)),y)
		plt.ylabel(symbol_list[cryptoname]")
		plt.xlabel("time(hours)")
		plt.savefig('plot_'+symbol_list_1[cryptoname]+' ')
		plt.clf()

	def save__model(self,cryptoname):
		# os.mkdir(date)
		#save_model(model, 'model1.h5')

		# conv = lite.TFLiteConverter.from_saved_model('savedmodel')
		# conv = lite.TFLiteConverter.from_keras_model_file('model1.h5')
		conv = lite.TFLiteConverter.from_keras_model(model)
		tfmodel = conv.convert()
		with open("model_"+symbol_list_1[cryptoname]+".tflite", "wb") as f:
			f.write(tfmodel)

		# conv1 = lite.TFLiteConverter.from_keras_model_file('model.h5')
		# tfmodel1 = conv1.convert()
		# open("model1.tflite","wb").write(tfmodel1)

kl = KerasModel()
symbol_list_1 = ['eth','eos','xrp','bch','ltc','trx','etc','bnb','okb']
symbol_list = ['ETH','EOS','XRP','BCH','LTC','TRX','ETC','BNB','OKB']
for symbol in range(0,len(symbol_list)):
	dataset_original = genfromtxt('training_data_'+symbol_list[symbol]+'.csv', delimiter=',')

	dataset_original = dataset_original[:]

	minval = dataset_original.min()
	maxval = dataset_original.max()

	dataset = (dataset_original-minval)/(maxval-minval)

	X = dataset[:, 0:30]
	Y = dataset[:, 30:]

	print("X", X.shape)
	print("Y", Y.shape)

	start = timer()

	model = kl.get_model()
	print(X.shape)
	print(Y.shape)


	model.fit(X, Y, epochs=10, shuffle=False, batch_size=30, validation_split=0.05,
	callbacks=[
	EarlyStopping(monitor='val_loss',
	restore_best_weights=True, patience=20, verbose=True),
	ReduceLROnPlateau(monitor='val_loss', patience=4, verbose=True)
	#             TensorBoard(batch_size=100)
	]
	)
	model.summary()
	end = timer()
	print("without GPU:", end-start)
	kl.predictions(symbol)
	model.save("model.h5", include_optimizer=True)  # model,'savedmodel')
	kl.save__model(symbol)