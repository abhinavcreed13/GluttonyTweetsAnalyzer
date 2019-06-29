#!/bin/bash
#
# Team 13, Melbourne
# Abhinav Sharma, 1009225
# Benjamin Frengley, 1050642
# Kabir Manandhar Shrestha, 1059431
# Rohit Kumar Gupta, 1023418
# Jan Knížek, 1052305
#

echo "##### Removing old packages #####"
if [ -f "./package/projectsds-1.0.0.tar.gz" ]; then rm -r ./package/projectsds-1.0.0.tar.gz; fi
if [ -f "./deployment/sds-ansible/sds-application/roles/sds-deploy-app/package/projectsds-1.0.0.tar.gz" ]; then rm -r ./deployment/sds-ansible/sds-application/roles/sds-deploy-app/package/projectsds-1.0.0.tar.gz; fi

echo "##### Creating Package #####"
tar --exclude='./deployment' --exclude='./package' --exclude='./venv' --exclude='./.git' --exclude='./.idea' -zcvf ./package/projectsds-1.0.0.tar.gz .

echo "##### Pushing to Deployment #####"
cp -rf ./package/projectsds-1.0.0.tar.gz ./deployment/sds-ansible/sds-application/roles/sds-deploy-app/package

echo "##### DONE #####"
