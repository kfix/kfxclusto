"""
APC Power Strips

"""
from clusto.drivers.devices.powerstrips.basicpowerstrip import BasicPowerStrip
from clusto.drivers.devices.common import IPMixin, SNMPMixin
from clusto.drivers.resourcemanagers import IPManager
from clusto.exceptions import DriverException

from scapy.all import SNMP, SNMPget, SNMPset, SNMPnext, SNMPvarbind
from socket import socket, AF_INET, SOCK_DGRAM

class APCPowernet(BasicPowerStrip, IPMixin, SNMPMixin):
    """
    Provides core SNMP functions for APC Powernet strips

    """

    _driver_name = "apcpowernet"

    #_properties = {'withslave':0}

    _outlet_states = ['outletOn', 'outletOff', 'outletReboot', 'outletUnknown', 'outletOnWithDelay', 'outletOffWithDelay', 'outletRebootWithDelay']

    def _ensure_portnum(self, porttype, portnum):
        """map powertower port names to clusto port numbers"""

        if not self._portmeta.has_key(porttype):
            msg = "No port %s:%s exists on %s." % (porttype, str(num), self.name)
                    
            raise ConnectionException(msg)

        if isinstance(portnum, int):
            num = portnum
        else:
            '''alphanumeric ports are the DEVIL!'''
            msg = "No non-numeric port %s:%s exists on %s." % (porttype, str(num), self.name)
            raise ConnectionException(msg)
 
        numports = self._portmeta[porttype]
        #if self.withslave:
        #    if porttype in ['mains', 'pwr']:
        #        numports *= 2

        if num < 0 or num >= numports:
            msg = "No port %s:%s exists on %s." % (porttype, str(num), 
                                                   self.name)
            raise ConnectionException(msg)

        return num

    def _get_port_oid(self, outlet):
        return '.1.3.6.1.4.1.318.1.1.12.3.3.1.1.4.' + str(outlet)
        #^hardcoding for now, will do the retrieve style checking later
        for oid, value in self._snmp_walk('1.3.6.1.4.1.1718.3.2.3.1.2'):
            if value.lower() == outlet:
                return oid

    def get_outlet_state(self, outlet):
        oid = self._get_port_oid(outlet)
        state = self._snmp_get(oid)
        return self._outlet_states[int(state) - 1]

    def set_outlet_state(self, outlet, state, session=None):
        oid = self._get_port_oid(outlet)
        r = self._snmp_set(oid, state)
        if r.PDU.varbindlist[0].value.val != state:
            raise DriverException('Unable to set SNMP state')

    def set_power_off(self, porttype, portnum):
        if porttype != 'pwr-nema-5':
            raise DriverException('Cannot turn off ports of type: %s' % str(porttype))
        state = self.set_outlet_state(portnum, 2)

    def set_power_on(self, porttype, portnum):
        if porttype != 'pwr-nema-5':
            raise DriverException('Cannot turn on ports of type: %s' % str(porttype))
        state = self.set_outlet_state(portnum, 1)

    def reboot(self, porttype, portnum):
        if porttype != 'pwr-nema-5':
            raise DriverException('Cannot turn reboot ports of type: %s' % str(porttype))
        state = self.set_outlet_state(portnum, 3)

    #overriding default version 2 with v1
    #need to update the firmware http://www.apcmedia.com/salestools/ASTE-6Z6KAV_R1_EN.pdf
    def _snmp_set(self, oid, value):
        community, sock = self._snmp_connect()

        pdu = SNMPset(varbindlist=[SNMPvarbind(oid=str(oid), value=value)])
        p = SNMP(version=0, community=community, PDU=pdu) #{0:"v1", 1:"v2c", 2:"v2", 3:"v3"})
        sock.sendall(p.build())

        r = SNMP(sock.recv(4096))
        return r

class APCPowernet7960(APCPowernet):
    """
    Provides support for APC Powernet strips

    Power Port designations start with 1 at the upper left (.aa1) down to 32
    at the bottom right (.bb8).
    """

    _driver_name = "apcpernet7960"

    _portmeta = { 'pwr-nema-L5': { 'numports':1 },
                  'pwr-nema-5' : { 'numports':24, },
                  'nic-eth' : { 'numports':1, },
                  'console-serial' : { 'numports':1, },
                  }

