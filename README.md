# Creating 3D model from 2D image and showing the model in AR on website

This repository contains our implementation of creating a 3d model from single image using [PyTorch MiDaS](https://pytorch.org/hub/intelisl_midas_v2/) and then showing the model in augmented reality on website using [AR.js](https://ar-js-org.github.io/AR.js-Docs/).

## Task

We want to make an algorithm that creates 3D model of furniture from 2D images. Then we want to fit this furniture in the interior of the room using AR, so we needed a website that can show the 3D model using your camera. 

## Installation 

To create a model from picture yourself you should follow this steps:

***! IMPORTANT !: Please make sure you are using Python 3.8.n***

1. Clone repo:

`git clone https://github.com/smeyanoff/image-depth-estimation`

2. Install all the requirements:

`pip install -r requirements.txt`

---

To display the example 3D model in AR you should follow this steps:

1. Download [this](https://drive.google.com/file/d/17ADHEdwKrz4rE9oNZdG7C44uUbicCnlf/view?usp=sharing) 3D model object (or any other and name it "test_object.obj") and put it in *visualisation* directory
2. Run the server on your localhost:

`cd visualisation`

`python -m http.server`


2. If you open the website on your localhost you should allow the access to camera. On AR.js we define specific 3D models for specific markers, so when the camera recognizes a marker, the web-app shows the 3D model on top of it. The marker for example model is shown below (for example you open web-app on PC, turn on the webcamera, download the marker on your phone and place the marker in front of webcamera):
<img src="https://user-images.githubusercontent.com/27068383/201076772-b0a1b911-7b82-47eb-9933-7bea8d2dff8f.png" alt="hiro" width="200"/>

The model that is shown as an example is located in visualisation/object directory (you can change it).

3. You also can run the website on your other device with camera. To host this website with your PC and open it on other device you can install [ngrok](https://ngrok.com) and then run this command:
`
ngrok http 80
`

## Solution

The pipeline can be seen in pipeline.py:

1. First we take the picture from *test/photos* directory, read it and pass to MiDaS depth estimator
2. Once depth of the picture is estimated the result of this calculation is saved in *test/depth_predicted* directory:

<img src="https://user-images.githubusercontent.com/27068383/201118396-dd38f952-04b8-417c-aa3a-e4d057af8eed.jpg" alt="depth_predicted" width="300"/>

3. Then the .obj object is saved:

![Запись-экрана-2022-11-10-в-17 44 12](https://user-images.githubusercontent.com/27068383/201122720-e0b7ac7e-c900-47de-b04e-166b25f72f22.gif)


In future we want to figure out how we can pass multiple pictures of object from different angles to create a full model that will be accurate enough. Some code of the project is not deleted due to testing reasons.

## Project tree

```
.
├── depth_estimator
│   ├── glpn.py                             - this code is for testing the other model
│   ├── midas.py                            - depth prediction code
│   └── weights
│       ├── config.json
│       ├── preprocessor_config.json
│       └── pytorch_model.bin 
├── pipeline.py                             - ML-pipeline code
├── requirements.txt
├── models_testing.ipynb                    - file with models evaluation and compairing
├── settings.py
└── test
│   ├── depth_predicted                     - predicted depth of an image
│   ├── objects                             - saved .obj 3D objects created from pictures
│   └── photos                              - source pictures (can be in .jpg .png)
└── visualisation
    └── index.html                          - HTML-code of website to scan and show the 3d model on the marker (created using AR.js)
```

## Experiments

You can have a look on evaluation of the models in model_testing.ipynb 

## Reference

[PyTorch MiDaS](https://pytorch.org/hub/intelisl_midas_v2/)

[AR.js](https://ar-js-org.github.io/AR.js-Docs/)
