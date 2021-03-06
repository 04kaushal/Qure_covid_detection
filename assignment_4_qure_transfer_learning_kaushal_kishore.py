# -*- coding: utf-8 -*-
"""Assignment_4_Qure_Transfer_learning_Kaushal_kishore.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1pspUu-G058qAiqIxVRkAc_hIOam_YtXb

# **(Machine) Learning to make decisions better '21-22**

# **Assignment - 4|| Qure case Study || Kaushal Kishore || P2021PTLP0020**

## Downloading the data & extracting images
"""

!wget https://www.dropbox.com/s/1ewy9gw42sty8pt/cxr_plaksha_assignment_qure.zip?dl=0

!unzip cxr_plaksha_assignment_qure.zip?dl=0

!ls

"""## Importing all required libraries"""

import os
from tensorflow.keras.preprocessing import image
image_names = os.listdir('/content/cxr_plaksha_assignment_qure')

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import keras
from keras.layers import *
from keras.models import *
from keras.preprocessing import image

# import the libraries as shown below

from tensorflow.keras.layers import Input, Lambda, Dense, Flatten
from tensorflow.keras.models import Model
from tensorflow.keras.applications.resnet50 import ResNet50
#from keras.applications.vgg16 import VGG16
from tensorflow.keras.applications.resnet50 import preprocess_input
from tensorflow.keras.preprocessing import image
from tensorflow.keras.preprocessing.image import ImageDataGenerator,load_img
from tensorflow.keras.models import Sequential
import numpy as np
from glob import glob
import matplotlib.pyplot as plt
import torch
import torch.utils.data as data
from torch.utils.data import Dataset
from torchvision.transforms import ToTensor
import pandas as pd
import os
import cv2
import matplotlib.pyplot as plt
import torch
import torch.utils.data as data
from torch.utils.data import Dataset
from torchvision.transforms import ToTensor
import torchvision.transforms as transforms

"""## Preparing Train & Validation Data"""

df= pd.read_csv("/content/drive/MyDrive/Assignments/Machine_application/Qure/consolidation_train_gt.csv",dtype=str)
df.head(2)

df_new=df.drop(["consolidation-left","consolidation-right"],axis=1)
def append_ext(fn):
    return fn+".png"

df_new["filename"]=df_new["filename"].apply(append_ext)
df_new.head(2)

import os
import shutil

original = '/content/cxr_plaksha_assignment_qure'
new_path = '/content/new_data'


files_list = sorted(os.listdir(original))
file_names= df_new['filename']

for curr_file in file_names:
    shutil.copyfile(os.path.join(original, curr_file),
                    os.path.join(new_path, curr_file))

df_new['consolidation'].value_counts()

all_images = pd.DataFrame(files_list)
all_images.columns =['Name']
all_images.head()

files_list_train = sorted(os.listdir(new_path))
train_images = pd.DataFrame(files_list_train)
train_images.columns =['Name']
train_images.head()

"""### Preparing Test Data For prediction"""

test_images = all_images[~all_images.Name.isin(train_images.Name)]
test_images.head()

test_images.shape

# copying the images with names in the csv to another folder 
import os
import shutil

Actual = '/content/cxr_plaksha_assignment_qure'
test_images_path = '/content/test'

file_names= test_images['Name']

for curr_file in file_names:
  shutil.copyfile(os.path.join(Actual, curr_file),
                  os.path.join(test_images_path, curr_file))

from keras.models import Sequential 
from tensorflow.keras.layers import Conv2D
from keras.applications.mobilenet import MobileNet
from keras.layers import GlobalAveragePooling2D, Dense, Dropout, Flatten
from keras.models import Sequential
from keras.layers import Activation, Dense
from tensorflow.keras.layers import Conv2D, MaxPooling2D
from keras.optimizers import rmsprop_v2

"""## Model building"""

model = Sequential()
model.add(Conv2D(32, kernel_size=(3,3), activation = 'relu', input_shape =(224,224,3)))
model.add(Conv2D(64,(3,3),activation = 'relu'))
model.add(MaxPooling2D(pool_size= (2,2)))
model.add(Dropout(0.25))

model.add(Conv2D(64,(3,3), activation = 'relu'))
model.add(MaxPooling2D(pool_size= (2,2)))
model.add(Dropout(0.25))

model.add(Conv2D(64,(3,3), activation = 'relu'))
model.add(MaxPooling2D(pool_size= (2,2)))
model.add(Dropout(0.25))

model.add(Flatten())
model.add(Dense(64, activation = 'relu'))
model.add(Dropout(0.50))
model.add(Dense(2, activation = 'softmax')) # final layer we are perform binary classification so kept layer 1 & sigmoid
model.compile(loss = keras.losses.categorical_crossentropy, optimizer = 'adam', metrics = [
        'accuracy',
        tf.keras.metrics.Precision(name='precision'),
        tf.keras.metrics.Recall(name='recall')
    ])
model.summary()

# Use the Image Data Generator to import the images from the dataset
from tensorflow.keras.preprocessing.image import ImageDataGenerator

train_datagen = ImageDataGenerator(rescale = 1./255,
                                   validation_split=0.25,
                                   shear_range = 0.2,
                                   zoom_range = 0.2,
                                   )

# Make sure you provide the same target size as initialied for the image size
training_set = train_datagen.flow_from_dataframe(directory='/content/new_data',
                                                 dataframe = df_new,
                                                 x_col="filename",
                                                 y_col="consolidation",
                                                 subset="training",
                                                 target_size = (224,224),
                                                 batch_size = 32,
                                                 shuffle=True,
                                                 class_mode = 'categorical')

train_datagen

df_new

# Make sure you provide the same target size as initialied for the image size
validation_set = train_datagen.flow_from_dataframe(directory='/content/new_data',
                                                 dataframe = df_new,
                                                 x_col="filename",
                                                 y_col="consolidation",
                                                 subset="validation",
                                                 target_size = (224,224),
                                                 batch_size = 32,
                                                 shuffle=True,
                                                 seed=15,
                                                 class_mode = 'categorical')

df_new.shape

"""## Model Performance Evaluation"""

# fitting the model 
STEP_SIZE_TRAIN=training_set.n//training_set.batch_size
STEP_SIZE_VALID=validation_set.n//validation_set.batch_size

history = model.fit_generator(generator=training_set,
                    steps_per_epoch=STEP_SIZE_TRAIN,
                    validation_data=validation_set,
                    validation_steps=STEP_SIZE_VALID,
                    epochs=6)

epochs = [i for i in range(6)]
fig , ax = plt.subplots(1,2)
train_acc = history.history['accuracy']
train_loss = history.history['loss']
val_acc = history.history['val_accuracy']
val_loss = history.history['val_loss']
fig.set_size_inches(20,10)

ax[0].plot(epochs , train_acc , 'go-' , label = 'Training Accuracy')
ax[0].plot(epochs , val_acc , 'ro-' , label = 'Validation Accuracy')
ax[0].set_title('Training & Validation Accuracy')
ax[0].legend()
ax[0].set_xlabel("Epochs")
ax[0].set_ylabel("Accuracy")

ax[1].plot(epochs , train_loss , 'g-o' , label = 'Training Loss')
ax[1].plot(epochs , val_loss , 'r-o' , label = 'Validation Loss')
ax[1].set_title('Testing Accuracy & Loss')
ax[1].legend()
ax[1].set_xlabel("Epochs")
ax[1].set_ylabel("Training & Validation Loss")
plt.show()

training_set.class_indices

model.evaluate_generator(training_set)

model.evaluate_generator(validation_set)

#prediction = model.predict_classes('1')
predict_x=model.predict(validation_set) 
classes_x=np.argmax(predict_x)
classes_x

"""## Predicting on remaining 20% Test Data"""

y_tests = []
for i in os.listdir("/content/test/"):
  img = image.load_img("/content/test/"+i, target_size=(224,224))
  img = image.img_to_array(img)
  img = np.expand_dims(img, axis =0)
  predict_x=model.predict(img) 
  classes_x=np.argmax(predict_x)
  y_tests.append(classes_x)

predsss = model.predict(img)
print(predsss.shape)

Target_test = pd.DataFrame(y_tests)
Target_test.columns =['Target']
Target_test.head()

Target_test.value_counts()

test_datagen=ImageDataGenerator(rescale=1./255.)
test_generator=test_datagen.flow_from_dataframe(
dataframe=test_images,
directory="/content/test/",
x_col="Name",
y_col=None,
batch_size=32,
seed=42,
shuffle=False,
class_mode=None,
target_size=(224,224))

STEP_SIZE_TEST=test_generator.n//test_generator.batch_size
test_generator.reset()
pred=model.predict_generator(test_generator,steps=STEP_SIZE_TEST, verbose=1)

pred

temp = pd.DataFrame(pred)
temp

predicted_class_indices=np.argmax(pred,axis=1)

predicted_class_indices

labels = (training_set.class_indices)
labels = dict((v,k) for k,v in labels.items())
predictions = [labels[k] for k in predicted_class_indices]

df_r = pd.DataFrame(predictions)

df_r.columns =['Predictions']

df_r.value_counts()

filenames=test_generator.filenames
results=pd.DataFrame({"Filename":filenames})
results.head()

results['predictions'] = df_r['Predictions']
results.head()

model.save('model_base.h5')

"""# Using Transfer learning - VGG 16 Model"""

from tensorflow.keras.optimizers import Adam
def create_model(input_shape, n_classes, optimizer='rmsprop', fine_tune=0):
    """
    Compiles a model integrated with VGG16 pretrained layers
    
    input_shape: tuple - the shape of input images (width, height, channels)
    n_classes: int - number of classes for the output layer
    optimizer: string - instantiated optimizer to use for training. Defaults to 'RMSProp'
    fine_tune: int - The number of pre-trained layers to unfreeze.
                If set to 0, all pretrained layers will freeze during training
    """
    
    # Pretrained convolutional layers are loaded using the Imagenet weights.
    # Include_top is set to False, in order to exclude the model's fully-connected layers.
    conv_base = VGG16(include_top=False,
                     weights='imagenet', 
                     input_shape=input_shape)
    
    # Defines how many layers to freeze during training.
    # Layers in the convolutional base are switched from trainable to non-trainable
    # depending on the size of the fine-tuning parameter.
    if fine_tune > 0:
        for layer in conv_base.layers[:-fine_tune]:
            layer.trainable = False
    else:
        for layer in conv_base.layers:
            layer.trainable = False

    # Create a new 'top' of the model (i.e. fully-connected layers).
    # This is 'bootstrapping' a new top_model onto the pretrained layers.
    top_model = conv_base.output
    top_model = Flatten(name="flatten")(top_model)
    top_model = Dense(4096, activation='relu')(top_model)
    top_model = Dense(1072, activation='relu')(top_model)
    top_model = Dropout(0.2)(top_model)
    output_layer = Dense(n_classes, activation='softmax')(top_model)
    
    # Group the convolutional base and new fully-connected layers into a Model object.
    model = Model(inputs=conv_base.input, outputs=output_layer)

    # Compiles the model for training.
    model.compile(optimizer=optimizer, 
                  loss='categorical_crossentropy',
                  metrics=['accuracy'])
    
    return model

from keras.applications.vgg16 import VGG16, preprocess_input

BATCH_SIZE = 32
input_shape = (224, 224, 3)
optim_1 = Adam(learning_rate=0.001)
n_classes=2

n_steps = training_set.samples // BATCH_SIZE
n_val_steps = validation_set.samples // BATCH_SIZE
n_epochs = 15

# First we'll train the model without Fine-tuning
vgg_model = create_model(input_shape, n_classes, optim_1, fine_tune=0)

pip install livelossplot

from livelossplot.inputs.keras import PlotLossesCallback
from keras.callbacks import ModelCheckpoint, EarlyStopping
plot_loss_1 = PlotLossesCallback()

# ModelCheckpoint callback - save best weights
tl_checkpoint_1 = ModelCheckpoint(filepath='tl_model_v1.weights.best.hdf5',
                                  save_best_only=True,
                                  verbose=1)

# EarlyStopping
early_stop = EarlyStopping(monitor='val_loss',
                           patience=10,
                           restore_best_weights=True,
                           mode='min')

# Commented out IPython magic to ensure Python compatibility.
# %%time 
# 
# vgg_history = vgg_model.fit(training_set,
#                             batch_size=BATCH_SIZE,
#                             epochs=n_epochs,
#                             validation_data=validation_set,
#                             steps_per_epoch=n_steps,
#                             validation_steps=n_val_steps,
#                             callbacks=[tl_checkpoint_1, early_stop, plot_loss_1],
#                             verbose=1)

"""### Checking performance on Validation data"""

# Generate predictions
vgg_model.load_weights('tl_model_v1.weights.best.hdf5') # initialize the best trained weights
true_classes_val = validation_set.classes
class_indices = training_set.class_indices
class_indices = dict((v,k) for k,v in class_indices.items())
vgg_preds_val = vgg_model.predict(validation_set)
vgg_pred_classes_val = np.argmax(vgg_preds_val, axis=1)

from sklearn.metrics import accuracy_score
vgg_acc_val = accuracy_score(true_classes_val, vgg_pred_classes_val)
print("VGG16 Model Accuracy without Fine-Tuning: {:.2f}%".format(vgg_acc_val * 100))

"""### Predicting class labels for unseen test data i.e. remaining 4000"""

# Loading predictions from last article's model
vgg_preds = vgg_model.predict(test_generator)
vgg_pred_classes = np.argmax(vgg_preds, axis=1)

df_predicted_labels_for_test = pd.DataFrame(vgg_pred_classes)
df_predicted_labels_for_test.head()

df_predicted_labels_for_test.columns =['Predictions']
df_predicted_labels_for_test.value_counts()

"""## Fine Tuning - VGG16"""

# Reset our image data generators
training_set.reset()
validation_set.reset()
test_generator.reset()

# Use a smaller learning rate
optim_2 = Adam(lr=0.0001)

# Re-compile the model, this time leaving the last 2 layers unfrozen for Fine-Tuning
vgg_model_ft = create_model(input_shape, n_classes, optim_2, fine_tune=2)

# Commented out IPython magic to ensure Python compatibility.
# %%time
# 
# plot_loss_2 = PlotLossesCallback()
# 
# # Retrain model with fine-tuning
# vgg_ft_history = vgg_model_ft.fit(training_set,
#                                   batch_size=BATCH_SIZE,
#                                   epochs=n_epochs,
#                                   validation_data=validation_set,
#                                   steps_per_epoch=n_steps, 
#                                   validation_steps=n_val_steps,
#                                   callbacks=[tl_checkpoint_1, early_stop, plot_loss_2],
#                                   verbose=1)

"""### Prediction on test to be used later"""

vgg_preds_train = vgg_model_ft.predict(training_set)
vgg_preds_train

vgg_pred_classes_ft_train = np.argmax(vgg_preds_train, axis=1)
vgg_pred_classes_ft_train

"""## Checking performance on validation data"""

# Generate predictions
vgg_model_ft.load_weights('tl_model_v1.weights.best.hdf5') # initialize the best trained weights
true_classes_val = validation_set.classes
vgg_preds_ft_val = vgg_model_ft.predict(validation_set)
vgg_pred_classes_ft_val = np.argmax(vgg_preds_ft_val, axis=1)

vgg_acc_ft_val = accuracy_score(true_classes_val, vgg_pred_classes_ft_val)
print("VGG16 Model Accuracy with Fine-Tuning: {:.2f}%".format(vgg_acc_ft_val * 100))

"""### Predicting class label for unseen data i.e. 4000"""

# Loading predictions from last article's model
vgg_preds_ft = vgg_model_ft.predict(test_generator)
vgg_pred_classes_ft = np.argmax(vgg_preds_ft, axis=1)
df_predicted_labels_for_test_ft = pd.DataFrame(vgg_pred_classes_ft)
df_predicted_labels_for_test_ft.head()

df_predicted_labels_for_test_ft.columns =['Predictions']
df_predicted_labels_for_test_ft.value_counts()

df_predicted_labels_for_test_ft.to_csv('Predictions_labels_4000_unseen_test_data_with_VGG16_fine_tuned.csv')

"""## Checking on pre trained base model"""

from keras.models import load_model
scratch_model = load_model('/content/model_base.h5')
scratch_preds_validation = scratch_model.predict(validation_set)
scratch_pred_classes_validation = np.argmax(scratch_preds_validation, axis=1)
true_classes_val= validation_set.classes

scratch_acc_validation = accuracy_score(true_classes_val, scratch_pred_classes_validation)
print("From Scratch Model Accuracy with Fine-Tuning: {:.2f}%".format(scratch_acc_validation * 100))

"""## Checking Performance through confusion matrix

### Checking on Validation data
"""

import seaborn as sns
from sklearn.metrics import confusion_matrix
import matplotlib.pyplot as plt


# Get the names of the ten classes
class_names = validation_set.class_indices.keys()

def plot_heatmap(y_true, y_pred, class_names, ax, title):
    cm = confusion_matrix(y_true, y_pred)
    sns.heatmap(
        cm, 
        annot=True, 
        square=True, 
        xticklabels=class_names, 
        yticklabels=class_names,
        fmt='d', 
        cmap=plt.cm.Blues,
        cbar=False,
        ax=ax
    )
    ax.set_title(title, fontsize=16)
    ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha="right")
    ax.set_ylabel('True Label', fontsize=12)
    ax.set_xlabel('Predicted Label', fontsize=12)

fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(20, 10))

plot_heatmap(true_classes_val, scratch_pred_classes_validation, class_names, ax1, title="Custom CNN")    
plot_heatmap(true_classes_val, vgg_pred_classes_val, class_names, ax2, title="Transfer Learning (VGG16) No Fine-Tuning")    
plot_heatmap(true_classes_val, vgg_pred_classes_ft_val, class_names, ax3, title="Transfer Learning (VGG16) with Fine-Tuning")    

fig.suptitle("Confusion Matrix Model Comparison on Validation data", fontsize=24)
fig.tight_layout()
fig.subplots_adjust(top=1.10)
plt.show()

"""## Finding Confidence i.e. Probability of consolidation on train, test & validation"""

vgg_pred_classes_ft_val

# Create a dataframe with filenames
filenames = os.listdir("/content/new_data/")
categories = []
new_filenames = []
for filename in filenames:
    filename = "/content/new_data/" + filename
    new_filenames.append(filename)

train_df = pd.DataFrame({
    'filename': new_filenames,
})
train_df.head()

all_preds_16K = pd.DataFrame(vgg_pred_classes_ft_train)

only_val = pd.DataFrame(vgg_pred_classes_ft)

all_16K = pd.concat([all_preds_16K,only_val], ignore_index = True)
all_16K.head()

all_16K.columns =['category']
all_16K.head()

all_16K.shape

train_df['category'] = all_16K['category']
train_df.head()

train_df.shape

"""### Finding probability of consolidation on given data i.e. 16000 data for which true labels are known"""

from keras.preprocessing.image import load_img
sample_test = train_df.sample(n=21).reset_index()
sample_test.head()
plt.figure(figsize=(18, 18))
for index, row in sample_test.iterrows():
    prob_pred = np.max(vgg_preds_ft_val[index])
    filename = row['filename']
    category = row['category']
    img = load_img(filename, target_size=(224, 224))
    plt.subplot(7, 3, index+1)
    plt.imshow(img)
    if category == 0:
        class_guess = 'No Consolidation'
    else:
        class_guess = 'Consolidation Present'
    pred_label = '\n\nI think this is a ' + class_guess + ' with ' +str(round(float(prob_pred)*100,5)) + '% probability'
    plt.xlabel(pred_label + '(' + "{}".format(category) + ')')
plt.tight_layout()
plt.show()

from keras.preprocessing.image import load_img
sample_test = train_df.sample(n=21).reset_index()
sample_test.head()
plt.figure(figsize=(18, 18))
for index, row in sample_test.iterrows():
    prob_pred = np.max(vgg_preds_ft_val[index])
    filename = row['filename']
    category = row['category']
    img = load_img(filename, target_size=(224, 224))
    plt.subplot(7, 3, index+1)
    plt.imshow(img)
    if category == 1:
        class_guess = 'Consolidation Present'
        
    pred_label = '\n\nI think this is a ' + class_guess + ' with ' +str(round(float(prob_pred)*100,5)) + '% probability'
    plt.xlabel(pred_label + '(' + "{}".format(category) + ')')
plt.tight_layout()
plt.show()

from keras.preprocessing.image import load_img
sample_test = train_df.tail(4000).reset_index()
sample_test.head()
probability_val = []
for index, row in sample_test.iterrows():
    prob_pred = np.max(vgg_preds_ft_val[index])
    filename = row['filename']
    category = row['category']
    img = load_img(filename, target_size=(224, 224))
    if category == 1:
        class_guess = 'Consolidation Present'
        result_tes = filename + ' has consolidation with ' +  str(round(float(prob_pred)*100,2))+ '% probability'
        probability_val.append(result_tes)

from keras.preprocessing.image import load_img
sample_test = train_df.head(12000).reset_index()
sample_test.head()
probability_tr = []
for index, row in sample_test.iterrows():
    prob_pred = np.max(vgg_preds_train[index])
    filename = row['filename']
    category = row['category']
    img = load_img(filename, target_size=(224, 224))
    if category == 1:
        class_guess = 'Consolidation Present'
        result_tes = filename + ' has consolidation with ' +  str(round(float(prob_pred)*100,2))+ '% probability'
        probability_tr.append(result_tes)

probability_train = pd.DataFrame(probability_tr)
probability_train.columns =['Probability of consolidation']
probability_train.head(5)

probability_validation = pd.DataFrame(probability_val)
probability_validation.columns =['Probability of consolidation']
probability_validation.head(5)

Probability_consolidation_16000_images = pd.concat([probability_train, probability_validation], ignore_index = True)
Probability_consolidation_16000_images.head()

Probability_consolidation_16000_images.to_csv('Probability_consolidation_16000_images.csv')

"""### Finding probability of consolidation on Test Data i.e. 4000 data for which true labels are not known"""

# Create a dataframe with filenames
filenames = os.listdir("/content/test/")
categories = []
new_filenames = []
for filename in filenames:
    filename = "/content/test/" + filename
    new_filenames.append(filename)

test_df = pd.DataFrame({
    'filename': new_filenames,
})
test_df.head()

vgg_pred_classes_ft

test_df['category'] = vgg_pred_classes_ft
test_df.head()

test_df.category.value_counts()

from keras.preprocessing.image import load_img
sample_test = test_df.sample(n=21).reset_index()
sample_test.head()
plt.figure(figsize=(18, 18))
for index, row in sample_test.iterrows():
    prob_pred = np.max(vgg_preds_ft[index])
    filename = row['filename']
    category = row['category']
    img = load_img(filename, target_size=(224, 224))
    plt.subplot(7, 3, index+1)
    plt.imshow(img)
    if category == 0:
        class_guess = 'No Consolidation'
    else:
        class_guess = 'Consolidation Present'
    pred_label = '\n\nI think this is a ' + class_guess + ' with ' +str(round(float(prob_pred)*100,5)) + '% probability'
    plt.xlabel(pred_label + '(' + "{}".format(category) + ')')
plt.tight_layout()
plt.show()

from keras.preprocessing.image import load_img
sample_test = test_df.reset_index()
sample_test.head()
row = []
probability = []
for index, row in sample_test.iterrows():
    prob_pred = np.max(vgg_preds_ft[index])
    filename = row['filename']
    category = row['category']
    img = load_img(filename, target_size=(224, 224))
    if category == 1:
        class_guess = 'Consolidation Present'
        result_tes = filename + ' has consolidation with ' +  str(round(float(prob_pred)*100,2))+ '% probability'
        probability.append(result_tes)

probability

test_df_consolidation = test_df.loc[test_df['category'] == 1]
test_df_consolidation['Probability of consolidation on test'] = probability
test_df_consolidation.head()

test_df_consolidation.to_csv('Probability_consolidation_4000_test_images.csv')

