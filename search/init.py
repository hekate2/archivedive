import shutil
import os
import threading
from dumps import dump_data

def dump_data_thread():
    dump_data()

dir_path = os.path.dirname(os.path.realpath(__file__))
index_folder = os.path.join(dir_path, "index")
print("INDEX FOLDER LOC: " + index_folder)

sites_db = os.path.join(dir_path, "data", "sites.db")
sites_csv = os.path.join(dir_path, "data", "sites.csv")

os.remove(sites_db)
# Run dump_data() in a separate thread and wait for it
thread = threading.Thread(target=dump_data_thread)
thread.start()
thread.join()

if os.path.exists(index_folder):
    shutil.rmtree(index_folder)
    print("Deleted 'index' folder.")
else:
    print("'index' folder does not exist.")

os.makedirs(index_folder, exist_ok=True)