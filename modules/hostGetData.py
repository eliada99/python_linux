#!/usr/bin/python
import json

JSON_FILE = "json_file.json"


def get_versions_from_json():
    with open(JSON_FILE) as f:
        json_file = json.load(f)
        f.close()
    dic_versions = {"bfbImage": json_file["update_setup"]["versions"]["BFB"],
                    "driver": json_file["update_setup"]["versions"]["ofed_install_command"],
                    "fw": json_file["update_setup"]["versions"]["FW"]}

    return dic_versions
