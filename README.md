# Query Dell Enterprise SONiC Devices for Basic Info

[![Contributions welcome](https://img.shields.io/badge/contributions-welcome-orange.svg)](#-how-to-contribute)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](https://github.com/benjamingoldstone/query_DES_basic_info/blob/main/LICENSE.md)
[![GitHub issues](https://img.shields.io/github/issues/benjamingoldstone/query_DES_basic_info)](https://github.com/benjamingoldstone/query_DES_basic_info/issues)

Built and maintained by [Ben Goldstone](https://github.com/benjamingoldstone/) and [Contributors](https://github.com/benjamingoldstone/query_DES_basic_info/graphs/contributors)

------------------

## Contents

- [Description and Objective](#-description-and-objective)
- [Requirements](#-requirements)
- [How to Contribute](#-how-to-contribute)

## Description and Objective

This is a basic script for querying a list of Dell Enterprise SONiC devices for basic info such as software version and system uptime. It currently will render such info for all devices into a spreadsheet in .csv format.

## Requirements

Python3 is required to run the script - it has been tested on Windows and Linux with Python3 version 3.11.

Install requirements via the standard `python -m pip install -r requirements.txt`. It's recommended that you use a virtual environment.

Set up a `devices.json` file by copying the example file to `devices.json` and filling out the relevant parameters. Note that you can of course change the name of each device, in the example file 'leaf1' and 'leaf2' are just examples.

Note that the code is currently set up to write a CSV file to the local directory and will by default overwrite an existing file with the same name.

## How to Contribute

Suggestions and contributions welcome, please reference the [CONTRIBUTING](https://github.com/benjamingoldstone/query_DES_basic_info/blob/main/CONTRIBUTING.md) guide.