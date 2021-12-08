import flask
import pandas as pd
from flask import *
import os
import json

import imgpre
from imgpre import *


app = Flask(__name__)

app.config["UPLOAD_PATH"]=r"static\uploads"


@app.route('/')
def upload():
    return render_template("index.html")


@app.route('/success', methods=['GET','POST'])
def success():
    if request.method == 'POST':
        f=request.files.getlist('file')
        print(f)
        for i in f:
            name=i.filename
            print(name)
            i.save(os.path.join(app.config["UPLOAD_PATH"],name))
            x=imgpre.txt(name)
            print(x)
            # col=x.columns
            # val=x.values
            data=json.loads(x.to_json(orient='records'))
            print(data)

        return render_template("result.html",dt=f,data=data)



if __name__ == '__main__':
    # app.run(host='192.168.196.21',port=5000,threaded=False,debug=True)
    app.run(debug=True)