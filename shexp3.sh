#!/bin/bash
echo "Welcome back my friends to the show that never ends"
echo ""
echo "Running Reno sims for queues DropTail and RED"
ns exp3.tcl reno DropTail
ns exp3.tcl reno RED
echo "Running SACK sims for queues DropTail and RED"
ns exp3.tcl sack DropTail
ns exp3.tcl sack RED
