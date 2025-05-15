import os
import time

DATA_LAKE_DIR = "data_lake/all_transactions"
RETENTION_DAYS = 7
now = time.time()

for folder in os.listdir(DATA_LAKE_DIR):
    path = os.path.join(DATA_LAKE_DIR, folder)
    if os.path.isdir(path):
        creation_time = os.path.getctime(path)
        age_days = (now - creation_time) / 86400
        if age_days > RETENTION_DAYS:
            print(f" Suppression : {path}")
            os.system(f"rm -r {path}")