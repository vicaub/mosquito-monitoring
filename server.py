from flask import Flask, request, render_template, send_file
from db_model.Mosquito import Mosquito
from db_model.User import User
from classification.preprocessing import Preprocessing
import os
import zipfile

app = Flask(__name__)

@app.route("/")
def renderHTML():
    return render_template("index.html")


@app.route("/postform", methods=["POST"])
def postForm():
    form = request.form
    files = request.files

    print(form)
    print(files)

    user = User(form["name"], form["email"])

    files["fileToUpload"].save("./tmp/" + files["fileToUpload"].filename)

    mosquito = Mosquito(user, "./tmp/" + files["fileToUpload"].filename)
    coords = Preprocessing.mosquito_position(mosquito.picture)


    cropped_pic = Preprocessing.save_crop_img(coords, mosquito.picture, mosquito.picture + "_crop")
    framed_pic = Preprocessing.save_framed_img(coords, mosquito.picture, mosquito.picture + "_framed")

    os.remove("./tmp/" + files["fileToUpload"].filename)

    zipf = zipfile.ZipFile('Name.zip', 'w', zipfile.ZIP_DEFLATED)
    for root, dirs, files in os.walk('output/'):
        for file in files:
            zipf.write('output/' + file)
    zipf.close()
    return send_file('Name.zip',
                     mimetype='zip',
                     attachment_filename='Name.zip',
                     as_attachment=True)

    return send_file(, mimetype='image/gif')

if __name__ == "__main__":
    app.run()
