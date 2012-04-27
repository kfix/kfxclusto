#from clusto.drivers.locations.datacenters.basicdatacenter import BasicDatacenter
#class SohoDatacenter(BasicDatacenter):

import clusto.drivers.locations.datacenters.basicdatacenter
class SohoDatacenter(clusto.drivers.locations.datacenters.basicdatacenter.BasicDatacenter):
    """
    Small office/Home "datacenter" (closet, garage, shed) driver
    """

    _clusto_type = "datacenter"
    _driver_name = "sohodatacenter"

    def remote_hands(self):
      raise NotImplemented
      #add a nice modular way to plug in a Vendor() contact so can send them a basic message prepoluated with pertinent info on the device/rack in question...
