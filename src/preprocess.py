import os, numpy as np
from generator import generate_captcha

os.makedirs("data_preprocessed",exist_ok=True)
cls=["easy","medium","hard"]
for c in cls:
    os.makedirs(f"data_preprocessed/{c}",exist_ok=True)

for i in range(2000):
    img,_=generate_captcha(0,0,0)
    np.save(f"data_preprocessed/easy/{i}.npy",np.array(img.resize((200,70)))/255)

for i in range(2000):
    img,_=generate_captcha(0.3,0.3,0.2)
    np.save(f"data_preprocessed/medium/{i}.npy",np.array(img.resize((200,70)))/255)

for i in range(2000):
    img,_=generate_captcha(0.7,0.7,0.6)
    np.save(f"data_preprocessed/hard/{i}.npy",np.array(img.resize((200,70)))/255)
