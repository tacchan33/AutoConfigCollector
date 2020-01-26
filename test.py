# -*- coding:utf-8 -*-

import paramiko
import time

hostname = ''
ssh_username = ''
ssh_password = ''
enable_password = ''

client = paramiko.SSHClient()
client.load_system_host_keys()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

try:
    client.connect(hostname, username=ssh_username, password=ssh_password, look_for_keys=False, allow_agent=False)
    ssh_connection = client.invoke_shell()
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
    time.sleep(1)
    print(ssh_connection.recv(65535).decode('utf-8'))
    ssh_connection.send('show running-config\n')
    time.sleep(1)

    try:
        file = open("./"+hostname+".log","w")
        file.write(ssh_connection.recv(65535).decode('utf-8'))
        print("Getting config complete!")
    except Exception as fe:
        print("Getting config failed")
        print(fe)

except Exception as e:
    
    print(e)
    print(hostname + 'ssh error')

finally:
    client.close()
