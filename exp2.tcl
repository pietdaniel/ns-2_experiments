# Experiment 2

proc experiment_two {ax ay cbr_rate} {
  global tcpx tcpy

  set local 1

  # set constants
  set ns [new Simulator]
  set CBR_RATE $cbr_rate

  # tcp x
  if {$ax == "tahoe"} {
    set tcpx [new Agent/TCP]
  } elseif {$ax == "reno"} {
    set tcpx [new Agent/TCP/Reno]
  } elseif {$ax == "newreno"} {
    set tcpx [new Agent/TCP/Newreno]
  } elseif {$ax == "vegas"} {
    set tcpx [new Agent/TCP/Vegas]
  }

  #tcp y
  if {$ay == "tahoe"} {
    set tcpy [new Agent/TCP]
  } elseif {$ay == "reno"} {
    set tcpy [new Agent/TCP/Reno]
  } elseif {$ay == "newreno"} {
    set tcpy [new Agent/TCP/Newreno]
  } elseif {$ay == "vegas"} {
    set tcpy [new Agent/TCP/Vegas]
  }

  # io
  global tf
  set tf [open ./logs/exp2/$ax$ay/exp2-$CBR_RATE-$ax$ay.tr w]
  $ns trace-all $tf


  proc finish {} {
    global tf
    close $tf
    exit 0
  }

  # Create six nodes
  set n1 [$ns node]
  set n2 [$ns node]
  set n3 [$ns node]
  set n4 [$ns node]
  set n5 [$ns node]
  set n6 [$ns node]
  
  # Connect nodes
  $ns duplex-link $n1 $n2 10Mb 10ms DropTail
  $ns duplex-link $n5 $n2 10Mb 10ms DropTail
  $ns duplex-link $n2 $n3 10Mb 10ms DropTail
  $ns duplex-link $n3 $n4 10Mb 10ms DropTail
  $ns duplex-link $n3 $n6 10Mb 10ms DropTail
  
  # Add a CBR source at N2 and a sink at N3
  
  # Create UDP agent at node 2
  set udp [new Agent/UDP]
  $ns attach-agent $n2 $udp
  
  # Attach CBR to UDP at node 2
  set cbr [new Application/Traffic/CBR]
  $cbr set rate_ $CBR_RATE
  $cbr attach-agent $udp
  
  # Add sink at node 3 
  set null [new Agent/Null]
  $ns attach-agent $n3 $null
  
  # Connect send data from node 2 to node 3
  $ns connect $udp $null
  
  # Add a single TCP stream from N1 to a sink at N4
  
  $ns attach-agent $n1 $tcpx
  
  # Add TCP sink to node 4
  set sinkx [new Agent/TCPSink]
  $ns attach-agent $n4 $sinkx
  
  # Send data from node 1 to node 4
  $ns connect $tcpx $sinkx
  
  # Run FTP application
  set ftpx [new Application/FTP]
  $ftpx attach-agent $tcpx

  # Add a single TCP stream from N5 to a sink at N6
  $ns attach-agent $n5 $tcpy
  
  # Add TCP sink to node 4
  set sinky [new Agent/TCPSink]
  $ns attach-agent $n6 $sinky
  
  # Send data from node 1 to node 4
  $ns connect $tcpy $sinky
  
  # Run FTP application
  set ftpy [new Application/FTP]
  $ftpy attach-agent $tcpy
  
  # Simulation
  
  # Schedule events for the CBR and FTP agents
  $ns at 0.1 "$cbr start"
  $ns at 1.0 "$ftpx start"
  $ns at 1.1 "$ftpy start"
  $ns at 9.0 "$ftpx stop"
  $ns at 9.0 "$ftpy stop"
  $ns at 9.9 "$cbr stop"
  
  # Call the finish procedure after 5 seconds of simulation time
  $ns at 10.0 "finish"
  
  #Run the simulation
  $ns run
}

experiment_two [lindex $argv 0] [lindex $argv 1] [lindex $argv 2]
