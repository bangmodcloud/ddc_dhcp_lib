from pydhcplib.format_handler import FormatHandler
from datetime import date

class DhcpAddrHandler:
  def __init__(self, lease_time):
    self.lease_time = lease_time
    self.available_addr = [{
      'ip': FormatHandler.fromip("192.168.1.1"),
      'exp': None
    } 
    for x in range(255)]

  def is_lease_time_expire(self, addr):
    return addr['exp'] == None or addr['exp'] < date.today()

  def first_addr(self):
    return next(filter(self.is_lease_time_expire, self.available_addr), None)

  def offer(self):
    offer_ip = self.first_addr()
    if offer_ip == None:
      raise Exception("Dhcp ran out of ip.")
    offer_ip['exp'] = date.today()
    return offer_ip

  def ack(self):
    return self.available_addr

lung_pol = DhcpAddrHandler(86400)
k = lung_pol.offer()
print(k)