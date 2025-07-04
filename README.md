# Installing

Command line:
`python -m pip install git+https://github.com/stellaaanz/vrchat_oscquery.git#egg=vrchat_oscquery`

Adding it to your project via requirements.txt:
`vrchat_oscquery @ git+https://github.com/stellaaanz/vrchat_oscquery@main`


# Simple proxy usage
If you just want to run multiple OSC programs at the same time, this library includes a setup script that will register multiple apps with VRChat on specified OSC ports.

For example, the config file 
```
{
  "App 1": 12345,
  "App 2": 2000
}
```
Will tell VRChat an app named "App 1" is listening for OSC messages on port 12345, an "App 2" is listening on port 2000. Once VRChat is aware of these, the program will shut down.

To run (which will generate a config.json if necessary): `python -m vrchat_oscquery`

# VRChat OSCQuery Examples
I could not find any simple/understandable examples of OSCQuery, nor anything
vrchat specific. There exist some examples of OSCQuery, and figuring out how to
make them work with VRC took a few days.

To save others time I have packaged up this into a library that lets you easily
create VRChat OSC applications that can work simultaneously. Normally multiple
OSC apps will fight over who gets to listen on port 9001.

# Examples:

There are 4 examples, Foreground/Background versions of asyncio and threading.

Each example implements an application that shows reading and writing. 

1. Read from the users 'MuteSelf' setting (/avatar/parameters/MuteSelf)
2. Then write to VRChat osc input (/chatbox/input).

# More technical details (VRChat OSCQuery requirements TLDR):

## High level systems:

1. An OSC server is setup on some arbitrary port (udp).

2. A web server is setup on another arbitrary port (tcp).

  * Note: This can be (and in this library is) the same port as the OSC server

3. Using zeroconf, we announce the web server.

4. The web server provides where to send OSC data, and which OSC paths to send.

## More specifics

### Web server:

#### Protocol
The web server technically should implement a much more complicated protocol 
[OSCQuery spec](https://github.com/Vidvox/OSCQueryProposal). But that's not
necessary currently, VRChat only sends 2 GET requests :

* "/"
  * This is responsible for providing the OSC paths
  * An example that pulls all data:
```json
"CONTENTS": {
  "avatar": {"FULL_PATH": "/avatar"},
  "tracking": {"FULL_PATH": "/tracking"},
}
```
* "/?HOST_INFO"
  * This is responsible for providing the OSC port
  * An example that points VRChat to port 12345:
```json
{"OSC_PORT": 12345}
```

### ZeroConf

#### Service Info

ZeroConf/Bonjour services announce themselves using MDNS.

These services include a type, name, address, port:

* Type: `_oscjson._tcp.local.`
* Name: A string that ends with `._oscjson._tcp.local.`
  * Seems like a period is the only thing that's not allowed. I even used emojis successfully!
* Address: The IP Address of the http server mentioned above.
* Port: The Port of the http server mentioned above.

Several services can announce they provide the same type of data, this is how VRChat can find multiple OSC applications.


# Some questions I still have:

1. Can you provide a `OSC_IP` value in the HOST_INFO response?
  * Seemingly no. It just ignored it and send to 127.0.0.1
2. Can you use non-127.0.0.1 anywhere/everywhere?
4. Can you use whole external host names. (i.e. can I host a service on snail.rocks that other people can hook up via osc?)

