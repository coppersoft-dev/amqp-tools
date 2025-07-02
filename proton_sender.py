import argparse
import sys
import time
import uuid
from proton import SSLDomain, Message
from proton.handlers import MessagingHandler
from proton.reactor import Container


class Sender(MessagingHandler):
    def __init__(self, server, address, receiver, message):
        super(Sender, self).__init__()
        self.server = server
        self.address = address
        self.message = message
        self.receiver = receiver

    def on_start(self, event):
        ssl = SSLDomain(mode=SSLDomain.MODE_CLIENT)
        # ssl.set_trusted_ca_db(certificate_db="/Users/max/dev/associmates/amprion-rgce-ecp/ca/prod/ca-bundle.crt")
        ssl.set_peer_authentication(SSLDomain.ANONYMOUS_PEER)
        # ssl.set_credentials(cert_file="/Users/max/dev/associmates/ecp-prod-network/ecp-ep2/cert.pem",
        #                     key_file="/Users/max/dev/associmates/ecp-prod-network/ecp-ep2/privkey.pem",
        #                     password=None)
        conn = event.container.connect(self.server,
                                       ssl_domain=ssl,
                                       user="endpoint",
                                       password="password",
                                       allow_insecure_mechs=True,
                                       sasl_enabled=True)
        event.container.create_sender(conn, self.address)

    def on_sendable(self, event):
        with open(self.message, 'rb') as file:
            msg_body = file.read()
        corid = str(uuid.uuid4())
        msg = Message(body=msg_body, properties={
            "messageType": "zotzen",
            "receiverCode": self.receiver,
            "baMessageID": corid,
        },
            creation_time=int(time.time()),
        )
        msg.correlation_id = corid
        event.sender.send(msg)
        event.sender.close()
        event.connection.close()
        print(msg.correlation_id)


parser = argparse.ArgumentParser(description="ECP AMQP consumer")
parser.add_argument("-a", "--address", default="127.0.0.1",
                    help="IP address to connect to")
parser.add_argument("-p", "--port", default="5672",
                    help="TCP port to connect to")
parser.add_argument("-q", "--queue", default="ecp.endpoint.outbox",
                    help="Queue to consume from broker")
parser.add_argument("-r", "--receiver-code", default="",
                    help="ECP endpoint code of the receiver")
parser.add_argument("-f","--file", default="",
                    help="file to read message body from")
args = parser.parse_args()

if len(sys.argv) >= 2:
    queue = sys.argv[1]
Container(Sender(f"amqps://{args.address}:{args.port}",
          args.queue, args.receiver_code, args.file)).run()
