require 'pcaprub'

capture = PCAPRUB::Pcap.open_live('eth0', 0xffff, true, 0)

capture.setfilter('port 80')

count = 0
capture.each_packet do |packet|
  count += 1
  puts "====/", count, "/===="
  puts packet.class, Time.at(packet.time)
  puts "micro => #{packet.microsec}"
  puts "Packet Length => #{packet.length}"
end

