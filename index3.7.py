import os, uuid
from tkinter import *
from tkinter.ttk import *
from tkinter.filedialog import askopenfile
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient
import kwargs as kwargs

dir_= "C:/Users/rahulshi/Desktop/my/20200402/"
name_ = 0

# bloob code
try:
    print("Azure Blob storage v12 - Python quickstart sample")
    # Quick start code goes here
    connect_str = os.getenv('AZURE_STORAGE_CONNECTION_STRING',)
    #connect_str = "q5DQyUf07SfLJjEAnpI2zmd/TisHnydJQs6x8Ba4DMYh/kDmx3qnFX/8OQC4dq0XeIdyiVP5AwsVSioqBFKNKg=="
    #connect_str = "DefaultEndpointsProtocol=https;AccountName=mystorageaccountname123;AccountKey=q5DQyUf07SfLJjEAnpI2zmd/TisHnydJQs6x8Ba4DMYh/kDmx3qnFX/8OQC4dq0XeIdyiVP5AwsVSioqBFKNKg==;EndpointSuffix=core.windows.net"
    print(connect_str)

    # Create the BlobServiceClient object which will be used to create a container client
    blob_service_client = BlobServiceClient.from_connection_string(connect_str)
    container_name = "mycontainer123"

    # Create a file in local data directory to upload and download
    local_path = dir_
    local_file_name = "quickstart" + str(uuid.uuid4()) + ".txt"
    upload_file_path = os.path.join(local_path, local_file_name)

    # Write text to the file
    file = open(upload_file_path, 'w')
    file.write("Hello, World!")
    file.close()

    # Create a blob client using the local file name as the name for the blob
    blob_client = blob_service_client.get_blob_client(container=container_name, blob=local_file_name)

    print("\nUploading to Azure Storage as blob:\n\t" + local_file_name)

    # Upload the created file
    with open(upload_file_path, "rb") as data:
        blob_client.upload_blob(data)

except Exception as ex:
    print('Exception:')
    print(ex)


