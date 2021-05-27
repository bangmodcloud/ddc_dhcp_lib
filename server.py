#!/usr/bin/python
#
# pydhcplib
# Copyright (C) 2008 Mathieu Ignacio -- mignacio@april.org
#
# This file is part of pydhcplib.
# Pydhcplib is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

from pydhcplib.dhcp_packet import *
from pydhcplib.dhcp_network import *
import struct


netopt = {'client_listen_port':"68",
           'server_listen_port':"67",
           'listen_address':"0.0.0.0"}

class DhcpPacketHandler:
  def CreateOfferPacket(packet):
      offer = DhcpPacket()
      offer.CreateDhcpOfferPacketFrom(packet)
      offer.SetOption("yiaddr", [10,10,8,11])
      offer.SetLeaseTime(86400)
      offer.SetOption("router", [10,10,8,1])
      offer.SetOption("subnet_mask", [255,255,255,0])
      offer.SetOption("server_identifier", [10,10,6,21])
      offer.SetOption("tftp_server_name", strlist("10.10.8.1").list())
      offer.SetOption("bootfile_name", strlist("undionly.kpxe").list())
      offer.SetOption("domain_name_server", [8,8,8,8])
      return offer

  def CreateAckPacket(packet):
      ack = DhcpPacket()
      ack.CreateDhcpAckPacketFrom(packet)
      ack.SetOption("siaddr", [10,10,8,1])
      ack.SetOption("yiaddr", [10,10,8,11])
      ack.SetLeaseTime(86400)
      ack.SetOption("router", [10,10,8,1])
      ack.SetOption("subnet_mask", [255,255,255,0])
      ack.SetOption("server_identifier", [10,10,6,21])
      ack.SetOption("tftp_server_name", strlist("10.10.8.1").list())
      ack.SetOption("bootfile_name", strlist("undionly.kpxe").list())
      ack.SetOption("domain_name_server", [8,8,8,8])
      return ack

class Server(DhcpServer):
    def __init__(self, options):
        DhcpServer.__init__(self,options["listen_address"],
                            options["client_listen_port"],
                            options["server_listen_port"])
        
    def HandleDhcpDiscover(self, packet):
        offer = DhcpPacketHandler.CreateOfferPacket(packet)
        self.SendDhcpPacketTo(offer, "10.10.6.1", 67)

    def HandleDhcpRequest(self, packet):
        ack = DhcpPacketHandler.CreateAckPacket(packet)
        self.SendDhcpPacketTo(offer, "10.10.6.1", 67)

    def HandleDhcpDecline(self, packet):
        pass

    def HandleDhcpRelease(self, packet):
        pass

    def HandleDhcpInform(self, packet):
        pass


server = Server(netopt)

while True :
    server.GetNextDhcpPacket()
