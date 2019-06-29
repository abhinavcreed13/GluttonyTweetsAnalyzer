## SDS Ansible Script Deployment

### Overview

In computing, Ansible is an open-source software provisioning, configuration management, and application deployment tool. It runs on many Unix-like systems, and can configure both Unix-like systems as well as Microsoft Windows. It includes its own declarative language to describe system configuration.

Our aim is to deploy our entire application with its dependencies and infrastructure using **single executable script.**

### Prerequisities

- Ansible
- Linux Terminal
- Openstack cloud (Nectar)

### Installation

**Ansible** (Ubuntu/MacOS):

`$ sudo easy_install pip`

`$ sudo pip install ansible`

### Execution

The execution of deployment script starts with this command:

`cd sds-ansible`

`sh exec-sds-ansible.sh`

### Package Overview 

Using this ansible package, we can deploy application with all its the dependencies and required infrastructure. It follows a serial execution flow to deploy all functionalities.

#### **1. Infrastructure**:

- **sds-infra**: This ansible package is used to deploy all the required infrastructure related aspects of the application. This package use `sds-infra-vars.yaml` script to provide configuration for the below roles:
    
    1. **sds-infra-common**: This role will install required common dependencies for building infrastructure:
        
        - python-pip
        - openstacksdk
        
    2. **sds-infra-volume**: This role will create volumes on the cloud as per the names provided and map their ids with name in a dictionary.
    3. **sds-infra-security-group**: This role will create required security groups with their rules on the cloud.
    4. **sds-infra-instances**: This role will create required VM instances and map above created volumes and security groups with their respective instances.

#### **2. Dependencies**:    
 
- **sds-dependencies**: This ansible package is used to install all the required dependencies on the virtual machines created by `sds-infra` package. This package use `sds-deps-vars.yaml` script to provide configuration for the below roles:
    
    **Note:** `sds-infra` dynamically create `hosts` file which contains all the ipv4 addresses of the created VM hosts on which dependencies are required to be installed. This file is then transferred to `sds-dependencies` package by the main control script: `exec-sds-ansible.sh`
    
    1. **sds-deps-common**: This role will install basic dependencies which is required by the application on the newly created VM hosts.
    
    2. **sds-deps-mount-volumes**: This role will format the volumes to `ext4` filesystem on the VMs and mount them on the location as provided using configuration.
    
    3. **sds-deps-install-docker**: This role will install docker on all the provided host VMs by setting proper repositories for downloading and installing docker.
    
    4. **sds-deps-install-couchdb**: This role will install CouchDB 2.0 on all the host VMs provided, by configuring and building it from the source and installing it on external mounted storage.
    
 - **sds-couch-nodes-cluster**: This ansible package will enable CouchDB cluster on all the couchdb nodes installed by the previous package. This package uses `curl` commands to register nodes in the cluster and starting cluster after proper setup.
 
    This package depends on 2 dynamically created files by `sds-infra` package:
    
    - **hosts_couch:** This file is created by `sds-infra` so as to decide the node which would be responsible for performing handshakes and completing CouchDB cluster setup. Hence, only 1 host is added in this file on which `sds-couch-nodes-cluster` executes.
    
    - **sds-couch-dynamic-vars.yaml**: This file is also created by `sds-infra` so as to decide all the other nodes which would participate in the CouchDB cluster. These nodes will be registered in the cluster by the host provided in the `hosts-couch` file.
    
   Both of these files are transferred to their proper locations by the main control script: `exec-sds-ansible.sh`
   
   This package provides configuration to the below role using dynamically created file: `sds-couch-dynamic-vars.yaml`
   
   - **sds-deploy-couch-cluster**: This role will enable CouchDB cluster using the host provided in `hosts_couch` file and registering all other nodes in the cluster as per the dynamic configuration.
   
### **3. Application**:

**sds-application:** This ansible package is used to deploy and install the application with
harvester on the virtual machines created by sds-infra package. Before starting roles of
this package, we use custom created script - `create_package.sh` - which transforms our
entire project into .tar.gz file and copy package into required location, which can later
be deployed and extracted in VMs using following roles:

**-sds-deploy-app:** This role will create the project directory in all provided VMs,
deploy .tar.gz package and unarchive it using ansible commands.
-sds-run-harvester: This role starts the harvester by building docker image and
starting container. Before building image, it uses ansible regexp
for pointing harvester’s configuration to correct couchdb.

**-sds-run-app:** This role starts the application python flask server which exposes
API endpoints for UI interactions and manipulations. It is also started by building
docker image and starting container. Similar to above regexp
code, application data connector configuration is also pointed to correct couch db.  
 
    
     



