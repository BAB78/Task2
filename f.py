import telnetlib
import paramiko
import difflib
import os

# Define common variables
ip_address = '192.168.56.101'
username = 'cisco'
password = 'cisco123!'
enable_password = 'class123!'
ssh_username = 'cisco'
ssh_password = 'cisco123!'
output_file = 'running_config.txt'  # Name of the local file to save the configuration

# Telnet session using telnetlib
try:
    tn = telnetlib.Telnet(ip_address)
    tn.read_until(b'Username: ')
    tn.write(username.encode('utf-8') + b'\n')
    tn.read_until(b'Password: ')
    tn.write(password.encode('utf-8') + b'\n')

    # Add this line to read until you find the "Password" prompt
    tn.read_until(b'Password: ')
    
    print('Telnet Session:')
    print(f'Successfully connected to: {ip_address}')
    print(f'Username: {username}')

    # Send a command to output the running configuration
    tn.write(b'show running-config\n')

    # Read until you find some end pattern or timeout
    running_config_telnet = tn.read_until(b'end\r\n\r\n', timeout=10).decode('utf-8')

    # Save the Telnet running configuration to a local file
    with open(output_file, 'w') as file:
        file.write(running_config_telnet)

    print('Running configuration saved to', output_file)
    print('------------------------------------------------------')

    # Close Telnet session
    tn.write(b'quit\n')
    tn.close()
except Exception as e:
    print(f'Telnet Session Failed: {e}')

# SSH session using paramiko
try:
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(ip_address, username=ssh_username, password=ssh_password, look_for_keys=False, allow_agent=False)
    ssh_shell = ssh.invoke_shell()

    # Enter enable mode
    ssh_shell.send('enable\n')
    ssh_shell.send(enable_password + '\n')
    
    print('SSH Session:')
    print(f'Successfully connected to: {ip_address}')
    print(f'Username: {ssh_username}')
    print(f'Password: {ssh_password}')
    print(f'Enable Password: {enable_password}')

    # Send a command to output the running configuration
    ssh_shell.send('show running-config\n')
    running_config_ssh = ssh_shell.recv(65535).decode('utf-8')

    # Save the SSH running configuration to a local file
    with open(output_file, 'w') as file:
        file.write(running_config_ssh)

    print('Running configuration saved to', output_file)
    print('------------------------------------------------------')

    # Exit enable mode
    ssh_shell.send('exit\n')

    # Close SSH session
    ssh.close()
except Exception as e:
    print(f'SSH Session Failed: {e}')

# Load the offline configuration
offline_config_file = 'offline_config.txt'
with open(offline_config_file, 'r') as offline_file:
    offline_config = offline_file.read()

# Compare the configurations
diff = list(difflib.unified_diff(running_config_telnet.splitlines(), offline_config.splitlines()))

# Display the differences
print('Differences between the current running configuration and the offline version:')
for line in diff:
    if line.startswith('  '):
        continue  # Unchanged line
    elif line.startswith('- '):
        print(f'Removed: {line[2:]}')  # Line only in the offline config
    elif line.startswith('+ '):
        print(f'Added: {line[2:]}')  # Line only in the running config

print('------------------------------------------------------')


error message 
Traceback (most recent call last):
  File "/home/devasc/Downloads/f.py", line 24, in <module>
    tn.read_until(b'Password: ')
  File "/usr/lib/python3.8/telnetlib.py", line 315, in read_until
    if selector.select(timeout):
  File "/usr/lib/python3.8/selectors.py", line 415, in select
    fd_event_list = self._selector.poll(timeout)
KeyboardInterrupt
