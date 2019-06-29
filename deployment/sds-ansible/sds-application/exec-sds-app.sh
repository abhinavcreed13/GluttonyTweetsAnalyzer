#!/usr/bin/env bash

. ./openrc.sh; ansible-playbook -i hosts -u ubuntu --key-file=cloud.key --ask-become-pass sds-app.yaml
