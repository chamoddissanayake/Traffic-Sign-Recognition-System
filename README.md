
# Traffic Sign Recognition System


The Traffic Sign Recognition System is a machine learning application designed to identify and classify various traffic signs from images. Using a convolutional neural network (CNN) model, the system processes uploaded images, predicts the corresponding traffic sign, and returns its classification. It supports real-time image uploads and leverages a well-structured dataset for training. The system is user-friendly, enabling efficient and accurate recognition of traffic signs, enhancing road safety and navigation.
## Run Locally

Install Python 3.10.0


  https://www.python.org/downloads/release/python-3100/

Install Node 21.6.2


  https://nodejs.org/en/blog/release/v21.6.2


Clone the project

```bash
  git clone https://github.com/chamoddissanayake/Traffic-Sign-Recognition-System.git
```

Go to Frontend Folder

```bash
  Frontend > traffic-sign-recognition
```

Install dependencies

```bash
  npm install
```

Start the Frontend

```bash
  npm start
```

Go to Frontend Web App

```bash
  http://localhost:3000/
```

Go to Backend Folder

```bash
  Backend >
```

Install dependencies

```bash
  pip install -r requirements.txt
```

Go to Service Folder

```bash
  Backend > service
```

Start the Backend

```bash
  python traffic_sign_microservice.py
```
## Tech Stack

**Programming Language:**

  * Python
  * Typescript

**Web Framework:**

  * Flask
  * React

**Machine Learning Framework:**

  * Keras (with TensorFlow backend)

**Image Processing Libraries:**

  * PIL (Pillow)
  * NumPy

**Data Handling:**

  * pandas (if used for data manipulation)

**Model Training:**

  * Keras for model building and training
  * scikit-learn for data splitting
## Usage/Examples


POST Method

```bash
http://localhost:5007/classify
```

Request
```javascript
{
  "image_path": "../images/08357.png"
}
```
Response
```javascript
{
    "sign": "Turn right ahead"
}
```
