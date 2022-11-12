# Creating 3D model from 2D image and showing the model in AR on website

This repository contains our implementation of creating a 3d model from single image using [PyTorch MiDaS](https://pytorch.org/hub/intelisl_midas_v2/) and then showing the model in augmented reality on website using [AR.js](https://ar-js-org.github.io/AR.js-Docs/). 
If you want to watch saved 3d objects, download [this](https://www.meshlab.net/#download).

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

1. Download [this](https://drive.google.com/file/d/1wjN1vsNTyyyofeo-0U_VWO305y0F-mro/view?usp=sharing) 3D model object (or any other and name it "test_object") and put it in *visualisation* directory
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

### Our goal in models testing was to evaluete how accurately they can predict depth of common domestick objects

In this way we used RGBD dataset was found [here](https://www.kaggle.com/datasets/metagrasp/metagraspnetdifficulty1-easy)

Our metric was MAE and we compared model`s predicted depth with true object depth. Moreover we evaluated run-time

| photo_name | model       | MAE    | run-time (sec) |
|------------|-------------|--------|----------------|
| 0          | DPT_Large   | 62.28  | 0.728810       |
| 1          | DPT_Large   | 123.02 | 0.551458       |
| 2          | DPT_Large   | 111.97 | 0.575197       |
| 3          | DPT_Large   | 122.65 | 0.557782       |
| 4          | DPT_Large   | 111.37 | 0.569186       |
| 5          | DPT_Large   | 116.99 | 0.566448       |
| 6          | DPT_Large   | 111.79 | 0.558274       |
| 7          | DPT_Large   | 122.68 | 0.552736       |
| 8          | DPT_Large   | 111.23 | 0.559168       |
| 0          | MiDaS_small | 200.15 | 0.258206       |
| 1          | MiDaS_small | 157.51 | 0.037596       |
| 2          | MiDaS_small | 286.24 | 0.033803       |
| 3          | MiDaS_small | 361.18 | 0.036079       |
| 4          | MiDaS_small | 258.91 | 0.033406       |
| 5          | MiDaS_small | 167.70 | 0.034455       |
| 6          | MiDaS_small | 197.53 | 0.036982       |
| 7          | MiDaS_small | 323.14 | 0.035028       |
| 8          | MiDaS_small | 228.32 | 0.035127       |
| 0          | glpn        | 61.89  | 0.093825       |
| 1          | glpn        | 125.74 | 0.100389       |
| 2          | glpn        | 140.61 | 0.106214       |
| 3          | glpn        | 129.60 | 0.097953       |
| 4          | glpn        | 141.15 | 0.114711       |
| 5          | glpn        | 127.72 | 0.114895       |
| 6          | glpn        | 140.60 | 0.114242       |
| 7          | glpn        | 128.32 | 0.117232       |
| 8          | glpn        | 141.58 | 0.107963       |

Mean result

| model       | MAE        | run-time (sec) |
|-------------|------------|----------------|
| DPT_Large   | 110.442222 | 0.579895       |
| MiDaS_small | 242.297778 | 0.060076       |
| glpn        | 126.356667 | 0.107492       |


## Algorithm performance

Models were evaluated on system with 12th Gen Intel(R) Core(TM) i5-12450H   2.00 GHz and GeForce MX550. We need to evaluate depth not only for one photo but more than six, than we need multiply run-time on count of photos plus time to build 3D object. 

## Reference

[PyTorch MiDaS](https://pytorch.org/hub/intelisl_midas_v2/)

[AR.js](https://ar-js-org.github.io/AR.js-Docs/)
