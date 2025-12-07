
import os, numpy as np
from sklearn.model_selection import train_test_split
from tensorflow.keras import layers, models
from tensorflow.keras.utils import to_categorical

X=[]; y=[]
cls=["easy","medium","hard"]
for i,c in enumerate(cls):
    for f in os.listdir(f"data_preprocessed/{c}"):
        X.append(np.load(f"data_preprocessed/{c}/{f}"))
        y.append(i)

X=np.array(X).reshape(-1,70,200,3)
y=to_categorical(np.array(y),3)

Xtr,Xte,ytr,yte=train_test_split(X,y,test_size=0.2)

m=models.Sequential([
    layers.Input((70,200,3)),
    layers.Conv2D(32,(3,3),activation="relu"),
    layers.MaxPooling2D(),
    layers.Conv2D(64,(3,3),activation="relu"),
    layers.MaxPooling2D(),
    layers.Flatten(),
    layers.Dense(128,activation="relu"),
    layers.Dense(3,activation="softmax")
])

m.compile(optimizer="adam",loss="categorical_crossentropy",metrics=["accuracy"])
m.fit(Xtr,ytr,epochs=12,batch_size=32,validation_split=0.1)
os.makedirs("models",exist_ok=True)
m.save("models/captcha_model.keras")

