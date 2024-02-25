from flask import Flask, request, render_template, flash, redirect, url_for
from super_image import PanModel, ImageLoader
from PIL import Image
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = './uploads'
app.config['STATIC_FOLDER'] = './static'
app.config['TEMPLATES_AUTO_RELOAD'] = True

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    try:
        if 'image' not in request.files:
            flash('No file part')
            return redirect(request.url)

        file = request.files['image']

        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)

        if file:
            filename = file.filename
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)

            image = Image.open(filepath)

            model = PanModel.from_pretrained('eugenesiow/pan', scale=2)
            inputs = ImageLoader.load_image(image)
            preds = model(inputs)

            output_path = os.path.join(app.config['STATIC_FOLDER'], 'scaled_2x.png')
            ImageLoader.save_image(preds, output_path)

            print("Input Image Path:", filepath)
            print("Output Image Path:", output_path)

            return render_template('result.html', input_path=filepath, output_path=output_path)
    except Exception as e:
        flash('An error occurred during image processing')
        print("Error:", str(e))
        return redirect(request.url)


