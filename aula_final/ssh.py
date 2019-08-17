import paramiko

client = paramiko.client.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

client.connect('172.17.0.3', username='root', key_filename='/home/developer/.ssh/id_rsa')

stdin, stdout, stderr = client.exec_command('apt-get install -y htop sl')

for l in stdout:
	print(l.strip())

sftp = client.open_sftp()
sftp.put('ssh.py', 'lucas-sales-force.py')