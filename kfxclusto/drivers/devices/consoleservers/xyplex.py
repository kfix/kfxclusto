from clusto.drivers.devices.consoleservers.basicconsoleserver import BasicConsoleServer
from clusto.exceptions import ConnectionException
from clusto.drivers.resourcemanagers import IPManager

from subprocess import Popen

class XyplexMaxserverMixin():
    '''
   http://www.pimpworks.org/xyplex/ http://google.com/search?q=cache:a5iUaXT0y3MJ:www.pimpworks.org/xyplex/maxserver-getting-started.pdf
   http://loreley.flyingparchment.org.uk/pages/xyplex 
   http://service.mrv.com/downloads/view.cfm?tp=as_cabling.cfm&print=no

  http://www.gno.org/~gdr/xyplex/ (yay, plain HTML) 
  RESET
    power on, wait for full boot and press reset button with paper clip. All serial lights will illuminate. Press and hold reset.  When lights 14,15,16 light in a group, release reset.
    when run light flashes rapidly, hook serial terminal to any port and press enter a few times. When you recieve "Configuration in progress, please wait.", type in 'ACCESS' and hit return.
    sequence 3,y,enter,s,enter,y,enter will set factory defaults.

    on reboot, hit enter when run light is solid for prompt. default user+pass is "ACCESS"
    reconfig: http://www.pimpworks.org/xyplex/xyplex.html

   get enabled:
     set privilege
     (pass is "SYSTEM")

   see whats up:
     show parameter server
     show ip

   stop the set(running-config)/def(startup-config) dichtomy and set both simultaneously (using only def):
     set server change enable

   PROTIP: set GNU Screen's "slowpaste 20" and paste from its buffer


   set up ports:
     define port all telnet transmit immediate
     define port 1 telnet echo mode disable
     define port 2-40 telnet echo mode character
     define port all telnet newline nothing
     define port all telnet binary session mode passall
     define port all default session mode passall
     define port all broadcast disable
     define port 1 access local
     define port 2-40 access remote
     define port all speed 9600
     define port all autobaud disable
     define port all modem enable
     define port all dsrlogout disable
     define port dsrwait disable
     define port 2-40 dtrwait forconnection
     define port all flow control disable
     define port 2-40 dcd timeout 0
     define port all flow disable
     define port all typeahead 16348
     define port all autoprompt disabled
     define port all line editor disabled
     define port all verification disabled
     logout port 2-40


   to remotely log in to the admin port:
     telnet csm1.blah 2000
     (type enter - you will get a '#' prompt)
     (type access - you will get a normal login prompt)
     login as normal

   to kick a user:
     set privilege
     show users
     logout port 40 (or whatever)
'''

    def config_port_label(self, port):
      '''NOTE: I strenously suggest that you use a SEPARATE POLICY PACKAGE to interrogate clusto and render configs for your ports rather than storing your site-specific config policy in clusto drivers! This is only an example of what is possible...'''
      
    def telnet(self, port):
        host = IPManager.get_ips(self)
        if len(host) == 0:
            host = self.name
        else:
            host = host[0]

        proc = Popen(['telnet', host, str(port)])
        proc.communicate()


    def connect(self, porttype, num, ssh_user=None):
        '''connect to a client device console port via telnet. ssh_user is ignored'''

        if porttype != 'console-serial':
            raise DriverException("Cannot connect to a non-serial port")

        self.telnet(port=((num * 100) + 2000))

    def connect_admin(self, **kwargs):
        self.telnet(port=2000)


#class XyplexMaxserver1640(BasicConsoleServer, XyplexMaxserverMixin):
class XyplexMaxserver1640(XyplexMaxserverMixin, BasicConsoleServer):

    _driver_name = 'xyplexmaxserver1640'

    _portmeta = { 'pwr-nema-5' : { 'numports':1, },
                  'nic-eth' : { 'numports':1, },
                  'console-serial' : { 'numports':40, },
                  }


