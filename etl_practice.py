# ************ Modules ************
import glob 
import pandas as pd 
import xml.etree.ElementTree as ET 
from datetime import datetime 

# ************ File Paths ************
log_file = "log_file.txt"               # Stores logs
target_file = "transformed_data.csv"    # Final output for loading into DB


# ************ Functions ************
# Extract data from CSV
def extract_from_csv(file_to_process):
    dataframe = pd.read_csv(file_to_process)
    return dataframe

# Extract data from JSON
def extract_from_json(file_to_process):
    dataframe = pd.read_json(file_to_process, lines=True)
    return dataframe

# Extract data from XML
def extract_from_xml(file_to_process): 
    dataframe = pd.DataFrame(columns=["car_model", "year_of_manufacture", "price", "fuel"]) 
    tree = ET.parse(file_to_process)    # Open XML file
    root = tree.getroot()               # Based on format of file tree
    
    # Loop goes through relevant header and accesses data
    for row in root: 
        car_model = row.find("car_model").text 
        year_of_manufacture = row.find("year_of_manufacture").text
        price = float(row.find("price").text) 
        fuel = row.find("fuel").text 
        dataframe = pd.concat([dataframe, pd.DataFrame([{"car_model":car_model, "year_of_manufacture":year_of_manufacture, "price":price, "fuel":fuel}])], ignore_index=True) 
    
    return dataframe     

# Extracts data based on file type
def extract(): 
    extracted_data = pd.DataFrame(columns=['car_model','year_of_manufacture','price','fuel']) # create an empty data frame to hold extracted data 
     
    # process all csv files 
    for csvfile in glob.glob("*.csv"): 
        extracted_data = pd.concat([extracted_data, pd.DataFrame(extract_from_csv(csvfile))], ignore_index=True) 
         
    # process all json files 
    for jsonfile in glob.glob("*.json"): 
        extracted_data = pd.concat([extracted_data, pd.DataFrame(extract_from_json(jsonfile))], ignore_index=True) 
     
    # process all xml files 
    for xmlfile in glob.glob("*.xml"): 
        extracted_data = pd.concat([extracted_data, pd.DataFrame(extract_from_xml(xmlfile))], ignore_index=True) 
         
    return extracted_data 

# Data Transformation
def transform(data): 
    '''Round price values to 2 decimal places'''
    data['price'] = round(data.price,2) 
    return data 

# Loading extracted data into CSV
def load_data(target_file, transformed_data): 
    transformed_data.to_csv(target_file) 

# Logging operations
def log_progress(message): 
    timestamp_format = '%Y-%h-%d-%H:%M:%S' # Year-Monthname-Day-Hour-Minute-Second 
    now = datetime.now() # get current timestamp 
    timestamp = now.strftime(timestamp_format) 
    with open(log_file,"a") as f: 
        f.write(timestamp + ',' + message + '\n') 


# ************ Main program ************


# Log the initialization of the ETL process 
log_progress("ETL Job Started") 
 
# Log the beginning of the Extraction process 
log_progress("Extract phase Started") 
extracted_data = extract() 
 
# Log the completion of the Extraction process 
log_progress("Extract phase Ended") 
 
# Log the beginning of the Transformation process 
log_progress("Transform phase Started") 
transformed_data = transform(extracted_data) 
print("Transformed Data") 
print(transformed_data) 
 
# Log the completion of the Transformation process 
log_progress("Transform phase Ended") 
 
# Log the beginning of the Loading process 
log_progress("Load phase Started") 
load_data(target_file,transformed_data) 
 
# Log the completion of the Loading process 
log_progress("Load phase Ended") 
 
# Log the completion of the ETL process 
log_progress("ETL Job Ended") 