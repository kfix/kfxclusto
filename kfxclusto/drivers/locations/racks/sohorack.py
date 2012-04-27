from clusto.drivers.locations.racks.basicrack import BasicRack

class SohoRack(BasicRack):
    '''a small office / home rack enclosure, usually on wheels'''

    _driver_name = "sohorack"

    _properties = {'minu':1,
                   'maxu':30}
    #loc-x, loc-y, loc-z ?
