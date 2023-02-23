import socket

import upnpy
import upnpy.exceptions

import urllib.request

import sys

def get_internal_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # connect() for UDP doesn't send packets
    s.connect(('10.0.0.0', 0)) 
    internal_ip = s.getsockname()[0]
    s.close()
    return internal_ip


def upnp_port_forward(external_port: int, internal_port: int, lease_duration=0):
    internal_client_ip = get_internal_ip()
    upnp = upnpy.UPnP()
    devices = upnp.discover()
    if len(devices) == 0:
        return "No devices found"
    gateway_device = upnp.get_igd()
    services = gateway_device.get_services()
    if 'WANIPConnection1' not in services:
        return "WANIPConnection not found"
    port_forward_service = gateway_device['WANIPConnection1']
    actions = port_forward_service.get_actions()
    if 'AddPortMapping' not in actions:
        return "Port forwarding not enabled"
    try:
        port_forward_service.AddPortMapping(
            NewRemoteHost='',
            NewExternalPort=external_port,
            NewProtocol='TCP',
            NewInternalPort=internal_port,
            NewInternalClient=internal_client_ip,
            NewEnabled=1,
            NewPortMappingDescription='Cloud in a Bottle service',
            NewLeaseDuration=lease_duration
        )
    except (upnpy.exceptions.ActionNotFoundError, upnpy.exceptions.SOAPError) as error:
        return "Port Forwarding not Available"

# check if a port is open
def check_port(external_ip, external_port):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        socket.setdefaulttimeout(1)

        # returns an error indicator
        result = s.connect_ex((external_ip, external_port))
        if result == 0:
            print(f"Port {external_port} is open")
        else:
            print(f"Port {external_port} is closed")
        s.close()
        return True if result == 0 else False

    except KeyboardInterrupt:
        print("\n Exiting Program !!!!")
    except socket.gaierror:
        print("\n Hostname Could Not Be Resolved !!!!")
    except socket.error:
        print("\n Server not responding !!!!")


def setup():
    internal_ip = socket.gethostbyname(socket.gethostname())
    external_ip = urllib.request.urlopen('https://ident.me').read().decode('utf8')
    # setup screen
    # ask for internal port, external port, internal client ip, and lease duration
    # internal_port = int(input("Port between 49152-65535"))
    # external_port = int(input("Port between 49152-65535"))
    # lease_duration = int(input())

    # attempt to use upnp with those values
    # upnp_port_forward(internal_port, external_port, internal_ip, lease_duration)

    # if upnp not work, bring up port forwarding guide

    # port sniff to check if port has been forwarded
    # in a separate thread:
    #   while True:
    #       check_port(external_ip, external_port)
    # if port detected:
    #   print(f"Port {external_port} open")


def health_checker():
    external_ip = urllib.request.urlopen('https://ident.me').read().decode('utf8')
    external_port = None
    check_port(external_ip, external_port)
    

def main():
    pass


if __name__ == "__main__":
    print(upnp_port_forward(8000, 8000))
