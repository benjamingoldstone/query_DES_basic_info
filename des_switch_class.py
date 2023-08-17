import logging
import sys

import requests
import json

requests.packages.urllib3.disable_warnings()


class DellEnterpriseSONiCSwitch:

    def __init__(self, switch_ip, username, password, description, firmware_ver):
        self.switch_ip = switch_ip
        self.username = username
        self.password = password
        self.description = description
        self.hostname = ""
        self.asic_version = ""
        self.build_commit = ""
        self.build_date = ""
        self.built_by = ""
        self.config_db_version = ""
        self.hwsku_version = ""
        self.kernel_version = ""
        self.platform_name = ""
        self.product_description = ""
        self.serial_number = ""
        self.software_version = ""
        self.firmware_version = firmware_ver
        self.uptime = ""
        self.datetime = ""
        self.dns = ""
        self.service_tag = ""
        self.mgmt_mac_addr = ""
        if self.validate_firmware_version() == "3.5.1":
            self.get_switch_system_components351()
        elif self.validate_firmware_version() == "4.1.1":
            self.get_switch_system_components411()
        else:
            logging.error(f"Firmware Version not Specified correctly in devices.json file for {self.description}"
                          f", skipping.")
            # sys.exit()

    def __iter__(self):  # TODO: This is hacky, clean this up
        return iter([self.description,
                     self.switch_ip,
                     self.hostname,
                     self.asic_version,
                     self.build_commit,
                     self.build_date,
                     self.built_by,
                     self.config_db_version,
                     self.hwsku_version,
                     self.kernel_version,
                     self.platform_name,
                     self.product_description,
                     self.serial_number,
                     self.software_version,
                     self.uptime,
                     self.datetime,
                     self.dns,
                     self.service_tag,
                     self.mgmt_mac_addr
                     ])

    def validate_firmware_version(self):
        """

        :return:
        """
        supported_firmware_versions = ["3.5.1", "4.1.1"]
        print(f"Firmware version declared is: {self.firmware_version}")
        if self.firmware_version is None:
            logging.error("Firmware version not specified in devices.json file, exiting.")
            sys.exit()
        elif self.firmware_version not in supported_firmware_versions:
            logging.error(f"Firmware version specified in devices.json file for {self.description} not one of "
                          f"{supported_firmware_versions}, exiting.")
            sys.exit()
        else:
            return self.firmware_version

    def get_switch_system_components411(self):
        """
        Get all system components from switch via API call, render into switch variables
        :param self: object
        :return: none
        """
        try:
            logging.info(f"Querying switch {self.description} for info via API")
            url = f"https://{self.switch_ip}/restconf/data/openconfig-platform:components"
            headers = {}
            response = requests.request("GET", url, auth=(self.username, self.password), headers=headers, verify=False)
            switch_info = response.text
            switch_info_dict = json.loads(switch_info)

            l1 = switch_info_dict.get("openconfig-platform:components")
            l2 = l1.get("component")[58]
            l25 = l2.get("software-module")
            l3 = l25.get("state")
            self.hostname = self.get_hostname()
            self.asic_version = l3.get("openconfig-platform-software-ext:asic-version")
            self.build_commit = l3.get("openconfig-platform-software-ext:build-commit").replace("'", "")
            self.build_date = l3.get("openconfig-platform-software-ext:build-date")
            self.built_by = l3.get("openconfig-platform-software-ext:built-by")
            self.config_db_version = l3.get("openconfig-platform-software-ext:config-db-version")
            self.hwsku_version = l3.get("openconfig-platform-software-ext:hwsku-version")
            self.kernel_version = l3.get("openconfig-platform-software-ext:kernel-version").replace("'", "")
            self.platform_name = l3.get("openconfig-platform-software-ext:platform-name")
            self.product_description = l3.get("openconfig-platform-software-ext:product-description")
            self.serial_number = l3.get("openconfig-platform-software-ext:serial-number")  # TODO: this doesn't exist, fix
            self.software_version = l3.get("openconfig-platform-software-ext:software-version").replace("'", "")
            self.uptime = l3.get("openconfig-platform-software-ext:up-time")
            self.datetime = self.get_datetime()
            self.dns = self.get_dns()

        except requests.ConnectionError as e:
            print(e)

    def get_switch_system_components351(self):
        """
        Get all system components from switch via API call, render into switch variables
        :param self: object
        :return: none
        """
        try:
            logging.info(f"Querying switch {self.description} for info via API")
            url = f"https://{self.switch_ip}/restconf/data/openconfig-platform:components"
            headers = {}
            response = requests.request("GET", url, auth=(self.username, self.password), headers=headers, verify=False)
            switch_info = response.text
            switch_info_dict = json.loads(switch_info)

            l1 = switch_info_dict.get("openconfig-platform:components")
            l2 = l1.get("component")[58]
            l3 = l2.get("openconfig-platform-ext:software")
            self.hostname = self.get_hostname()
            self.asic_version = l3.get("asic-version")
            self.build_commit = l3.get("build-commit").replace("'", "")
            self.build_date = l3.get("build-date")
            self.built_by = l3.get("built-by")
            self.config_db_version = l3.get("config-db-version")
            self.hwsku_version = l3.get("hwsku-version")
            self.kernel_version = l3.get("kernel-version").replace("'", "")
            self.platform_name = l3.get("platform-name")
            self.product_description = l3.get("product-description")
            self.serial_number = l3.get("serial-number")
            self.software_version = l3.get("software-version").replace("'", "")
            self.uptime = l3.get("up-time")
            self.datetime = self.get_datetime()
            self.dns = self.get_dns()

        except requests.ConnectionError as e:
            print(e)

    def get_hostname(self):

        try:
            url = f"https://{self.switch_ip}/restconf/data/openconfig-system:system/config/hostname"
            headers = {}
            response = requests.request("GET", url, auth=(self.username, self.password), headers=headers, verify=False)
            switch_hostname_text = response.text
            switch_hostname_dict = json.loads(switch_hostname_text)
            return switch_hostname_dict.get("openconfig-system:hostname")
        except requests.ConnectionError as e:
            print(e)

    def get_datetime(self):

        try:
            url = f"https://{self.switch_ip}/restconf/data/openconfig-system:system/state/current-datetime"
            headers = {}
            response = requests.request("GET", url, auth=(self.username, self.password), headers=headers, verify=False)
            switch_info_text = response.text
            switch_info_dict = json.loads(switch_info_text)
            return switch_info_dict.get("openconfig-system:current-datetime")
        except requests.ConnectionError as e:
            print(e)

    def get_dns(self):

        try:
            url = f"https://{self.switch_ip}/restconf/data/openconfig-system:system/dns/servers"
            headers = {}
            response = requests.request("GET", url, auth=(self.username, self.password), headers=headers, verify=False)
            switch_info_text = response.text
            switch_info_dict = json.loads(switch_info_text)
            return switch_info_dict  # .get("openconfig-system:current-datetime")  # TODO: Fix this
        except requests.ConnectionError as e:
            print(e)
