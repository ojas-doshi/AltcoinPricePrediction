from datetime import datetime
from timeit import default_timer as timer

from numpy import genfromtxt

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, InputLayer
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.callbacks import  EarlyStopping, ReduceLROnPlateau

from tensorflow import lite

import matplotlib.pyplot as plt

date = str(datetime.now()).replace(':', '_')


class KerasModel:

	CRYPTO_SYMBOL = ['ETH','EOS','XRP','BCH','LTC','TRX','ETC','BNB','OKB']

	def __init__(self):
		self._model = None

	@property
	def model(self):
		'''
		this will return created model
		'''
		if self._model is None:
			self.get_model()
		return self._model

	@property
	def symbol_list(self):
		'''
		this will return symbol list
		'''
		return self.CRYPTO_SYMBOL

	def get_model(self):

		model = Sequential()
		model.add(InputLayer(input_shape=(30,)))

		model.add(Dense(70, activation='relu'))
		model.add(Dense(40, activation='relu'))
		model.add(Dense(25, activation='sigmoid'))

		model.add(Dense(1, activation='linear'))

		optimizer1 = Adam(lr=0.001)
		# optimizer1 = RMSprop(lr=.0001)
		model.compile(loss='mae', optimizer=optimizer1,metrics=[])
		return model

	# def plot_graph(self):
	# 	Y.shape
	# 	predt.shape
	# 	x = X[:, :1]
	# 	plt.style.use()
	# 	fig, ax = plt.subplots(nrows=2, ncols=2)
	# 	print(ax)
	# 	ax.plot(x, Y, 'k--')
	# 	ax.plot(x,predt)
	# 	ax.set_xlabel('Original')
	# 	ax.set_ylabel('Predicted')
	# 	plt.savefig(''+date+'/plot'+date+'.png')
	# 	plt.show()
	# 	plt.legend()

	# def predictions(self):

	# 	predictions = self.model.predict(X)

	# 	print(predictions[0][0]*(maxval-minval)+minval)
	# 	print(predictions[1][0]*(maxval-minval)+minval)
	# 	print(predictions[2][0]*(maxval-minval)+minval)
	# 	print(predictions[3][0] * (maxval - minval) + minval)

	# 	x = []
	# 	y = []
	# 	for i in range(len(X)):
	# 		x.append(X[i][-1])
	# 		y.append(predictions[i][0])

	# 	print(x,y)

	# 	p1 = plt.plot(range(len(X)),x)
	# 	p2 = plt.plot(range(len(X)),y)
	# 	plt.ylabel(symbol_list[cryptoname])
	# 	plt.xlabel("time(hours)")
	# 	plt.savefig('plot_'+symbol_list_1[cryptoname]+' ')
	# 	plt.clf()

	def convert_model_to_lite(self):
		# os.mkdir(date)
		#save_model(model, 'model1.h5')

		# conv = lite.TFLiteConverter.from_saved_model('savedmodel')
		# conv = lite.TFLiteConverter.from_keras_model_file('model1.h5')
		conv = lite.TFLiteConverter.from_keras_model(self.model)
		tfmodel = conv.convert()
		with open(f"models\model_{self.symbol}.tflite", "wb") as f:
			f.write(tfmodel)

		# conv1 = lite.TFLiteConverter.from_keras_model_file('model.h5')
		# tfmodel1 = conv1.convert()
		# open("model1.tflite","wb").write(tfmodel1)

	def get_dataset_original(self):
		return genfromtxt(f'tensorflow_lite_models/training_data_{self.symbol}.csv', delimiter=',')

	def get_min_max_val(self):
		minval = self.dataset_original.min()
		maxval = self.dataset_original.max()
		
		return minval,maxval

	def get_dataset(self):
		self.dataset_original = self.get_dataset_original()
		
		minval,maxval = self.get_min_max_val()
		dataset = (self.dataset_original-minval)/(maxval-minval)

		return dataset

	def get_training_data(self):

		dataset = self.get_dataset()

		x = dataset[:, 0:30]
		y = dataset[:, 30:]

		print(f'Training Data x{x.shape}')
		print(f'Training Data y{y.shape}')
		
		return x,y

	def print_summary(self):
		'''
		This will print summary of model
		'''
		self.model.summary()

	def model_fit(self):
		'''
		Here model will be fitted
		'''
		x,y = self.get_training_data()
		self.model.fit(x, y, epochs=10, shuffle=False, batch_size=30, validation_split=0.05,
			callbacks=[
			EarlyStopping(monitor='val_loss',
			restore_best_weights=True, patience=20, verbose=True),
			ReduceLROnPlateau(monitor='val_loss', patience=4, verbose=True)
			#             TensorBoard(batch_size=100)
			]
			)
	
	def save_model(self):
		'''
		Here model is saved
		'''
		self.model.save(f"tensorflow_models/model_{self.symbol}.h5", include_optimizer=True)
		self.convert_model_to_lite()

	def train_models(self):
		'''
		Models will be trained here
		'''
		for symbol in self.symbol_list:
			self.symbol = symbol
			start = timer()
			self.model_fit()
			end = timer()
			print("without GPU:", end-start)
			self.print_summary()
			self.save_model()
			self.convert_model_to_lite()

kl = KerasModel()
kl.train_models()
# symbol_list_1 = ['eth','eos','xrp','bch','ltc','trx','etc','bnb','okb']
# symbol_list = ['ETH','EOS','XRP','BCH','LTC','TRX','ETC','BNB','OKB']
# for symbol in range(0,len(symbol_list)):
# 	dataset_original = genfromtxt('training_data\training_data_'+symbol_list[symbol]+'.csv', delimiter=',')

# 	dataset_original = dataset_original[:]

# 	minval = dataset_original.min()
# 	maxval = dataset_original.max()

# 	dataset = (dataset_original-minval)/(maxval-minval)

# 	model = kl.get_model()
# 	print(X.shape)
# 	print(Y.shape)


# 	model.fit(X, Y, epochs=10, shuffle=False, batch_size=30, validation_split=0.05,
# 	callbacks=[
# 	EarlyStopping(monitor='val_loss',
# 	restore_best_weights=True, patience=20, verbose=True),
# 	ReduceLROnPlateau(monitor='val_loss', patience=4, verbose=True)
# 	#             TensorBoard(batch_size=100)
# 	]
# 	)
# 	model.summary()
# 	kl.predictions(symbol)
# 	model.save("model.h5", include_optimizer=True)  # model,'savedmodel')
# 	kl.save__model(symbol)