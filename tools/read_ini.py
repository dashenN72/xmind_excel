# -*- coding: utf-8 -*-
# @Time    : 2020/2/4 0:44
# @Author  : dashenN72
import configparser


class ReadIni:
    def __init__(self, file_path=None):
        if file_path is None:
            self.file_path = "G:/Autointerface/db_config.ini"
        else:
            self.file_path = file_path

    def read_ini(self):
        conf = configparser.ConfigParser()
        conf.read(self.file_path)
        return conf

    def get_value_of_conf(self, key, section=None):
        if section is None:
            section = "api_test"
        result = self.read_ini().get(section, key)
        return result


if __name__ == "__main__":
    read_ini = ReadIni()
    print(read_ini.get_value_of_conf("host"))