#!/bin/bash
echo "Welcome back my friends to the show that never ends"
echo ""
echo "Running reno sims against CBR of 1,3,5,6,8,9,11 mb"
ns exp1.tcl reno 1mb
ns exp1.tcl reno 3mb
ns exp1.tcl reno 5mb
ns exp1.tcl reno 7mb
ns exp1.tcl reno 8mb
ns exp1.tcl reno 9mb
ns exp1.tcl reno 11mb
echo "Running newreno sims against CBR of 1,3,5,6,8,9,11 mb"
ns exp1.tcl newreno 1mb
ns exp1.tcl newreno 3mb
ns exp1.tcl newreno 5mb
ns exp1.tcl newreno 7mb
ns exp1.tcl newreno 8mb
ns exp1.tcl newreno 9mb
ns exp1.tcl newreno 11mb
echo "Running tahoe sims against CBR of 1,3,5,6,8,9,11 mb"
ns exp1.tcl tahoe 1mb
ns exp1.tcl tahoe 3mb
ns exp1.tcl tahoe 5mb
ns exp1.tcl tahoe 7mb
ns exp1.tcl tahoe 8mb
ns exp1.tcl tahoe 9mb
ns exp1.tcl tahoe 11mb
echo "Running vegas sims against CBR of 1,3,5,6,8,9,11 mb"
ns exp1.tcl vegas 1mb
ns exp1.tcl vegas 3mb
ns exp1.tcl vegas 5mb
ns exp1.tcl vegas 7mb
ns exp1.tcl vegas 8mb
ns exp1.tcl vegas 9mb
ns exp1.tcl vegas 11mb
