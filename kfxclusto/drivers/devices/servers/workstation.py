"""
Drivers for generic workstations
"""

from clusto.drivers.devices.servers.basicserver import BasicServer

class Workstation(BasicServer):
    """a workstation. meaning a big box chassis and no niceties like redundant PSU, serial BIOS, IPMI/DRAC/wfm/ILO/etc"""
    _driver_name = "workstation"

    asset_tag = None #linkage to accounting/inventory history on machine
    profile = None #linkage to detailed spec sheet on machine

class Workstation5U(Workstation):
    _driver_name = "workstation5u"
    _portmeta = {'pwr-nema-5': {'numports': 1},
                 'nic-eth': {'numports': 1},
                 'console-serial': {'numports': 1}}
    rack_units = 5

