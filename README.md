# Smart-home Python

This software is a gateway for smart home devices.
It is currently in beta and it's still being actively developed.

## Prerequisites

- Python ^3.7
- Raspberry PI 3 Model B or newer (with latest updates).
- Firebase `serviceAccountCreds` (for authenticating to Firebase Admin).

## How to run this program.

- Update your Linux repositories by running.

  `sudo apt update`

- In terminal run this command to install Python and necessary tools.

  `sudo apt install python-dev python3 python3-pip`

- Install necessary libraries with this command.

  `pip3 install -r requirements.txt`

- Run the program with sudo privileges (sudo is required for GPIO pins to be controlled).

  `sudo python3 app.py`
