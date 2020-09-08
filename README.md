*This application/script is provided at your own risk & is not a Splunk supported product. It is only meant for testing & is considered experimental*

**IF YOU CHOOSE TO DOWNLOAD THE ZIP FORMAT PLEASE NAME THE FILE FROM hipster-master TO hipster FOR THE SCRIPTS TO WORK CORRECTLY**

# hipster
A linux-based python based event generator with Splunk compatible data

Hipster is meant to be installed as a Splunk app on a forwarder with the $SPLUNK_HOME/etc/apps directory.

It is comprised of the following files:

- bin/hip.py - core python script that generates the load to be sent to Splunk for ingest

- default/dict - dictionary file that hipster uses to generated load. It is random text generated from base64 /dev/urandom input and makese the events for Splunk to index. Set to 5MB as default.

- default/inputs.conf - Scripted input that defines the interval (1m), index=junk & source/sourcetype=hipster

- default/load.conf - defines the load factor - keep this at 1.5x the others settings are experimental

- default/limits.conf - increases the thrupt to allow more data outbound (maxKBps=1024)

- deafult/outputs.conf - output destination - should be changed to match your environment

Hipster will create time-based data for Splunk to ingest and is meant only to generate load on a system for IO/indexing purposes. The data has no value and is completely random junk. 

In fact the inputs.conf will put the data into an index called junk by default so that data can easily be cleared from the system to run new tests & be captured by Splunk licensing for easier measurement.

This provided file will create about 20GB/day from a single forwarder with the interval set at 30s

Once deployed & provided with a dictionary & updated outputs file the script will generate load automatically 

To scale out a hipster test to more nodes I suggest the following procedure to deploy multiple forwarders within a Kubernetes deployment

**Hipster Multiple UF Load Generation Steps**

Host suggestion: m5.xlarge+ for 75 nodes and greater and I run this on Ubuntu 20.04

Setup the Kubes Cluster & configue with DNS/Storage support and configure the following

- sudo snap install microk8s --classic --channel=1.18/stable
- sudo usermod -a -G microk8s <username>
- sudo chown -f -R <username> ~/.kube
- sudo snap alias microk8s.kubectl kubectl

Log-off and then run these additional configurations for the cluster

- microk8s enable dns
- microk8s enable storage

This will setup the basic kubes cluster with enough network and storage to get started

In this case since we are using a hostPath configuration to share the directory /apps with each container we deploy in the /opt/splunkforwarder/apps directory so that apps can be mapped directly we need to take the following additional steps

sudo mkdir /apps
cd /apps
sudo wget https://codeload.github.com/klawrencegupta-splunk/hipster/zip/master
sudo mv master master.zip; sudo unzip master.zip; sudo mv hipster-master/ hipster


Once the /apps directory is staged and has your apps deployed we can deploy the follwowing yaml as a kubes Deployment by using the hipster.yaml file provided

kubectl apply -f hipster.yaml

To configure Hipster for load you need to modify 3 files

- dict is the sample of data you want to send - dict.dict is given as a neutral sample of simple apache data for testing
- inputs.conf will control the interval as which you want that dict file to be read - the default is 10 seconds
- outputs.conf will need to contain the IPs of the indexers you want to send data

# The formula to determine the amount of load you want to generate is:
    (number of hipster containers	* run intervals per day	* size dictionary in kb)/1024/1024 = Total GB/day load for all hipster containers
    - example: 75 hipster nodes x 1440 (or 60 second intervals) x 1000k sized dict = ~105GB of daily load
    


