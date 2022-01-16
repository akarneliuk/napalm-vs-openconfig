#!/usr/bin/env python

# Modules
import napalm
import datetime
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
        driver_obj = napalm.get_network_driver(name=hostvar_dict["nos"])
        
        ## Connect to device
        with driver_obj(hostname=hostvar_dict["ip_address"], username=hostvar_dict["username"],
                        password=hostvar_dict["password"]) as device_obj:
            print("Interfaces configuration:\n")
            print(json.dumps(device_obj.get_interfaces(), indent=4))

            print("\n\nARP table:")
            print(json.dumps(device_obj.get_arp_table(), indent=4))

        ## Get final timestamp
        t2 = datetime.datetime.now()

        ## Print time
        print("=" * 84)
        print("For device",  hostname_str,  "spent",  str(t2 - t1))
        print("=" * 84)