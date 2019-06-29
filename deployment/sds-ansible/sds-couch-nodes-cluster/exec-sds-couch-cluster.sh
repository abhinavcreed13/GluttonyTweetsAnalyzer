#!/usr/bin/env bash
#
# Team 13, Melbourne
# Abhinav Sharma, 1009225
# Benjamin Frengley, 1050642
# Kabir Manandhar Shrestha, 1059431
# Rohit Kumar Gupta, 1023418
# Jan Knížek, 1052305
#

. ./openrc.sh; ansible-playbook -i hosts_couch -u ubuntu --key-file=cloud.key --ask-become-pass sds-couch-nodes-cluster.yaml
