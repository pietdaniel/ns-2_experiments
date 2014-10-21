 4        5
  \      / 
   1----2
  /      \
 0        3

 CBR 1 -> 2
 TCP 0 -> 3

cbr n2 -> n3
tcp stream n1 -> n4
analyze 
 -throughput
 -packed drop rate
 -latency
 -- as function of bandwith used by cbr
   1Mbps
   2Mbps tcp performance
conduct on 
 tahoe reno new reno vegas

which get higher average throughput
lowest average latency
fewest drops
'best' tcp variant or not
