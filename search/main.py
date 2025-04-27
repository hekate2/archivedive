import shutil
import os
from dumps import dump_data

dir_path = os.path.dirname(os.path.realpath(__file__))
index_folder = os.path.join(dir_path, "index")
sites_db = os.path.join(dir_path, "data", "sites.db")

if not os.path.exists(sites_db):
    dump_data()

if os.path.exists(index_folder):
    shutil.rmtree(index_folder)
    print("Deleted 'index' folder.")
else:
    print("'index' folder does not exist.")

os.makedirs(index_folder, exist_ok=True)

import server.app