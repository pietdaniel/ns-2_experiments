#!/bin/bash
echo "Welcome back my friends to the show that never ends"
echo ""
echo "Running reno sims against CBR of 1,3,5,6,8,9,11 mb"
ns run.tcl reno 1mb
ns run.tcl reno 3mb
ns run.tcl reno 5mb
ns run.tcl reno 7mb
ns run.tcl reno 8mb
ns run.tcl reno 9mb
ns run.tcl reno 11mb
echo "Running newreno sims against CBR of 1,3,5,6,8,9,11 mb"
ns run.tcl newreno 1mb
ns run.tcl newreno 3mb
ns run.tcl newreno 5mb
ns run.tcl newreno 7mb
ns run.tcl newreno 8mb
ns run.tcl newreno 9mb
ns run.tcl newreno 11mb
echo "Running tahoe sims against CBR of 1,3,5,6,8,9,11 mb"
ns run.tcl tahoe 1mb
ns run.tcl tahoe 3mb
ns run.tcl tahoe 5mb
ns run.tcl tahoe 7mb
ns run.tcl tahoe 8mb
ns run.tcl tahoe 9mb
ns run.tcl tahoe 11mb
echo "Running vegas sims against CBR of 1,3,5,6,8,9,11 mb"
ns run.tcl vegas 1mb
ns run.tcl vegas 3mb
ns run.tcl vegas 5mb
ns run.tcl vegas 7mb
ns run.tcl vegas 8mb
ns run.tcl vegas 9mb
ns run.tcl vegas 11mb
