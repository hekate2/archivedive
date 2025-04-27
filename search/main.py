import shutil
import os

dir_path = os.path.dirname(os.path.realpath(__file__))
index_folder = os.path.join(dir_path, "index")

if os.path.exists(index_folder):
    shutil.rmtree(index_folder)
    print("Deleted 'index' folder.")
else:
    print("'index' folder does not exist.")

os.makedirs(index_folder, exist_ok=True)

import server.app