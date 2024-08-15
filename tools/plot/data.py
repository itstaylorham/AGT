# importing the module
import pandas as pd
  
# Display historical dsata as dataframe

# reading the file
data = pd.read_json("sesh.json")
  
# displaying the DataFrame
print(data)