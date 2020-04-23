# -*- coding:utf-8 -*-

import csv
import concurrent.futures
import yaml
import sys
from SSHCommand import *

class Main:
    def __init__(self):
        self.__configuration = ''
        self.__hosts = ''

    def run(self):
        self.__configuration = self.__readConfigurationFile()
        self.__initializeErrorFile(path=self.__configuration['ErrorLog'])
        self.__hosts = self.__readHostsFile(path=self.__configuration['HostsList'])
        with concurrent.futures.ThreadPoolExecutor(max_workers=60) as executor:
            executor = executor.map(self.__getResult,self.__hosts['command_type'], self.__hosts['hostname'], self.__hosts['ssh_username'], self.__hosts['ssh_password'])

    def __del__(self):
        pass

    def __getResult(self, config_type='0', hostname='switch', username='username', password='password'):
        if config_type == "1":
            try:
                cmd = SSHCommandPattern1(hostname=hostname, username=username, password=password, errorlogPath=self.__configuration['ErrorLog'])
                del cmd
            except Exception as e:
                print(e)
        elif config_type == "2":
            cmd = SSHCommandPattern2(hostname=hostname, username=username, password=password, errorlogPath=self.__configuration['ErrorLog'])
            del cmd


    def __initializeErrorFile(self, path):
        try:
            with open(path,'w') as file:
                file.write('')
        except Exception as e:
            print('Error.log Initialize Failed...')
            print(e)
            sys.exit(1)

    def __readConfigurationFile(self, path='/root/ConfigurationCollector/conf/ConfigurationCollector.yaml'):
        try:
            with open(path) as file:
                configuration = yaml.safe_load(file)
            return configuration
        except Exception as e:
            print('ConfigurationCollector.yaml Loading Failed...')
            print(e)
            sys.exit(1)

    def __readHostsFile(self, path='./hosts.csv'):
        try:
            hosts = { 'hostname':[] , 'command_type':[] , 'ssh_username':[] , 'ssh_password':[] }
            with open(path, newline='') as hostsFile:
                csvData = csv.reader(hostsFile, delimiter=',', quotechar='"')
                next(csvData) #First line skipped
                for row in csvData:
                    if '#' not in row[0]: # comments line skipped
                        hosts['hostname'].append(row[0])
                        hosts['command_type'].append(row[1])
                        hosts['ssh_username'].append(row[2])
                        hosts['ssh_password'].append(row[3])
            return hosts
        except Exception as e:
            print('Loading Failed...')
            print(e)
            sys.exit(1)
