from azure.storage.blob import BlobServiceClient
import os
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
def addtoblob(containername,file):
    filenames=""
    try:
        container_client.upload_blob(containername,file)  # upload the file to the container using the filename as the blob name
        filenames += container_name+ "<br /> "
    except Exception as e:
        print(e)
        print("Ignoring duplicate filenames")  # ignore duplicate filenames

def showblobimg():
    blob_items = container_client.list_blobs()  # list all the blobs in the container
    img_html = "<div style='display: flex; justify-content: space-between; flex-wrap: wrap;'>"

    for blob in blob_items:
        blob_client = container_client.get_blob_client(
            blob=blob.name)  # get blob client to interact with the blob and get blob url
        img_html += "<img src='{}'width='auto' height='200' style='margin: 0.5em 0;'/>".format(
            blob_client.url)  # get the blob url and append it to the html

    img_html += "</div>"
    print(img_html)
# addtoblob('data1','imgpre.py')