import os
from tensorflow.keras.models import load_model
from flask import Flask, render_template, request, Response
import cv2
import base64
from tensorflow.keras.preprocessing.image import load_img, img_to_array

app = Flask (__name__)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
model = load_model(os.path.join(BASE_DIR, 'model.h5'))

ALLOWED_EXT = set(['jpg', 'jpeg', 'png', 'jfif'])
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXT

classes = ['Bad', 'Good'] 

def predict(filename, model):
    img = load_img(filename, target_size = (120, 120))
    img = img_to_array(img)
    img = img.reshape(1, 120, 120, 3)

    img = img.astype('float32')
    img = img/255.0
    result = model.predict(img)

    dict_result = {}
    for i in range(2):
        dict_result[result[0][i]] = classes[i]

    res = result[0]
    res.sort()
    res = res[::-1]
    prob = res[:2]

    prob_result = []
    class_result = []
    for i in range(1):
        prob_result.append((prob[i]*100).round(2))
        class_result.append(dict_result[prob[i]])

    return class_result, prob_result

@app.route('/')
def home():
        return render_template("index.html")


@app.route("/save_image", methods = ["GET", "POST"])
def save_image():
    target_img = os.path.join(os.getcwd(), 'static/images')
    if request.method == "POST":
        img_file = request.json['image']
        decoded_image = base64.b64decode(img_file.split(",")[1])
        with open(f"{target_img}/{img_file}.jpg", "wb") as f:
            f.write(decoded_image)
        return render_template("index.html", img = img_file)


@app.route('/success', methods = ['GET', 'POST'])
def success():
    error = ''
    target_img = os.path.join(os.getcwd(), 'static/images')
    if request.method == 'POST':

            file = request.files['file']
            if file and allowed_file(file.filename):
                file.save(os.path.join(target_img, file.filename))
                img_path = os.path.join(target_img, file.filename)
                img = file.filename

                class_result, prob_result = predict(img_path, model)

                predictions = {
                        "class1": class_result,

                        "prob1": prob_result
                }

            else:
                error = "Please upload images of jpg , jfif, jpeg and png extension only"

            if(len(error) == 0):
                return render_template('success.html', img=img, predictions=predictions)
            else:
                return render_template('index.html', error=error)

    else:
        return render_template('index.html')

if __name__ == "__main__":
    app.run(port=4000, debug=True)