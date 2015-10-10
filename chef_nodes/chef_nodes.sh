#!/bin/sh
export HOME=/home/hcooper   # needed to keep knife happy
cd /home/hcooper/chef-repo  # your kniife directory
/usr/bin/knife exec scripts/knife_status.rb
