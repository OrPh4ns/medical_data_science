import time

from webdav3.client import Client
from dotenv import dotenv_values


class NasController:
    def __init__(self):
        env = dotenv_values()
        self.nas_host = env['NASHOST']
        self.nas_user = env['NASUSER']
        self.nas_pass = env['NASPASS']
        self.remote_path = []
        self.found = False
        self.counter = 0
        self.org = {
            'webdav_hostname': self.nas_host,
            'webdav_login': self.nas_user,
            'webdav_password': self.nas_pass,
        }

    def download_start(self, option):
        client = Client(option)
        files = client.list()
        for i in range(1, len(files)):
            if "/" in files[i]:
                print("\033[0m Folder Found ][ " + ''.join(self.remote_path) + files[i] + "\n")
                if self.found:
                    self.remote_path.pop()
                    self.found = False
                self.remote_path.append(files[i])
                options = {
                    'webdav_hostname': self.nas_host + "/" + '/'.join(self.remote_path),
                    'webdav_login': self.nas_user,
                    'webdav_password': self.nas_pass,
                }
                self.download_start(options)
            elif ".dcm" in files[i]:
                local_file_path = 'uploads/' +str(int(time.time()))+"_"+str(self.counter) + "_" + files[i]
                client2 = Client(self.org)
                print("\033[92m DICOM Found ][ " + ''.join(self.remote_path) + files[i])
                client2.download(''.join(self.remote_path) + files[i], local_file_path)
                self.counter += 1
                self.found = True

            # Check if the current file is the last file in the current folder
            if i == len(files) - 1 and self.remote_path:
                self.remote_path.pop()
                print("\033[91m Back to Folder ][ " + ''.join(self.remote_path))
                self.found = False
