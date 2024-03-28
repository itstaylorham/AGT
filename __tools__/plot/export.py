# importing the module
import pandas as pd
from datetime import datetime
import os
  
# reading the file
data = pd.read_json("__files__/file.json")

timestamp = datetime.now().strftime("%Y-%m-%d-%H:%M:%S")
if not os.path.exists("read_files"):
    os.makedirs("read_files")
data.to_csv(f'plot/exports/{timestamp}.csv')
done = True