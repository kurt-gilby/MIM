import tkinter as tk
import googlemaps as gm
import os
import json
from googlemaps.exceptions import ApiError

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
    

def get_location_suggestions(params):
    query = params[1].get()
    gmaps = gm.Client(key=params[0])    
    try:
        results = gmaps.places_autocomplete(query)
        suggestions = [result['description'] for result in results]
        params[2].delete(0,tk.END)
        for suggestion in suggestions:
            params[2].insert(tk.END, suggestion)
    except ApiError as e:
        print(f'Error: {e}')





def on_entry_change(event,params):
    get_location_suggestions(params)


def load_application(title,width,height,googlemaps_api_key):
    app = tk.Tk()
    app.title(title)
    app.geometry(f"{width}x{height}")
    location_label = tk.Label(app, text="Enter location:")
    location_label.pack(anchor=tk.W)
    location_entry = tk.Entry(app, width=50)
    location_entry.pack(anchor=tk.W)
    
    location_entry_params = []
    location_entry_params.append(googlemaps_api_key)
    location_entry_params.append(location_entry)
    

    suggestion_label = tk.Label(app, text="Pick a Location:")
    suggestion_label.pack(anchor=tk.W)
    suggestion_box = tk.Listbox(app, width=50)
    suggestion_box.pack(anchor=tk.W)

    location_entry_params.append(suggestion_box)

    location_entry.bind("<KeyRelease>", lambda event, params = location_entry_params: on_entry_change(event,params))
    app.mainloop()



    
def main():
    CWD = os.getcwd()
    
    GM_API_KEY_TXT_FILE = "google_map_api_key.txt"
    API_KEYS_JSON = "api_keys.json"
    API_STORAGE_FILES = [GM_API_KEY_TXT_FILE,API_KEYS_JSON]
    API_KEYS_JSON_GM_KEY ="googlemaps"
    GM_API_VALUE = "MY_GM_API_VALUE"
    APP_TITLE = "Meet in the Middle"
    APP_WIDTH = 800
    APP_WIDTH = 800
    
    does_file_exist_list = check_files_exist(CWD,API_STORAGE_FILES)
    does_file_exist_dict = create_dict_from_list(API_STORAGE_FILES,does_file_exist_list)
    does_api_storage_files_exist = check_api_storage_files_exist(does_file_exist_dict)
    should_use_jason_api_key_file = use_api_storage_file(does_file_exist_dict, API_KEYS_JSON)
    use_gm_api_text_file = use_api_storage_file(does_file_exist_dict, GM_API_KEY_TXT_FILE)
    GM_API_VALUE = get_google_maps_api_value(does_api_storage_files_exist,should_use_jason_api_key_file,use_gm_api_text_file,CWD,API_KEYS_JSON,API_KEYS_JSON_GM_KEY,GM_API_KEY_TXT_FILE,API_STORAGE_FILES)

    load_application(APP_TITLE,APP_WIDTH,APP_WIDTH,GM_API_VALUE)

    
if __name__ == "__main__":
    main()





