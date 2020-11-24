# broker
Simple Python Broker made with Paho MQTT and PyQt5.

## info
I developed this Broker in order to test an App for an Iot Project I'm doing fro my home. 
It emulates Amazon AWS Iot Core behaviour. 
The programs can store a simple Shadow, and give that Shadow to a MQTT client who request it.

## Use
To get a Shadow publish a dummy payload to the /get topic and listen to the /publish topic to receive it.
To update the Shadow Publish the new shadow to the /update topic.




