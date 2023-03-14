import os
import json
class GoogleMapsApiValue:

    def __init__(self) -> None:
        self.path = os.getcwd()
        with open("parameters.json", 'r') as open_file:
            try:
                file_data = json.load(open_file)
            except:
                open_file.seek(0)
                print(f'Error reading file "parameters.json", Check if the file is persent and readible.')
        self.gm_api_txt_file_name = file_data["GM_API_KEY_TXT_FILE"]
        self.api_keys_filename = file_data["API_KEYS_JSON"]
        self.gm_api_json_key = file_data["API_KEYS_JSON_GM_KEY"]
        self.gm_api_value = file_data["GM_API_VALUE"]
        self.api_storage_files = [self.gm_api_txt_file_name,self.api_keys_filename]

    def check_gm_api_key_files_exist(self) -> list:
        file_names = self.api_storage_files
        file_names_exists = []
        for file_name in file_names:
            if file_name in os.listdir(self.path):
                file_names_exists.append(True)
            else:
                file_names_exists.append(False)
        return file_names_exists
    
    def get_gm_api_key_files_exist_dic(self) -> dict:
        obj = GoogleMapsApiValue()
        files_exist_list = obj.check_gm_api_key_files_exist()
        files_exist_dict = dict(zip(self.api_storage_files,files_exist_list))
        return files_exist_dict
    
    def check_api_storage_files_exist(self) -> bool:
        obj = GoogleMapsApiValue()
        files_exist_dict = obj.get_gm_api_key_files_exist_dic()
        if all(value == False for value in files_exist_dict.values()):
            return False
        else:
            return True
        
    def use_api_keys_json(self) -> bool:
        obj = GoogleMapsApiValue()
        files_exist_dict = obj.get_gm_api_key_files_exist_dic()
        api_keys_filename = obj.api_keys_filename
        if files_exist_dict[api_keys_filename]:
            return True
        else:
            return False
    def get_gm_api_key_from_gm_api_txt(self) -> str:
        obj = GoogleMapsApiValue()
        with open(self.gm_api_txt_file_name,'r') as open_file:
            try:
                file_data = open_file.readline()
            except:
                open_file.seek(0)
                print(f"Error reading file {self.api_keys_filename}, Check if the file is persent and readible.")
            self.gm_api_value = file_data
            return self.gm_api_value
    
    def get_gm_api_key_from_api_key(self) -> str:
        obj = GoogleMapsApiValue()
        api_keys_file_exists = obj.use_api_keys_json()
        if api_keys_file_exists:
            with open(self.api_keys_filename,'r') as open_file:
                try:
                    file_data=json.load(open_file)
                except:
                    open_file.seek(0)
                    print(f"Error reading file {self.api_keys_filename}, Check if the file is persent and readible.")
            self.gm_api_value = file_data[self.gm_api_json_key]
            return self.gm_api_value
        else:
            return obj.get_gm_api_key_from_gm_api_txt()
        
    def print_gm_api_key(self) -> None:
        obj = GoogleMapsApiValue()
        gm_api_key = obj.get_gm_api_key_from_api_key()
        if len(gm_api_key) > 10:
            print(f'The googlemaps API Key is valid, Key:"{gm_api_key}"')
        else:
            print(f'Invalid Key!, Key:"{gm_api_key}"')
    
    def get_gm_api_key(self) -> str:
        obj = GoogleMapsApiValue()
        gm_api_key = obj.get_gm_api_key_from_api_key()
        return gm_api_key



    
