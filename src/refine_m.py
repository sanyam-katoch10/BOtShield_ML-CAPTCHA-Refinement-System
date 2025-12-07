
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'  


import numpy as np
from PIL import Image
from tensorflow.keras.models import load_model
from generator import generate_captcha

model=load_model("models/captcha_model.keras")
cls=["easy","medium","hard"]

def predict(img):
    arr=np.array(img.resize((200,70))).astype("float32")/255
    arr=np.expand_dims(arr,0)
    p=model.predict(arr,verbose=0)[0]
    i=np.argmax(p)
    return cls[i],p[i]

def refine(target="medium",steps=4):
    d={"easy":0,"medium":1,"hard":2}
    noise=0.3; dist=0.3; clutter=0.3
    for _ in range(steps):
        img,text=generate_captcha(noise,dist,clutter)
        p,_=predict(img)
        if p==target:
            return img,text,p
        if d[p]<d[target]:
            noise=min(1,noise+0.15)
            dist=min(1,dist+0.1)
            clutter=min(1,clutter+0.1)
        else:
            noise=max(0,noise-0.15)
            dist=max(0,dist-0.1)
            clutter=max(0,clutter-0.1)
    return img,text,p

img, text, pred = refine("medium")

print("Generated CAPTCHA text:", text)
print("Predicted difficulty:", pred)
img.show() 

