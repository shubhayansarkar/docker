import flask
import pandas as pd
from flask import *
import os
import json
from azure.storage.blob import BlobServiceClient
import imgpre
from imgpre import *


app = Flask(__name__)

os.environ['AZURE_STORAGE_CONNECTION_STRING'] = "DefaultEndpointsProtocol=https;AccountName=trial22;AccountKey=+fNPmToXAhJmJq/PYua9I2l8Kr4oD4j+Cvyf9N1ANqKbRPGCvEB6gRoo1H5pCLCt9YNi4ZZzhHmgF83WPNUyxA==;EndpointSuffix=core.windows.net"
connect_str = os.getenv('AZURE_STORAGE_CONNECTION_STRING') # retrieve the connection string from the environment variable
container_name = "photoes" # container name in which images will be store in the storage account
blob_service_client = BlobServiceClient.from_connection_string(conn_str=connect_str) # create a blob service client to interact with the storage account
try:
    container_client = blob_service_client.get_container_client(container=container_name) # get container client to interact with the container in which images will be stored
    container_client.get_container_properties() # get properties of the container to force exception to be thrown if container does not exist
except Exception as e:
    print(e)
    print("Creating container...")
    container_client = blob_service_client.create_container(container_name)


app.config["UPLOAD_PATH"]=r"static\uploads"


@app.route('/')
def upload():
    return render_template("index.html")


@app.route('/success', methods=['GET','POST'])
def success():
    filenames = ""
    dataname=""
    if request.method == 'POST':
        f=request.files.getlist('file')
        for j in f:
            name = j.filename
            try:
                container_client.upload_blob(name,j)  # upload the file to the container using the filename as the blob name
                filenames += name + "<br /> "
            except Exception as e:
                print(e)
                print("Ignoring duplicate filenames")  # ignore duplicate filenames
            print(f)
            name1="0199.jpg"
            print(name)
            j.save(os.path.join(app.config["UPLOAD_PATH"], name))
            x = imgpre.txt(name)
            print(x)
            # col=x.columns
            # val=x.values
            data = json.loads(x.to_json(orient='records'))

        blob_items = container_client.list_blobs()  # list all the blobs in the container
        img_html = "<div style='display: flex; justify-content: space-between; flex-wrap: wrap;'>"

        for blob in blob_items:
            blob_client = container_client.get_blob_client(
                blob=blob.name)  # get blob client to interact with the blob and get blob url
            img_html += "<img src='{}'/>".format(
                blob_client.url)  # get the blob url and append it to the html

        img_html += "</div>"
        print(img_html)

        imgurl=f"https://trial22.blob.core.windows.net/photoes/{name}"

        return render_template("result.html",dt=f,data=data,imgurl=imgurl)



if __name__ == '__main__':
    # app.run(host='192.168.196.21',port=5000,threaded=False,debug=True)
    app.run(debug=True)