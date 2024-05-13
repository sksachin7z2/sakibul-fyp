import argparse
from flask import Flask, render_template, request
from werkzeug.utils import send_from_directory
import os
import cv2
from ultralytics import YOLO

app = Flask(__name__)

@app.route("/")
def hello_world():
    return render_template('index.html')


@app.route("/", methods=["GET", "POST"])
def predict_img():
    if request.method == "POST":
        if 'file' in request.files:
            f=request.files['file'] 
            basepath = os.path.dirname(__file__)
            filepath = os.path.join(basepath,'uploads', f.filename)

            print("upload folder is ", filepath)
            
            f.save(filepath)
            global imgpath
            predict_img.imgpath = f.filename
            print("printing predict_img :", predict_img)

            file_extension = f.filename.rsplit('.', 1)[1].lower()

            if file_extension == 'jpg':
                img = cv2.imread(filepath)

                #Perform the detection
                model = YOLO('best.pt')
                detections = model(img, save=True)
                return display(f.filename)
    
    folder_path = 'runs/detect'
    subfolders = [f for f in os.listdir(folder_path) if os.path.isdir(os.path.join(folder_path, f))]
    latest_subfolder = max(subfolders, key=lambda x: os.path.getctime(os.path.join(folder_path, x)))
    image_path = folder_path + '/' + latest_subfolder + '/' + f.filename
    return render_template('index.html', image_path=image_path)

@app.route('/<path:filename>')
def display(filename):
    folder_path = 'runs/detect'
    subfolders = [f for f in os.listdir(folder_path) if os.path.isdir(os.path.join(folder_path, f))]    
    latest_subfolder = max(subfolders, key=lambda x: os.path.getctime(os.path.join(folder_path, x)))    
    directory = folder_path+'/'+latest_subfolder    
    print("printing directory: ",directory) 
    files = os.listdir(directory)
    latest_file = files[0]
    
    print(latest_file)

    filename = os.path.join(folder_path, latest_subfolder, latest_file)

    file_extension = filename.rsplit('.', 1)[1].lower()

    environ = request.environ
    if file_extension == 'jpg':      
        return send_from_directory(directory,latest_file,environ) #shows the result in seperate tab

    else:
        return "Invalid file format"
    


@app.route('/<path:filename>')
def displayImage(filename):
    return render_template('index.html', image_path=filename)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Flask app exposing yolov9 models")
    parser.add_argument("--port", default=8000, type=int, help="port number")
    args = parser.parse_args()
    model = YOLO('best.pt')
    app.run(host="0.0.0.0", port=args.port)