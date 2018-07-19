from Data_process import Data_process
from rnn import model_keras
import os
import pickle
import numpy as np

DIR = os.path.dirname(os.path.abspath(__file__))


def train(maxlen=40,
          batchsize=64,
          num_words=3000,
          num_units=128,
          epochs=1,
          mode='length',
          one_hot=False):
    data_process = Data_process()
    x, y, word_index = data_process.data_transform(num_words=num_words,
                                                   mode=mode,
                                                   len_min=5,
                                                   len_max=100,
                                                   maxlen=maxlen,
                                                   one_hot=one_hot)
    with open(DIR + '/model/word_index.pkl', mode='wb') as f:
        pickle.dump(word_index, f)
    model = model_keras(num_words=data_process.num_words, num_units=num_units)
    for epoch in range(epochs):
        if one_hot:
            model.fit(x=x, y=y, epochs=epochs, batch_size=batchsize, verbose=1)
        else:
            for batch in range(10):
                index_all = np.arange(len(x))
                index_batch = np.random.choice(index_all, batchsize)
                x_batch = x[index_batch]
                y_batch = y[index_batch]
                y_batch = np.array([data_process.creat_one_hot(y_1, data_process.num_words) for y_1 in y_batch])
                print('batch:', batch + 1)
                model.fit(x=x_batch, y=y_batch, epochs=1, batch_size=batchsize, verbose=1)
        model.save(DIR + '/model/model_keras_%d.h5' % (epoch))


if __name__ == '__main__':
    train(maxlen=100, batchsize=64, num_words=3000,
          num_units=128, epochs=1,
          mode='length', one_hot=False)
