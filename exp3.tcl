# Experiment 1

proc experiment_one {agent discipline} {

  set local 1

  # set constants
  set ns [new Simulator]
  set CBR_RATE 1mb
  
  if {$agent == "tahoe"} {
    set tcp [new Agent/TCP]
  } elseif {$agent == "reno"} {
    set tcp [new Agent/TCP/Reno]
  } elseif {$agent == "newreno"} {
    set tcp [new Agent/TCP/Newreno]
  } elseif {$agent == "vegas"} {
    set tcp [new Agent/TCP/Vegas]
  } elseif {$agent == "sack"} {
    set tcp [new Agent/TCP/Sack1]
  }

  # io
  global tf
  set tf [open ./logs/exp3/$agent/$agent-$discipline.tr w]
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
  $ns duplex-link $n1 $n2 10Mb 10ms $discipline
  $ns duplex-link $n5 $n2 10Mb 10ms $discipline
  $ns duplex-link $n2 $n3 10Mb 10ms $discipline
  $ns duplex-link $n3 $n4 10Mb 10ms $discipline
  $ns duplex-link $n3 $n6 10Mb 10ms $discipline
  
  # Add a CBR source at N5 and a sink at N6
  
  # Create UDP agent at node 5
  set udp [new Agent/UDP]
  $ns attach-agent $n5 $udp
  
  # Attach CBR to UDP at node 5
  set cbr [new Application/Traffic/CBR]
  $cbr set rate_ $CBR_RATE
  $cbr attach-agent $udp
  
  # Add sink at node 6 
  set null [new Agent/Null]
  $ns attach-agent $n6 $null
  
  # Connect send data from node 5 to node 6
  $ns connect $udp $null
  
  # Add a single TCP stream from N1 to a sink at N4
  
  $ns attach-agent $n1 $tcp
  
  # Add TCP sink to node 4
  set sink [new Agent/TCPSink]
  $ns attach-agent $n4 $sink
  
  # Send data from node 1 to node 4
  $ns connect $tcp $sink
  
  # Run FTP application
  set ftp [new Application/FTP]
  $ftp attach-agent $tcp
  
  # Simulation
  
  # Schedule events for the CBR and FTP agents
  $ns at 0.1 "$ftp start"
  $ns at 5.0 "$cbr start"
  $ns at 9.0 "$ftp stop"
  $ns at 9.9 "$cbr stop"
  
  # Call the finish procedure after 5 seconds of simulation time
  $ns at 10.0 "finish"
  
  #Run the simulation
  $ns run
}

experiment_one [lindex $argv 0] [lindex $argv 1]