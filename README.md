# Creating 3D model from 2D image and showing the model in AR on website

This repository contains our implementation of creating a 3d model from single image using [PyTorch MiDaS](https://pytorch.org/hub/intelisl_midas_v2/) and then showing the model in augmented reality on website using [AR.js](https://ar-js-org.github.io/AR.js-Docs/).

## instalation 


To create a model from picture yourself you should follow this steps:

***! IMPORTANT !: Please make sure you are using Python 3.8.12***

1. Clone repo:

`git clone https://github.com/smeyanoff/image-depth-estimation`

2. Install all the requirements:

`pip install -r requirements.txt`

3. [Download](https://drive.google.com/drive/folders/13TJ4PCw4N65R13PN6ozzgmc8F0lBD9x8?usp=share_link) model wights and add to `depth_estimator/weights` dir.


---

To display the model in AR you should follow this steps:
1. Run the server on your localhost:
`cd visualisation
python -m http.server
`

2. If you have a webcamera on your PC you should download this picture:
![hiro](https://user-images.githubusercontent.com/27068383/201076772-b0a1b911-7b82-47eb-9933-7bea8d2dff8f.png)


3. You also can run the website on your other device with camera. To host this website with your PC and open it on other device you can install [ngrok](https://ngrok.com) and then run this command:
`
ngrok http 80
`
