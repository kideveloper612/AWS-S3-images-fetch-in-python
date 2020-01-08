import os
import shutil
import requests
import csv

basedir = r"F:\working\python\scrapping\new\\"
def get_file_key(filename):
    print(filename)
    file, extension = os.path.splitext(filename)
    filename_array = file.split('-')
    if len(filename_array) > 1:
        return filename_array[1], extension
    else:
        return filename_array[0], extension

def get_files_in_folder(folder):
    for root, dirs, files in os.walk(folder):
        for file in files:
            path_array = root.split('\\')
            file_key, file_extension = get_file_key(file)
            file_name = "%s_%s_%s_%s%s" % (path_array[2], path_array[3], path_array[4], file_key, file_extension )
            new_path = os.path.join(basedir, file_name)
            print(file_name)

            if not os.path.exists(basedir):
                print("Not found")
                continue  # Next filename

            elif not os.path.exists(new_path):  # folder exists, file does not
                shutil.copy(os.path.join(root, file), new_path)

# get_files_in_folder("..\download")

def vin_decode(vin):
    headers = {
        "content-type": "application/json",
        "authorization": "Basic MzQ3NDc3NzMtOTg5Zi00YzczLWJmODItMTQxMTY5OGQ2Yjlk",
        "partner-token": "e4fec6eea8cf4922adaa4d4f6d717dda"
    }

    URL = "http://api.carmd.com/v3.0/decode?vin=%s" % vin
    res = requests.get(url=URL, headers=headers).json()
    print(res)
    return res

source_folder = "../Make_Model_VIN_Key"
# source_folder = "../vpic"
def rename_file(directory):
    for root, dirs, files in os.walk(directory):
        for file in files:
            print(file)
            if len(file.split("_")) > 4:
                continue
            vin = file.split("_")[2]
            vin_res = vin_decode(vin=vin)
            if vin_res['data'] is not None:
                year = vin_res['data']['year']
                filename_array = file.split("_")
                new_name = "%s_%s_%s_%s_%s" % (filename_array[0], filename_array[1], year, filename_array[2], filename_array[3])
                print(new_name)
                os.rename(os.path.join(root, file), os.path.join(source_folder, new_name))

# rename_file(source_folder)

#get year from local file
def get_year(vin):
    vin_array = []
    year_array = []
    file_path = "vehicle_images.csv"
    with open(file_path) as f:
        reader = csv.reader(f)
        for row in reader:
            vin_array.append(row[0])
            year_array.append(row[5])
    if (vin in vin_array):
        index = vin_array.index(vin)
        return year_array[index]

def get_year_vpic(vin):
    URL = "https://vpic.nhtsa.dot.gov/api/vehicles/DecodeVinValuesExtended/%s?format=json" % vin
    res = requests.get(url=URL).json()
    return res['Results'][0]['ModelYear']

def rename_file_csv(directory):
    for root, dirs, files in os.walk(directory):
        for file in files:
            print(file)
            if len(file.split("_")) > 4:
                continue
            vin = file.split("_")[2]
            year = get_year_vpic(vin=vin)
            if year:
                filename_array = file.split("_")
                new_name = "%s_%s_%s_%s_%s" % (filename_array[0], filename_array[1], year, filename_array[2], filename_array[3])
                print(new_name)
                os.rename(os.path.join(root, file), os.path.join(source_folder, new_name))
# rename_file_csv(source_folder)

def file_review(directory):
    count = 0
    for root, dirs, files in os.walk(directory):
        for file in files:
            print(file)
            if len(file.split("_")) > 4:
                count += 1
    print(count)

file_review(source_folder)

