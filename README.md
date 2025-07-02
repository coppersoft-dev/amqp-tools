# AMQP Tools

This repository hosts some tools we use for debugging, testing and playing with AMQP brokers. Currently these are mainly used for interacting with [ECCo SP](https://www.entsoe.eu/ecco-sp/) brokers.

## List of Tools

### proton_consumer.py

Connects to the internal ECP broker at the given address:port tuple and consumes messages from the given queue, writing each message's body to disk.

In the following example invocation the AMQP password is read interactively and then the script connects to the IP address 10.2.2.8 at the (default) port 5672, authenticating as user `endpoint` and consuming messages from the queue `ecp.endpoint.inbox`, writing each message to the directory `ep2_inbox/`:

```sh
$ read -p "Enter AMQP user password: " -r AMQP_PASSWORD && export AMQP_PASSWORD
$ python proton_consumer.py -a 10.2.2.8 -q ecp.endpoint.inbox -u endpoint -d ep2_inbox/
```

Use the `-h/--help` flag for a more in-depth documentation of the available flags:

```sh
$ python proton_consumer.py --help
usage: proton_consumer.py [-h] [-a ADDRESS] [-p PORT] [-q QUEUE] [-u USER] [-d DIRECTORY]

ECP AMQP consumer

options:
  -h, --help            show this help message and exit
  -a, --address ADDRESS
                        IP address to connect to
  -p, --port PORT       TCP port to connect to
  -q, --queue QUEUE     Queue to consume from broker
  -u, --user USER       Username used for authentication (password to be provided via AMQP_PASSWORD environment variable)
  -d, --directory DIRECTORY
                        Path of directory to write messages to. If empty, the current directory will be used.
```

### proton_sender.py

Connects to the internal ECP broker at the given address:port tuple and sends the given file to the given recipient.

In the following example invocation the script connects to the broker at 10.2.2.12 and sends the file `/tmp/2MiB.dat` to the ECP endpoint identified by the component code `ep2`:

```sh
$ python proton_sender.py -a 10.2.2.12 -r ep2 -f /tmp/2MiB.dat
```

Use the `-h/--help` flag for a more in-depth documentation of the available flags:

```sh
$ python proton_sender.py -h
usage: proton_sender.py [-h] [-a ADDRESS] [-p PORT] [-q QUEUE] [-r RECEIVER_CODE] [-f FILE]

ECP AMQP consumer

options:
  -h, --help            show this help message and exit
  -a, --address ADDRESS
                        IP address to connect to
  -p, --port PORT       TCP port to connect to
  -q, --queue QUEUE     Queue to consume from broker
  -r, --receiver-code RECEIVER_CODE
                        ECP endpoint code of the receiver
  -f, --file FILE       file to read message body from
```
