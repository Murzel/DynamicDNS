# DynDNS

This Python-Code keep track of your public ip address.

Requirements:
- Python 3.9

It will connect to your router through DynV2 protocol.
After that, you see your new entries through the created txt file or by the webserver.

In the browser just type the local ip address of the device running this script with the port (default port is 1337).
e.g.: 192.168.2.102:1337

You can also include your own code, which will be triggered when the ip changes.
An example, where the GoDaddy DNS Record will be updated, is already provided in the code.
