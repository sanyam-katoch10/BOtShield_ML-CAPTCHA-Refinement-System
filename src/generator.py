from captcha.image import ImageCaptcha
import random, string, numpy as np, cv2
from PIL import Image

def random_text(n=5):
    return ''.join(random.choice(string.ascii_uppercase+string.digits) for _ in range(n))

def cv2_to_pil(x):
    return Image.fromarray(cv2.cvtColor(x, cv2.COLOR_BGR2RGB))

def pil_to_cv2(x):
    return cv2.cvtColor(np.array(x), cv2.COLOR_RGB2BGR)

def generate_captcha(noise=0.0, dist=0.0, clutter=0.0, text=None):
    if text is None:
        text = random_text()
    gen = ImageCaptcha(width=200, height=70)
    img = gen.generate_image(text)
    img = pil_to_cv2(img)
    h,w=img.shape[:2]
    if dist>0:
        pts1=np.float32([[0,0],[w,0],[0,h]])
        pts2=np.float32([[random.randint(-5,5),random.randint(-3,3)],
                         [w+random.randint(-5,5),random.randint(-3,3)],
                         [random.randint(-5,5),h+random.randint(-3,3)]])
        M=cv2.getAffineTransform(pts1,pts2)
        img=cv2.warpAffine(img,M,(w,h))
    if noise>0:
        amt=int(150*noise)
        for _ in range(amt):
            x=random.randint(0,w-1)
            y=random.randint(0,h-1)
            img[y,x]=[random.randint(0,255) for _ in range(3)]
    if clutter>0:
        cnt=int(6*clutter)
        for _ in range(cnt):
            x1,y1=random.randint(0,w),random.randint(0,h)
            x2,y2=random.randint(0,w),random.randint(0,h)
            cv2.line(img,(x1,y1),(x2,y2),(random.randint(0,255),random.randint(0,255),random.randint(0,255)),1)
    return cv2_to_pil(img), text

