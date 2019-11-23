from joanna.network import Network
from time import sleep

class ChangeNetwork(Network):

    def change_bri_tlkm(self):
        cmd = ['config vdom', 'edit SERVICES', 'config router static','edit 64', 'set distance 50','end']
        self.command_firewall('extfw-a', cmd)
        return

    def change_bri_lintas(self):
        cmd = ['config vdom', 'edit SERVICES', 'config router static','edit 64', 'set distance 150','end']
        self.command_firewall('extfw-a', cmd)
        return

    def change_danamon_tlkm(self):
        cmd = ['config vdom', 'edit SERVICES', 'config router static', 'edit 41', 'set distance 100', 'end']
        self.command_firewall('extfw-a', cmd)
        return

    def change_danamon_lintas(self):
        cmd = ['config vdom', 'edit SERVICES', 'config router static', 'edit 41', 'set distance 10', 'end']
        self.command_firewall('extfw-a', cmd)
        return

    def change_bni_tlkm(self):
        cmd = ['config vdom', 'edit SERVICES', 'config router static','edit 65', 'set distance 100','end']
        self.command_firewall('extfw-a', cmd)
        return

    def change_bni_lintas(self):
        cmd = ['config vdom', 'edit SERVICES', 'config router static','edit 65', 'set distance 10','end']
        self.command_firewall('extfw-a', cmd)
        return


    def change_to_telkom(self):
        cmd = ['route-map TELKOM-DOMESTIC-LP permit 10', 'set local-preference 300', 'route-map TELKOM-GLOBAL-LP permit 10',
               'set local-preference 300', 'router bgp 58557', 'no neighbor 36.91.235.21 route-map AS_PREPEND_TELKOM out',
               'no neighbor 36.91.235.17 route-map AS_PREPEND_TELKOM out']
        self.config_cisco('core-a', ['router bgp 58557', 'neighbor 61.8.78.21 route-map AS_PREPEND_LA out',
                                     'neighbor 202.152.44.121 route-map AS_PREPEND_LA out'])
        self.config_cisco('core-b', cmd)
        sleep(1)
        self.command_cisco('core-b', 'clear ip bgp * soft')
        sleep(2)
        self.command_cisco('core-a', 'clear ip bgp * soft')
        return

    def change_to_lintas(self):
        cmd = ['route-map TELKOM-DOMESTIC-LP permit 10', 'set local-preference 100', 'route-map TELKOM-GLOBAL-LP permit 10',
               'set local-preference 100','router bgp 58557', 'neighbor 36.91.235.21 route-map AS_PREPEND_TELKOM out',
               'neighbor 36.91.235.17 route-map AS_PREPEND_TELKOM out','do clear ip bgp * soft']
        self.config_cisco('core-a', ['router bgp 58557', 'no neighbor 61.8.78.21 route-map AS_PREPEND_LA out',
                                     'no neighbor 202.152.44.121 route-map AS_PREPEND_LA out', 'do clear ip bgp * soft out'])
        self.config_cisco('core-b', cmd)
        return

    def change_telkom_domestic(self):
        cmd = ['route-map TELKOM-DOMESTIC-LP permit 10', 'set local-preference 300', 'router bgp 58557',
               'no neighbor 36.91.235.21 route-map AS_PREPEND_TELKOM out', 'do clear ip bgp * soft', 'do wr']
        self.config_cisco('core-a', ['router bgp 58557','neighbor 61.8.78.21 route-map AS_PREPEND_LA out',
                                     'do clear ip bgp * soft', 'do wr'])
        self.config_cisco('core-b', cmd)
        return

    def change_telkom_global(self):
        cmd = ['route-map TELKOM-GLOBAL-LP permit 10', 'set local-preference 300', 'router bgp 58557',
               'no neighbor 36.91.235.17 route-map AS_PREPEND_TELKOM out', 'do clear ip bgp * soft', 'do wr']
        self.config_cisco('core-a', ['router bgp 58557', 'neighbor 202.152.44.121 route-map AS_PREPEND_LA out',
                                     'do clear ip bgp * soft out', 'do wr'])
        self.config_cisco('core-b', cmd)
        return


    def change_la_domestic(self):
        cmd = ['route-map TELKOM-DOMESTIC-LP permit 10', 'set local-preference 100', 'router bgp 58557',
               'neighbor 36.91.235.21 route-map AS_PREPEND_TELKOM out', 'do clear ip bgp * soft', 'do wr']
        self.config_cisco('core-a', ['neighbor 61.8.78.21 route-map AS_PREPEND_LA out', 'do clear ip bgp * soft',
                                     'do wr'])
        self.config_cisco('core-b', cmd)

    def change_la_global(self):
        cmd = ['route-map TELKOM-GLOBAL-LP permit 10', 'set local-preference 100', 'router bgp 58557',
               'neighbor 36.91.235.17 route-map AS_PREPEND_TELKOM out', 'do clear ip bgp * soft', 'do wr']
        self.config_cisco('core-a', ['router bgp 58557', 'no neighbor 202.152.44.121 route-map AS_PREPEND_LA out',
                                     'do clear ip bgp * soft out', 'do wr'])
        self.config_cisco('core-b', cmd)