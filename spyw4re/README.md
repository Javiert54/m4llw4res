# Spyware (Dummy)

This folder contains an example of a dummy spyware program for educational purposes only.

## Features:

This malware has the following features:

- Gets the public IP address and the local Ip address
- Collect cockies and history from all browsers
- Gets usernames from the device
- Uses a key-logger to register any keystrokes
- Performs network-scans to discover all hosts on the network
- Performs port-scans to every discovered host
- Takes periodical screenshots
- Lists all aplications installed on the device
- Sends all the collected data to a remote SSH server
- Raises a http server


## Installation:

WARNING: This program is for educational purposes only. Running unauthorized spyware is illegal and harmful.  We recommend using this program in a safe, virtualized environment to understand how spyware works.

Instructions for setting up a virtual machine can be found in the main README.

Once you have your virtual machine set up:

Clone the repository from GitHub. (Instructions in main README)

Navigate to the spyware folder:

````Bash
cd m4llw4res/spyware
#Install all the dependencies
pip install -r requirements.txt
```` 
Run the program:

````Bash
#First, you need to run the quickSetup.py script to set up the settings.json file
python quickSetup.py
#Then, you can run the program
python run_spyware.py
````

Disclaimer: This project is intended for educational purposes only. The code provided should not be used for any illegal activities. The authors are not responsible for any misuse of the code. Use this project responsibly and only for learning and experimentation.