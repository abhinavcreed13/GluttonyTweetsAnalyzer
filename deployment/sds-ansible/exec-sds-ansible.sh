#!/bin/bash
#
# Team 13, Melbourne
# Abhinav Sharma, 1009225
# Benjamin Frengley, 1050642
# Kabir Manandhar Shrestha, 1059431
# Rohit Kumar Gupta, 1023418
# Jan Knížek, 1052305
#

echo "#### Copying server files to all Ansible packages ####"
cp -rf static/serverfiles/openrc.sh sds-infra
cp -rf static/serverfiles/* sds-dependencies
cp -rf static/serverfiles/* sds-couch-nodes-cluster
cp -rf static/serverfiles/* sds-application

echo "#### Changing permissions of private key #####"
sudo chmod 600 sds-dependencies/cloud.key
sudo chmod 600 sds-couch-nodes-cluster/cloud.key
sudo chmod 600 sds-application/cloud.key

echo "##### EXEC ANSIBLE SDS INFRA #####"
cd sds-infra
sh exec-sds-infra.sh

echo "##### Moving hosts from Infra to Dependencies & Application #####"
cd ..
cp -rf sds-infra/hosts sds-dependencies
cp -rf sds-infra/hosts sds-application

echo "##### EXEC ANSIBLE SDS DEPENDENCIES #####"
cd sds-dependencies
sh exec-sds-deps.sh

echo "##### Moving files from (Infra + static) to couch nodes cluster deployment #####"
cd ..
cp -rf sds-infra/files/hosts_couch sds-couch-nodes-cluster
cp -rf sds-infra/files/sds-couch-dynamic-vars.yaml sds-couch-nodes-cluster/host_vars
rm -r sds-infra/files/sds-couch-dynamic-vars.yaml
cp -rf static/couchdbviews/common.dataview.json sds-couch-nodes-cluster/roles/sds-deploy-couch-cluster/tasks/couchdbviews
cp -rf static/couchdbviews/sdsdb.storyview.json sds-couch-nodes-cluster/roles/sds-deploy-couch-cluster/tasks/couchdbviews

echo "#### DEPLOY COUCH MULTI-NODE CLUSTER ####"
cd sds-couch-nodes-cluster
sh exec-sds-couch-cluster.sh

echo "#### DEPLOY & RUN APPLICATION ####"
cd ..
cd sds-application
sh exec-sds-app.sh
