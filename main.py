from colorthief import ColorThief
import matplotlib.pyplot as plt
from flask import Flask, render_template, request, redirect, url_for, flash
from wtforms import FileField, SubmitField
from flask_wtf import FlaskForm
from werkzeug.utils import secure_filename
import os

UPLOAD_FOLDER = 'static/files'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
filename = None

app = Flask(__name__)
app.config['SECRET_KEY'] = 'KJSDFGJHFVREFKUYGFALEJREGL36289HJFW'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

class UploadFileForm(FlaskForm):
    file = FileField('File')
    submit = SubmitField('Upload File')


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS



@app.route('/', methods=['GET', "POST"])
def home():
    global filename
    if filename:
        os.remove(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    form = UploadFileForm()
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        print(file)
        print(file.filename)
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('colors'))
    return render_template('index.html', form=form)


@app.route('/colors')
def colors():
    ct = ColorThief(f'static/files/{filename}')
    dominant_color = ct.get_color(quality=1)
    palette = ct.get_palette(color_count=5)
    plt.imshow([[palette[i] for i in range(5)]])
    return render_template('colors.html', file=filename, dc=dominant_color, pl=palette)

@app.route('/refresh')
def refresh():
    return redirect(url_for('home'))


if __name__ == '__main__':
    app.run(debug=True)
