import os, uuid
from tkinter import *
from tkinter.ttk import *
from tkinter.filedialog import askopenfile
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient
import zlib, base64
#import kwargs as kwargs

root = Tk()
root.geometry('700x600')
dir_= ""
name_= ""
connect_str = "DefaultEndpointsProtocol=https;AccountName=mystorageaccountname123;AccountKey=q5DQyUf07SfLJjEAnpI2zmd/TisHnydJQs6x8Ba4DMYh/kDmx3qnFX/8OQC4dq0XeIdyiVP5AwsVSioqBFKNKg==;EndpointSuffix=core.windows.net"


def upload_file():
    # bloob code
    try:
        print("Azure Blob storage v12 - Python quickstart sample")
        # Quick start code goes here
        #connect_str = os.getenv('AZURE_STORAGE_CONNECTION_STRING', )
        # connect_str = "q5DQyUf07SfLJjEAnpI2zmd/TisHnydJQs6x8Ba4DMYh/kDmx3qnFX/8OQC4dq0XeIdyiVP5AwsVSioqBFKNKg=="

        print(connect_str)

        # Create the BlobServiceClient object which will be used to create a container client
        global blob_service_client
        blob_service_client = BlobServiceClient.from_connection_string(connect_str)
        container_name = "mycontainer123"

        # Create a file in local data directory to upload and download
        local_path = label_d["text"]
        print(local_path)
        #local_file_name = name_ + str(uuid.uuid4()) + ".txt"
        local_file_name = label_n["text"]
        print(local_file_name)
        upload_file_path = os.path.join(local_path, local_file_name)

        # Write text to the file
        #file = open(upload_file_path, 'w')
        # file.write("Hello, World!")
        # file.close()

        # Create a blob client using the local file name as the name for the blob
        blob_client = blob_service_client.get_blob_client(container=container_name, blob=local_file_name)

        print("\nUploading to Azure Storage as blob:\n\t" + local_file_name)

        # Upload the created file
        with open(upload_file_path, "rb") as data:
            blob_client.upload_blob(data)

    except Exception as ex:
        print('Exception:')
        print(ex)

    root.destroy()



# This function will be used to open
# file in read mode and only Python files
# will be opened
def open_file():
    file = askopenfile(mode='r', filetypes=[('Select files', '*.*')])

    if file is not None:
        dir_ = os.path.dirname(file.name)
        filetype = os.path.splitext(file.name)
        name_= os.path.basename(file.name)

        label_n["text"]=name_
        dir_ = os.path.dirname(file.name)
        label_d["text"]=dir_
        size_ = os.stat(file.name)
        print('name: ', name_)
        print('path: ', dir_)
        print(f'size of file is  {size_.st_size / (1024 * 1024) : .4f} mb')
        compress(name_, dir_)

        #print(dir_)
        #print(filetype)
        #content = file.read()
        #print(content)

def compress(name_, dir_):
    print("inside compress function")
    var_f= "%s\%s"%(dir_,name_)
    file = open(var_f, 'r')
    text = file.read()
    file.close()
    #print("Uncompressed Text: \n" + text)
    # encoding the text
    code = base64.b64encode(zlib.compress(text.encode('utf-8'), 9))
    code = code.decode('utf-8')
    var_c="%s/compress_2.txt"%(dir_)
    label_n["text"] = "compress_2.txt"
    f = open(var_c, 'w')
    f.write(code)
    f.close()
    print("compression complete")

def extract_file():
    optionmenu = option_menu(None)
    print("File name obtained... Proceeding with compression...")


class option_menu(Tk):

    def __init__(self, parent):
        Tk.__init__(self, parent)
        self.parent = parent
        self.initialize()
        self.grid()

    def initialize(self):
        frame = Frame(root)
        # Create a Tkinter variable
        tkvar = StringVar(root)
        tkvar.set('Select')
        choices = list()
        print("\nListing blobs...")
        blob_service_client = BlobServiceClient.from_connection_string(connect_str)
        container_client = blob_service_client.get_container_client("mycontainer123")
        # List the blobs in the container
        blob_list = container_client.list_blobs()
        for blob in blob_list:
            choices.append(blob["name"])

        popupMenu = OptionMenu(frame, tkvar, *choices, command=self.func)
        Label(frame, text="Choose a file to decompress").pack()
        popupMenu.pack(side='left')
        frame.pack()

    def func(self, value):
        print(value)
        decompress(value)

def decompress(file_to_decompress):
    # Download the blob to a local file
    # Add 'DOWNLOAD' before the .txt extension so you can see both files in the data directory
    local_path = "C:/Users/admin/Desktop/Decompressed/download.txt"
    blob_service_client = BlobServiceClient.from_connection_string(connect_str)
    download_file_path = local_path
    container_name = "mycontainer123"
    blob_client = blob_service_client.get_blob_client(container=container_name, blob=file_to_decompress)
    print("\nDownloading blob to \n\t" + download_file_path)

    with open(download_file_path, "wb") as download_file:
        download_file.write(blob_client.download_blob().readall())
        #print("Download completed for the file: ", file_to_decompress)

    print("Decompressing the file...")

    file = open(download_file_path, 'r')
    text = file.read()
    file.close()
    # decode the encoded text
    decoded_txt = zlib.decompress(base64.b64decode(text))
    decompress_path = "C:/Users/admin/Desktop/Decompressed/decompressed.txt"

    f = open(decompress_path, 'wb')
    f.write(decoded_txt)
    f.close()

    print("File decompressed and placed in the folder....")

label_n = Label(root, text="")
label_d = Label(root, text="")
btn = Button(root, text='Open', command=lambda: open_file())
btn1 = Button(root, text='Upload', command=lambda: upload_file())
btn2 = Button(root, text='Extract', command=lambda: extract_file())
btn.pack(side=TOP, pady=15)
btn1.pack(side=TOP, pady=15)
btn2.pack(side=TOP, pady=15)
label_n.pack()
#label_n.visible = False
label_d.pack()

#label_d.visible = False
root.mainloop()