# -*- coding:utf-8 -*-

import csv
import paramiko
import time

def main():
    with open('./hosts.csv', newline='') as hosts:
        csvReader = csv.reader(hosts)
        for row in csvReader:
            hostname = row[0]
            ssh_username = row[1]
            ssh_password = row[2]
            enable_password = row[3]
            result = getResult(hostname,ssh_username,ssh_password,enable_password)
            try:
                file = open("./"+hostname+".log","w")
                file.write(result)
                print("["+hostname+"] Getting config complete!")
            except Exception as e:
                    print("["+hostname+"] Getting config failed")
                    print(e)
            finally:
                file.close()

def getResult(hostname="Router", ssh_username="admin", ssh_password="password", enable_password="enable"):

    ssh_client = paramiko.SSHClient()
    ssh_client.load_system_host_keys()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        ssh_client.connect(hostname, username=ssh_username, password=ssh_password, look_for_keys=False, allow_agent=False)
        ssh_connection = ssh_client.invoke_shell()
        time.sleep(2)

        ssh_connection.send('enable\n')
        time.sleep(1)
        ssh_connection.send(enable_password + '\n')
        time.sleep(1)
        ssh_connection.send('terminal length 0\n')
        time.sleep(1)
        ssh_connection.send('copy running-config startup-config\n')
        time.sleep(1)
        ssh_connection.send('\n')
        time.sleep(2)
        print(ssh_connection.recv(65535).decode('utf-8'))
        ssh_connection.send('show running-config\n')
        time.sleep(1)
        
        return ssh_connection.recv(65535).decode('utf-8')

    except Exception as e:
        
        print(e)
        print(hostname + 'ssh error')

    finally:
        ssh_client.close()


if __name__ == "__main__":
    main()
