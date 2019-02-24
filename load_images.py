#Sys
import os
import numpy as np
from PIL import Image
import keras as k
from matplotlib import pyplot as p
from keras.models import Sequential
from keras import optimizers
from keras.layers import Dense, Dropout, Activation,Flatten,BatchNormalization
#from keras_sequential_ascii import sequential_model_to_ascii_printout
#from sklearn.metrics import classification_report, confusion_matrix
from keras.layers import Conv2D,ZeroPadding2D, MaxPooling2D

#Custom
from val_load import get_annotations_map

def load_images(path,num_classes):
    #Load images
    
    print('Loading ' + str(num_classes) + ' classes')

    X_train=np.zeros([num_classes*500,32,32,3],dtype='uint8')
    y_train=np.zeros([num_classes*500], dtype='uint8')

    trainPath=path+'/train/bilinear'

    print('loading training images...');

    i=0
    j=0
    annotations={}
    for sChild in os.listdir(trainPath):
        sChildPath = os.path.join(os.path.join(trainPath,sChild),'images')
        annotations[sChild]=j
        for c in os.listdir(sChildPath):
            X=np.array(Image.open(os.path.join(sChildPath,c)))
            if len(np.shape(X))==2:
                X_train[i]=np.array([X,X,X])
            else:
                X_train[i]=X
            y_train[i]=j
            i+=1
        j+=1
        if (j >= num_classes):
            break

    print('finished loading training images')

    val_annotations_map = get_annotations_map()

    X_test = np.zeros([num_classes*50,32,32,3],dtype='uint8')
    y_test = np.zeros([num_classes*50], dtype='uint8')


    print('loading test images...')

    i = 0
    testPath=path+'/val/bilinear/images'
    for sChild in os.listdir(testPath):
        if val_annotations_map[sChild] in annotations.keys():
            sChildPath = os.path.join(testPath, sChild)
            X=np.array(Image.open(sChildPath))
            if len(np.shape(X))==2:
                X_test[i]=np.array([X,X,X])
            else:
                X_test[i]=X
            y_test[i]=annotations[val_annotations_map[sChild]]
            i+=1
        else:
            pass


    print('finished loading test images')+str(i)

    return X_train,y_train,X_test,y_test

def model_creation():
	model = Sequential()
        model.add(Conv2D(32, (3, 3), padding='same', input_shape= (32,32, 3)))
	model.add(Activation('relu'))
	model.add(MaxPooling2D(pool_size=(2, 2)))
	
	
# conv2
	model.add(Conv2D(32,(3, 3), padding='same'))
	model.add(Activation('relu'))
	model.add(MaxPooling2D(pool_size=(2, 2)))
	
	#model.add(Conv2D(32,(3,3),padding='same'))
	#model.add(Activation('relu'))
	#model.add(MaxPooling2D(pool_size=(2,2)))
# conv3
	model.add(Conv2D(64, (3, 3), padding='same'))
	model.add(Activation('relu'))
	model.add(MaxPooling2D(pool_size=(2, 2)))
	model.add(BatchNormalization())
	model.add(Activation('relu'))
# conv4
	model.add(Conv2D(64, (3, 3), padding='same'))
	model.add(Activation('relu'))
	model.add(MaxPooling2D(pool_size=(2, 2)))

# conv5
	model.add(Conv2D(64, (3, 3), padding='same'))
	model.add(Activation('relu'))
	model.add(MaxPooling2D(pool_size=(2, 2)))
	model.add(Dropout(0.2))

	model.add(Flatten())

# fc1
	model.add(Dense(2048))
	model.add(Activation('relu'))
	
	model.add(Dense(1024))
	model.add(Activation('relu'))
        
	model.add(Dense(1024))
	model.add(Activation('relu'))

	model.add(Dense(512))
	model.add(Activation('relu'))
	
	model.add(Dense(512))
	model.add(Activation('relu'))
# fc2
	model.add(Dense(no_class))
  	model.add(Activation('softmax'))
  	opt = optimizers.Adam(beta_1=.9,beta_2=.999,lr = learning_rate)
  	model.compile(loss='categorical_crossentropy', optimizer=opt,metrics=['accuracy'])
  	return model



def model_creation1():
  model = Sequential()
  print('Input shape',X_train.shape[1:])
  model.add(Conv2D(64,(3,3),input_shape=(X_train.shape[1:])))
  model.add(Activation('relu'))
  model.add(Conv2D(64,(3,3),padding="same"))
  model.add(Activation('relu'))
  model.add(MaxPooling2D(pool_size=(2,2),padding="same"))
  model.add(BatchNormalization())
  model.add(Activation('relu'))
  

  model.add(Conv2D(128,(3,3),activation='relu',padding="same"))
  model.add(Conv2D(128,(3,3),padding="same"))
  model.add(Activation('relu'))
  model.add(MaxPooling2D(pool_size=(2,2),padding="same"))
  model.add(BatchNormalization())
  model.add(Activation('relu'))
  

  model.add(Conv2D(256,(3,3),padding="same",activation='relu'))
  model.add(Conv2D(256,(3,3),padding="same",activation='relu'))
  model.add(MaxPooling2D(pool_size=(2,2),padding="same"))
  model.add(BatchNormalization())
  model.add(Activation('relu'))
  #model.add(Dropout(0.25))
  
  
  model.add(Conv2D(512,(3,3),padding="same"))
  model.add(Activation('relu'))
  model.add(Conv2D(512,(3,3),padding="same"))
  model.add(Activation('relu'))
  model.add(MaxPooling2D(pool_size=(2,2),padding="same"))
  model.add(BatchNormalization())
  model.add(Activation('relu'))
  model.add(Dropout(0.25))

  model.add(Flatten())
  model.add(Dense(512))
  model.add(Activation('relu'))
  model.add(Dense(512))
  model.add(Activation('relu'))
  model.add(Dense(512))
  model.add(Activation('relu'))
  model.add(Dense(no_class))
  model.add(Activation('softmax'))
  opt = optimizers.Adam(beta_1=.9,beta_2=.999,lr = learning_rate)
  model.compile(loss='categorical_crossentropy', optimizer=opt,metrics=['accuracy'])
  return model


def plot_modelacc(fit_model):
    with p.style.context('ggplot'):
            p.plot(fit_model.history['acc'])
            p.plot(fit_model.history['val_acc'])
            p.title("MODEL ACCURACY")
            p.xlabel("# of EPOCHS")
            p.ylabel("ACCURACY")
            p.legend(['train', 'test'], loc='upper left')
    return p.show()

def plot_model_loss(fit_model):
    with p.style.context('ggplot'):
            p.plot(fit_model.history['loss'])
            p.plot(fit_model.history['val_loss'])
            p.title("MODEL LOSS")
            p.xlabel("# of EPOCHS")
            p.ylabel("LOSS")
            p.legend(['train', 'test'], loc='upper left')
    return p.show()


if __name__ == "__main__":
    import matplotlib.pyplot as plt
    print("In main file")	
    path='../../'
    X_train,y_train,X_test,y_test=load_images(path,200)
    no_class = 200 
    batch_size = 64
    epoch = 200
    learning_rate = 0.00001
    y_train = k.utils.to_categorical(y_train, no_class)
    y_test = k.utils.to_categorical(y_test, no_class)
    # pixel values range from 0 to 255 - normalize 
    X_train = X_train.astype('float32')
    X_test = X_test.astype('float32')
    X_train  /= 255
    X_test /= 255
    cnn_basemodel = model_creation()
    cnn_1 = cnn_basemodel.fit(X_train, y_train, batch_size=batch_size, epochs=epoch,validation_data=(X_test,y_test),shuffle=True)
    acc = cnn_basemodel.evaluate(X_test, y_test, verbose=1)
    print('Test data loss:', acc[0] )
    print('Test data accuracy:', acc[1] * 100)
    plot_modelacc(cnn_1)
    plot_model_loss(cnn_1)
 

#    fig1 = plt.figure()
#    fig1.suptitle('Train data')
#    ax1 = fig1.add_subplot(221)
#    ax1.axis("off")
#    ax1.imshow(np.transpose(X_train[0],(1,2,0)))
#    print(y_train[0])
#    ax2 = fig1.add_subplot(222)
#    ax2.axis("off")
#    ax2.imshow(np.transpose(X_train[499],(1,2,0)))
#    print(y_train[499])
#    ax3 = fig1.add_subplot(223)
#    ax3.axis("off")
#    ax3.imshow(np.transpose(X_train[500],(1,2,0)))
#    print(y_train[500])
#    ax4 = fig1.add_subplot(224)
#    ax4.axis("off")
#    ax4.imshow(np.transpose(X_train[999],(1,2,0)))
#    print(y_train[999])

#    plt.show()

#    fig2 = plt.figure()
#    fig2.suptitle('Test data')
#    ax1 = fig2.add_subplot(221)
#    ax1.axis("off")
#    ax1.imshow(np.transpose(X_test[0],(1,2,0)))
#    print(y_test[0])
#    ax2 = fig2.add_subplot(222)
#    ax2.axis("off")
#    ax2.imshow(np.transpose(X_test[49],(1,2,0)))
#    print(y_test[49])
#    ax3 = fig2.add_subplot(223)
#    ax3.axis("off")
#    ax3.imshow(np.transpose(X_test[50],(1,2,0)))
#    print(y_test[50])
#    ax4 = fig2.add_subplot(224)
#    ax4.axis("off")
#    ax4.imshow(np.transpose(X_test[99],(1,2,0)))
#    print(y_test[99])
    
#    plt.show()
