import asterisk.manager
import os
import time

# Set up Asterisk Manager Interface (AMI) connection
ami_username = 'AMI_USERNAME'
ami_password = 'AMI_PASSWORD'
ami_host = 'AMI_HOST'
ami_port = 'AMI_PORT'

# Set up AMI manager
ami_manager = asterisk.manager.Manager()
ami_manager.connect(ami_host, int(ami_port))
ami_manager.login(ami_username, ami_password)

# Set up number list
with open('numbers.list', 'r') as f:
    numbers = [line.strip() for line in f]

# Set up voice file
voice_file = 'voice.wav'

# Loop through numbers and make calls
for number in numbers:
    # Set up call file
    call_file = f'/var/spool/asterisk/outgoing/call_{number}.call'
    with open(call_file, 'w') as f:
        f.write(f'Channel: SIP/{number}\n')
        f.write(f'Application: Playback\n')
        f.write(f'Data: {voice_file}\n')

    # Move call file to outgoing directory
    cmd = f'mv {call_file} /var/spool/asterisk/outgoing/'
    os.system(cmd)

    # Wait for call to connect
    time.sleep(5)

# Disconnect from AMI manager
ami_manager.logoff()
ami_manager.close()
