# Modules
import yaml
import os

# Functions
def get_inventory(path_str: str) -> dict:
    result = {}
    try:
        files_list = os.listdir(path=path_str)

        for file_str in files_list:
            file_obj = open(file=f"{path_str}/{file_str}", mode="r")
            result.update({file_str.split(".")[0]: yaml.load(file_obj, Loader=yaml.FullLoader)})
        
    except FileNotFoundError as e:
        print(e)

    return result