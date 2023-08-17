# Collect info about a collection of Dell Enterprise SONiC Switches
# List of devices exists in the file devices.json - copy devices.json.example to devices.json

import json
import csv
import os
import logging
import sys

from des_switch_class import DellEnterpriseSONiCSwitch


def print_all_system_components(switch):
    print(f"###### {switch.description} ######")
    print(f"Hostname: {switch.hostname}")
    print(f"ASIC version: {switch.asic_version}")
    print(f"Build commit: {switch.build_commit}")
    print(f"Build date: {switch.build_date}")
    print(f"Built by: {switch.built_by}")
    print(f"Config DB Version: {switch.config_db_version}")
    print(f"HWSKU Version: {switch.hwsku_version}")
    print(f"Kernel Version: {switch.kernel_version}")
    print(f"Platform Name: {switch.platform_name}")
    print(f"Product Description: {switch.product_description}")
    print(f"Serial Number: {switch.serial_number}")
    print(f"Software Version: {switch.software_version}")
    print(f"Device Uptime: {switch.uptime}")
    print(f"Datetime: {switch.datetime}")
    print(f"System DNS: {switch.dns}")
    print("")


def read_info_json_file(filename):
    try:
        with open(filename, "r") as jsonfile:
            config_file = json.load(jsonfile)
            logging.info(f"Import of JSON formatted device config file '{filename}' was successful.")
        return config_file
    except Exception as e:  # TODO: obviously way to broad, clean this up
        logging.error(e)
        sys.exit()


def create_switch_objects(config):
    logging.info("Creating list of switch objects from device configuration.")
    list_of_switch_objects = []
    for _ in config.keys():
        parameters = config.get(_)
        switch_ip = parameters.get("switch_ip")
        username = parameters.get("username")
        password = parameters.get("password")
        description = parameters.get("description")
        firmware_version = parameters.get("firmware_ver")
        switch = DellEnterpriseSONiCSwitch(switch_ip, username, password, description, firmware_version)
        list_of_switch_objects.append(switch)
    return list_of_switch_objects


def write_csv_file(filename, switch_objects):
    logging.info("Writing switch info to CSV file.")
    with open(filename, 'w', encoding='UTF8', newline='') as f:
        writer = csv.writer(f)

        header = ["Description", "IP Address", "Hostname", "ASIC Version", "Build commit", "Build date", "Built by",
                  "Config DB Version", "HWSKU Version", "Kernel Version", "Platform Name", "Product Description",
                  "Serial Number", "Software Version", "Device Uptime", "Datetime", "System DNS"]  \
            # TODO: move this out, is not DRY

        writer.writerow(header)
        for i in range(len(switch_objects)):
            writer.writerow(switch_objects[i])


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    logging.info("Starting new run.")
    switch_config = read_info_json_file("devices.json")
    switches = create_switch_objects(switch_config)
    write_csv_file("switches_info.csv", switches)
    os.startfile("switches_info.csv")
