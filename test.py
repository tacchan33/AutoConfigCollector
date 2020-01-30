# -*- coding:utf-8 -*-

import csv
import paramiko
import time
import concurrent.futures

def main():

    hosts = getHosts('./hosts.csv')
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        executor = executor.map(getResult, hosts['hostname'], hosts['ssh_username'], hosts['ssh_password'], hosts['enable_password'],)

def getHosts(path='./hosts.csv'):
    hosts = { 'hostname':[] , 'ssh_username':[] , 'ssh_password':[] , 'enable_password':[] , }
    with open(path, newline='') as data:
        csvData = csv.reader(data)
        for row in csvData:
            hosts['hostname'].append(row[0])
            hosts['ssh_username'].append(row[1])
            hosts['ssh_password'].append(row[2])
            hosts['enable_password'].append(row[3])
    return hosts
            

def getResult(hostname="Router", ssh_username="admin", ssh_password="password", enable_password="enable"):
    print(hostname+"開始")

    ssh_client = paramiko.SSHClient()
    ssh_client.load_system_host_keys()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        ssh_client.connect(hostname, username=ssh_username, password=ssh_password, timeout=15.0, look_for_keys=False, allow_agent=False)
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
        #print(ssh_connection.recv(65535).decode('utf-8'))
        ssh_connection.recv(65535).decode('utf-8')
        ssh_connection.send('show running-config\n')
        time.sleep(10)

        result = ssh_connection.recv(65535).decode('utf-8')

        try:
            file = open("./config/"+hostname+".log","w")
            file.write(result)
            print("["+hostname+"] Getting config complete!")
        except Exception as e:
            print("["+hostname+"] Getting config failed")
            print(e)
        finally:
            file.close()

    except Exception as e:
        
        print(e)
        print(hostname + 'ssh error')

    finally:
        ssh_client.close()

if __name__ == "__main__":
    start = time.time()
    main()
    elapsed_time = time.time() - start
    print("かかった時間は"+format(elapsed_time)+"[sec]")
