# -*- coding:utf-8 -*-

import paramiko
import time

host_name = ''
host_ipaddr = ''
ssh_username = ''
ssh_password = ''
enable_password = ''

ftp_hostname = ''
ftp_dirpath = ''
ftp_username = ''
ftp_password = ''

client = paramiko.SSHClient()
client.load_system_host_keys()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

try:
    client.connect(host_ipaddr, username=ssh_username, password=ssh_password, look_for_keys=False, allow_agent=False)
    ssh_con = client.invoke_shell()
    time.sleep(2)

    result = ssh_con.recv(65535).decode('utf-8') #ログイン後の出力メッセージ受け取り
    print(result)
    if host_name in result: #ホスト名が一致しているか確認
        ssh_con.send('enable\n')
        time.sleep(1)
        ssh_con.send(enable_password + '\n')
        time.sleep(1)
        ssh_con.send('terminal length 0\n')
        time.sleep(1)
        print(ssh_con.recv(65535).decode('utf-8'))
        ssh_con.send('copy running-config startup-config\n')
        time.sleep(1)
        ssh_con.send('\n')
        time.sleep(1)
        print(ssh_con.recv(65535).decode('utf-8'))
        ssh_con.send('copy running-config ftp://' + ftp_username + ':' + ftp_password + '@' + ftp_hostname + ftp_dirpath + '\n')
        time.sleep(1)
        ssh_con.send('\n')
        time.sleep(1)
        ssh_con.send('\n')
        time.sleep(1)
        print(ssh_con.recv(65535).decode('utf-8'))
        ssh_con.send('show running-config\n')
        time.sleep(1)
        print(ssh_con.recv(65535).decode('utf-8'))

    else:
        print('NG')

except Exception as e:
    
    print(e)
    print(host_ipaddr + 'ssh error')

finally:
    client.close()
