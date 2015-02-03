#!/usr/bin/env ruby

require 'packetfu'

cap = PacketFu::Capture.new(:start => true, :iface => 'eth0', :filter => 'ip')

cap.stream.each do |p|
	pkt = PacketFu::Packet.parse(p)
	puts pkt.inspect
end
