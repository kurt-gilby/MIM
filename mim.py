import tkinter as tk
import googlemaps as gm
import os
import json

def check_file_exist(path, file_name):
    if file_name in os.listdir(path):
        return True
    else:
        return False

def check_files_exist(path,file_names):
    files_exist = []
    for file_name in file_names:
        files_exist.append(check_file_exist(path,file_name))
    return files_exist

def create_dict_from_list(key_list, value_list):
    new_dict = dict(zip(key_list,value_list))
    return new_dict

def check_api_storage_files_exist(file_exists_dict):
    if all(value == False for value in file_exists_dict.values()):
        return False
    else:
        return True
    
def use_api_storage_file(file_exists_dict,json_file_name):
    if file_exists_dict[json_file_name]:
        return True
    else:
        return False
    
def get_full_path(path,file_name):
    full_path = os.path.join(path,file_name)
    return full_path

def read_json_data(path,file_name):
    file = get_full_path(path,file_name)
    with open(file, 'r') as open_file:
        try:
            file_data = json.load(open_file)
        except:
            open_file.seek(0)
            print(f"Error reading file {file_name}, Check if the file is persent and readible.")    
    return file_data

def read_txt_data(path,file_name):
    file = get_full_path(path,file_name)    
    with open(file, 'r') as open_file:
        try:
            file_data = open_file.readline()
        except:
            open_file.seek(0)
            print(f"Error reading file {file_name}, Check if the file is persent and readible.")   
    return file_data

def print_google_maps_api_not_found(files_names):
    print(f'Google Maps API Key is needed and should be added to any of the following files:')
    for file_name in files_names:
        index = files_names.index(file_name)
        print(f"{index+1}. {file_name}")
    print('Please check the README for more information!')

def get_google_maps_api_value(storage_files_exist,use_json_api_key_file,use_gm_api_text_file,path,json_api_key_file,json_api_key,gm_api_text_file,files_List):
    if storage_files_exist:
        if use_json_api_key_file:
            json_data = read_json_data(path,json_api_key_file)
            for key, value in json_data.items():
                if key == json_api_key:
                    GM_API_VALUE = value
                    return GM_API_VALUE
        elif use_gm_api_text_file:
            txt_data = read_txt_data(path,gm_api_text_file)
            GM_API_VALUE = value
            return GM_API_VALUE
        else:
             print_google_maps_api_not_found(files_List)
             return "0"
    else:
        print_google_maps_api_not_found(files_List)
        return"0"


    
def main():
    CWD = os.getcwd()
    
    GM_API_KEY_TXT_FILE = "google_map_api_key.txt"
    API_KEYS_JSON = "api_keys.json"
    API_STORAGE_FILES = [GM_API_KEY_TXT_FILE,API_KEYS_JSON]
    API_KEYS_JSON_GM_KEY ="googlemaps"
    GM_API_VALUE = "MY_GM_API_VALUE"
    
    does_file_exist_list = check_files_exist(CWD,API_STORAGE_FILES)
    does_file_exist_dict = create_dict_from_list(API_STORAGE_FILES,does_file_exist_list)
    does_api_storage_files_exist = check_api_storage_files_exist(does_file_exist_dict)
    should_use_jason_api_key_file = use_api_storage_file(does_file_exist_dict, API_KEYS_JSON)
    use_gm_api_text_file = use_api_storage_file(does_file_exist_dict, GM_API_KEY_TXT_FILE)
    GM_API_VALUE = get_google_maps_api_value(does_api_storage_files_exist,should_use_jason_api_key_file,use_gm_api_text_file,CWD,API_KEYS_JSON,API_KEYS_JSON_GM_KEY,GM_API_KEY_TXT_FILE,API_STORAGE_FILES)
    


    
if __name__ == "__main__":
    main()





