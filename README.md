# autocaller
this script connects to asterisk using AMI user and imports two files: a numbers.list file and a voice.wav file, the script calls the numbers in numbers.list file and plays voice.wav for each number it calls.
```python
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
```

Here's how the script works:

1. The script sets up an AMI connection to Asterisk using the `asterisk.manager.Manager` class from the `python-asterisk` library.
2. The script reads the list of numbers from a `numbers.list` file and stores them in the `numbers` list.
3. The script sets the voice file to `voice.wav`.
4. The script loops through the `numbers` list and creates a call file for each number with the `Channel` set to the SIP channel for that number and the `Application` set to `Playback` with the `Data` set to the `voice_file`.
5. The script moves the call file to the outgoing directory for Asterisk to initiate the call.
6. The script waits for 5 seconds to allow the call to connect before making the next call.
7. The script disconnects from the AMI manager.

Note that this is a very basic example of a script that can initiate calls using Asterisk and the AMI. To make the script more robust, you may want to add error handling, logging, and other features to improve its functionality.
