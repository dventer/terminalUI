from netmiko import Netmiko
from joanna.network import Network
import re, socket, requests
from varhost import *

class CheckNetwork(Network):

    def check_bca(self):
        cmd = ['config vdom', 'edit SERVICES', f'get router info routing-table details | grep {svrbca}']
        device = {
            'ip': 'extfw-a',
            'username': self.username,
            'password': self.password,
            'use_keys': self.keys,
            'device_type': 'fortinet',
        }

        net_connect = Netmiko(**device, fast_cli=True)
        for command in cmd[:-1]:
            net_connect.send_command(command, expect_string=r"#")
        gateway = re.findall(r'[0-9]+(?:\.[0-9]+){3}', net_connect.send_command(cmd[-1]))[-1]
        if gateway == '{bankswa}':
            print("\n[BCA] Currently using CBN")
            result = self.command_cisco(f'{rtrbcacbn}',[f'sh crypto isakmp sa | i {cbnbca}', f'ping {cbnbca} repeat 10',
                                                      f'show ip bgp sum | i {cbnbca}'])
            if 'ACTIVE' in result[0]:
                print('\nIPSEC is UP')
            else:
                print('\nIPSECis DOWN')

            ping = [int(s) for s in result[1].split() if s.isdigit()]
            if ping[-1] == 100:
                print("[CBN] Connection Good")
            elif ping[-1] == 0:
                print("[CBN] Connection Timeout")
            else:
                print("[CBN] Connection Intermitten, Success Rate is " + str(ping[-1]))

            if any(char.isdigit() for char in result[-1].split()[-1]):
                print("[BGP] UP")
            else:
                print("[BGP] Down")

        elif gateway == '{bankswb}':
            print("[BCA] Primary Link Telkom")
            result = self.command_cisco(f'{rtrbcatlkm}', [f'sh crypto isakmp sa | i {tlkmbca}', f'ping {tlkmbca}'])
            ping = [int(s) for s in result[1].split() if s.isdigit()]
            if 'ACTIVE' in result[0]:
                print('\nIPSEC is UP')
            else:
                print('\nIPSECis DOWN')
            if ping[-1] == 100:
                print("[Telkom] Connection Good")
            elif ping[-1] == 0:
                print("[Telkom] Connection Timeout")
            else:
                print("[Telkom] Connection Intermitten, Success Rate is " + str(ping[-1]))

        else:
            print("Invalid Gateway")




    def check_bri(self):
        cmd = ['config vdom', 'edit SERVICES', f'get router info routing-table details | grep {svrbri}']
        device = {
            'ip': 'extfw-a',
            'username': self.username,
            'password': self.password,
            'use_keys': self.keys,
            'device_type': 'fortinet',
        }
        net_connect = Netmiko(**device, fast_cli=True)
        for command in cmd[:-1]:
            net_connect.send_command(command, expect_string=r"#")
        gateway = re.findall(r'[0-9]+(?:\.[0-9]+){3}', net_connect.send_command(cmd[-1]))[-1]
        return gateway

    def check_mandiri(self):
        Lintas = self.command_cisco('banksw-b', f'ping {lintasbmri} repeat 10')
        Telkom = self.command_cisco('banksw-a', f'ping {tlkmbmri} repeat 10')
        LintasValue = [int(s) for s in Lintas.split() if s.isdigit()]
        TelkomValue = [int(s) for s in Telkom.split() if s.isdigit()]
        if LintasValue[-1] == 100:
            print("\n[Lintas] Connection Good")
        elif LintasValue == 0:
            print("\n[Lintas] Connection Timeout")
        else:
            print("\n[Lintas] Connection Intermitten")
            print("Success Rate = " + LintasValue[-1])
        try:
            lintasPort = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            lintasPort.settimeout(2)
            lintasPort.connect((lintassvrbmri, portbmri))
            print(f"{lintassvrbmri} port {portbmri} is Connected\n")
            lintasPort.close()
        except:
            print(f"{lintassvrbmri} port {portbmri} is Timeout\n")
            lintasPort.close()

        if TelkomValue[-1] == 100:
            print("\n[Telkom] Connection Good")
        elif TelkomValue == 0:
            print("\n[Telkom] Connection Timeout")
        else:
            print("\n[Telkom] Connection Intermitten")
            print("Success Rate = " + str(TelkomValue[-1]))

        try:
            telkomPort = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            telkomPort.connect((tlkmsvrbmri, portbmri))
            telkomPort.settimeout(2)
            print(f"{tlkmsvrbmri} port {portbmri} is Connected\n")
            telkomPort.close()
        except:
            print(f"{tlkmsvrbmri} port {portbmri} is Timeout\n")
            telkomPort.close()



    def check_inet(self):
        la_lp = self.command_cisco('core-a', ['sh route-map LA-DOMESTIC-LP | i preference','sh route-map LA-GLOBAL-LP | i preference'])
        la_domestic, la_global = int(la_lp[0].lstrip().split(' ')[1]), int(la_lp[1].lstrip().split(' ')[1])
        tlkm_lp = self.command_cisco('core-b', ['sh route-map TELKOM-DOMESTIC-LP | i preference', 'sh route-map TELKOM-GLOBAL-LP | i preference'])
        tlkm_domestic, tlkm_global = int(tlkm_lp[0].lstrip().split(' ')[1]), int(tlkm_lp[1].lstrip().split(' ')[1])
        if la_domestic > tlkm_domestic:
            print('\n\nDomestic connection using Lintasarta')
        elif la_domestic < tlkm_domestic:
            print('\n\nDomestic Connection using Telkom')
        else:
            print('\n\nPlease Check your Local-Preference, maybe it has same value...')

        if la_global > tlkm_global:
            print('International connection using Lintasarta\n\n')
        elif la_global < tlkm_global:
            print('International connection using Telkom\n\n')
        else:
            print('Please Check your Local-Preference, maybe it has same value...\n\n')

        if la_domestic > tlkm_domestic:
            output = self.command_cisco('core-a', 'sh ip bgp sum')
            if 'Idle' in output or 'Active' in output:
                print("[BGP] Failed!")
            else:
                print("[BGP] Success!")
        elif la_domestic < tlkm_domestic:
            output = self.command_cisco('core-b', 'sh ip bgp sum')
            if 'Idle' in output or 'Active' in output:
                print("[BGP] Peering Failed!")
            else:
                print("[BGP] Peering Success!")
        else:
            print("Please Check BGP Configuration")


        try:
            socket.gethostbyname('www.google.com')
            socket.gethostbyname('www.detik.com')
            print("[DNS] Query Success!")
        except:
            print("[DNS] Query Failed!")

        try:
            requests.get('https://www.google.com', timeout=4, verify=True)
            requests.get('https://www.detik.com', timeout=4, verify=True)
            print("[HTTP Request] Success!\n")
        except:
            print("[HTTP Request] Failed!\n")







