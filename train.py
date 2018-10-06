from keras.models import Sequential
from keras.layers import *
from keras.optimizers import *
from qlearning4k import Agent

#------------------------------------
from server import Game
#------------------------------------

from keras import backend as K
K.set_image_dim_ordering('th')

grid_size = 21
nb_frames = 1
nb_actions = 5

model = Sequential()
model.add(Conv2D(16, (3, 3), activation='relu', input_shape=(nb_frames, grid_size, grid_size, 3)))
model.add(Conv2D(32, (4, 4), activation='relu'))
model.add(Flatten())
model.add(Dense(256, activation='relu'))
model.add(Dense(nb_actions))
model.compile(RMSprop(), 'MSE')

#------------------------------------
game = Game()
#------------------------------------

agent = Agent(model=model, memory_size=-1, nb_frames=nb_frames)
agent.train(game, batch_size=1, nb_epoch=10000, gamma=0.8)
agent.play(game)