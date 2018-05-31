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

With a 1 minute interval setting & 5MB dictionary file a single forwarder will generated approximatley 25-30GB of ingest per day.

Once deployed & provided with a dictionary & updated outputs file the script will generate load automatically 
