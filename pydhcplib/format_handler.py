from pydhcplib.dhcp_packet import *

class FormatHandler:
  def fromstr(_str):
    return strlist(_str).list()
  
  def fromip(_ip):
    return list(map(int, _ip.split('.')))
  
  def fromint(_int):
    return [(b) for b in pack('>L', _int)]