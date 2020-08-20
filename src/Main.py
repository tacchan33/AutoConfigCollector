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
        self.__hosts = self.__readHostsFile(path=self.__configuration['HostsList'], columnNumber=self.__configuration['HostsList_ColumnNumber'])
        with concurrent.futures.ThreadPoolExecutor(max_workers=500) as executor:
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
            try:
                cmd = SSHCommandPattern2(hostname=hostname, username=username, password=password, errorlogPath=self.__configuration['ErrorLog'])
                del cmd
            except Exception as e:
                print(e)
        elif config_type == "3":
            try:
                cmd = SSHCommandPattern3(hostname=hostname, username=username, password=password, errorlogPath=self.__configuration['ErrorLog'])
                del cmd
            except Exception as e:
                print(e)
        elif config_type == "4":
            try:
                cmd = SSHCommandPattern4(hostname=hostname, username=username, password=password, errorlogPath=self.__configuration['ErrorLog'])
                del cmd
            except Exception as e:
                print(e)
        elif config_type == "5":
            cmd = SSHCommandPattern5(hostname=hostname, username=username, password=password, errorlogPath=self.__configuration['ErrorLog'])
            del cmd
        elif config_type == "6":
            cmd = SSHCommandPattern6(hostname=hostname, username=username, password=password, errorlogPath=self.__configuration['ErrorLog'])
            del cmd
        else:
            print("["+hostname+"] SSHCommandPattern no found")


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

    def __readHostsFile(self, path='./hosts.csv', columnNumber=0):
        try:
            hosts = { 'hostname':[] , 'command_type':[] , 'ssh_username':[] , 'ssh_password':[] }
            with open(path, newline='') as hostsFile:
                csvData = csv.reader(hostsFile, delimiter=',', quotechar='"')
                next(csvData) #First line skipped
                for row in csvData:
                    if '#' not in row[0]: # comments line skipped
                        hosts['hostname'].append(row[columnNumber['FQDN']])
                        hosts['command_type'].append(row[columnNumber['config_template']])
                        hosts['ssh_username'].append(row[columnNumber['username']])
                        hosts['ssh_password'].append(row[columnNumber['password']])
            return hosts
        except Exception as e:
            print('Loading Failed...')
            print(e)
            sys.exit(1)
