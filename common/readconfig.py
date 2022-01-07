# -*- coding: utf-8 -*
import configparser
import json
import os


class ReadConfig:
    def __init__(self, config_name='config'):
        project_name = 'pyCache'

        temp_dir = os.path.dirname(os.path.abspath('.'))
        # s1 = temp_dir.index(project_name)
        # self.root_dir = temp_dir[0:s1] + project_name + '/'
        self.root_dir = temp_dir + '/' + project_name + '/'

        config_path = os.path.join(self.root_dir, "common/" + config_name + ".ini")

        self.cf = configparser.ConfigParser()
        self.cf.read(config_path)

    def get_config(self, data_class, param):
        value = self.cf.get(data_class, param)
        return value

    def read_json_file(self, file_path):
        rule_path = os.path.join(self.root_dir, "common/" + file_path)

        with open(rule_path, 'r', encoding='UTF-8') as load_f:
            load_dict = json.load(load_f)

            return load_dict


if __name__ == '__main__':
    pass

