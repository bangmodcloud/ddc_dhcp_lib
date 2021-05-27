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
import socket

netopt = {'client_listen_port':"68",
          'server_listen_port':"67",
          'listen_address':"0.0.0.0"}

class DhcpPacketHandler:
  def __init__(self, server_identifier):
      # change format from str of 'xx.xx.xx.xx' to [xx, xx ,xx ,xx]
      self.server_identifier = list(map(int, server_identifier.split('.')))

  def CreateOfferPacket(self, packet):
      offer = DhcpPacket()
      offer.CreateDhcpOfferPacketFrom(packet)
      # todo assign the proper ip to client
      offer.SetOption("yiaddr", [10,10,8,11])
      offer.SetLeaseTime(86400)
      # todo assign the proper router ip
      offer.SetOption("router", [10,10,8,1])
      offer.SetOption("subnet_mask", [255,255,255,0])
      offer.SetOption("server_identifier", self.server_identifier)
      # todo assign the proper router ip
      offer.SetOption("tftp_server_name", strlist("10.10.8.1").list())
      offer.SetOption("domain_name_server", [8,8,8,8])
      self.SelectBootfile(packet, offer)
      return offer

  def CreateAckPacket(self, packet):
      ack = DhcpPacket()
      ack.CreateDhcpAckPacketFrom(packet)
      ack.SetOption("siaddr", [10,10,8,1])
      ack.SetOption("yiaddr", [10,10,8,11])
      ack.SetLeaseTime(86400)
      ack.SetOption("router", [10,10,8,1])
      ack.SetOption("subnet_mask", [255,255,255,0])
      ack.SetOption("server_identifier", self.server_identifier)
      ack.SetOption("tftp_server_name", strlist("10.10.8.1").list())
      ack.SetOption("domain_name_server", [8,8,8,8])
      self.SelectBootfile(packet, ack)
      return ack
  
  def SelectBootfile(self, source_packet, target_packet):
      if source_packet.IsOption("user_class") and source_packet.GetOption("user_class") == strlist("iPXE").list():
        target_packet.SetOption("bootfile_name", strlist("http://file.doge.in.th/debian-raid-1.ipxe").list())
      elif source_packet.GetOption("client_system") == [0,0]:
        target_packet.SetOption("bootfile_name", strlist("undionly.kpxe").list())
      else:
        target_packet.SetOption("bootfile_name", strlist("ipxe.efi").list())

class Server(DhcpServer):
    def __init__(self, options):
        self.packet_handler = DhcpPacketHandler(server_identifier=self.GetServerIdentifier())
        DhcpServer.__init__(self,options["listen_address"],
                            options["client_listen_port"],
                            options["server_listen_port"])
        
    def HandleDhcpDiscover(self, packet):
        offer = self.packet_handler.CreateOfferPacket(packet)
        self.SendDhcpPacketTo(offer, "10.10.6.1", 67)

    def HandleDhcpRequest(self, packet):
        ack = self.packet_handler.CreateAckPacket(packet)
        self.SendDhcpPacketTo(ack, "10.10.6.1", 67)

    def HandleDhcpDecline(self, packet):
        pass

    def HandleDhcpRelease(self, packet):
        pass

    def HandleDhcpInform(self, packet):
        pass

server = Server(netopt)

while True :
    server.GetNextDhcpPacket()
