#!/usr/bin/env python

# Modules
import datetime
from pprint import pprint
from ncclient import manager
import xmltodict
import json

# Local modules
from bin.inventory import get_inventory

# Vars
path_inventory_str = "./inventory"

# Body
if __name__ == "__main__":
    ## Get inventory data
    inventory_dict = get_inventory(path_str=path_inventory_str)
    
    ## Collect data
    for hostname_str, hostvar_dict in inventory_dict.items():
        ## Get inital timestamp
        t1 = datetime.datetime.now()
        
        ## Get driver
        device_params_dict = {"name": hostvar_dict["nos"] if hostvar_dict["nos"] == "iosxr" else "default"}

        ## Connect to device
        with manager.connect(host=hostvar_dict["ip_address"], username=hostvar_dict["username"],
                             password=hostvar_dict["password"], device_params=device_params_dict) as device_obj:
            filter_str = "<filter type=\"subtree\"><interfaces xmlns=\"http://openconfig.net/yang/interfaces\"/></filter>"
            r1_str = str(device_obj.get(filter=filter_str))

            print("Interfaces operational data including ARP:\n")
            print(json.dumps(xmltodict.parse(r1_str), indent=4))

        ## Get final timestamp
        t2 = datetime.datetime.now()

        ## Print time
        print("=" * 84)
        print("Completed in",  str(t2 - t1), "for", hostname_str)
        print("=" * 84)