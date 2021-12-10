import flask
import pandas as pd
from flask import *
import os
import json

import azureconfig
import imgpre
from imgpre import *
from azureconfig import *

app = Flask(__name__)



app.config["UPLOAD_PATH"]=r"static\uploads"


@app.route('/')
def upload():
    return render_template("index.html")


@app.route('/success', methods=['GET','POST'])
def success():
    if request.method == 'POST':
        f=request.files.getlist('file')
        name1=''
        for j in f:
            name = j.filename
            print(type(name))
            name1 += f"{name}_output, "
            print(name1)
            print(type(name1))
            azureconfig.addtoblob(name,j)
            print(f)

            print(name)
            j.save(os.path.join(app.config["UPLOAD_PATH"], name))
            x = imgpre.txt(name)# img to tesseract
            print(x)
            # col=x.columns
            # val=x.values
            data = json.loads(x.to_json(orient='records'))# data in json
            s = open(r"static/data.txt", "w+")
            for y in data:
                s.write(str(y) + '\n')
            s.close()
            a=f'{data}'

            addtoblob(name1,a)
        azureconfig.showblobimg()#showing image

        imgurl=f"https://trial22.blob.core.windows.net/photoes/{name}"

        return render_template("result.html",dt=f,data=data,imgurl=imgurl)



if __name__ == '__main__':
    # app.run(host='192.168.196.21',port=5000,threaded=False,debug=True)
    app.run(debug=True)