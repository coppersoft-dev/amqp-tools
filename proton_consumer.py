import argparse
import json
import os
import sys
from proton import SSLDomain
from proton.handlers import MessagingHandler
from proton.reactor import Container


class HelloWorld(MessagingHandler):
    def __init__(self, server, address, user, passwd, outdir):
        super(HelloWorld, self).__init__()
        self.server = server
        self.address = address
        self.auth_user = user
        self.auth_pass = passwd
        self.outdir = outdir

    def on_start(self, event):
        ssl = SSLDomain(mode=SSLDomain.MODE_CLIENT)
        # ssl.set_trusted_ca_db(certificate_db="/Users/max/dev/associmates/amprion-rgce-ecp/ca/prod/ca-bundle.crt")
        ssl.set_peer_authentication(SSLDomain.ANONYMOUS_PEER)
        # ssl.set_credentials(cert_file="/Users/max/dev/associmates/ecp-prod-network/ecp-ep2/cert.pem",
        #                     key_file="/Users/max/dev/associmates/ecp-prod-network/ecp-ep2/privkey.pem",
        #                     password=None)
        conn = event.container.connect(self.server,
                                       ssl_domain=ssl,
                                       user=self.auth_user,
                                       password=self.auth_pass,
                                       allow_insecure_mechs=True,
                                       sasl_enabled=True)
        event.container.create_receiver(conn, self.address)
        event.container.create_sender

    def on_message(self, event):
        print(json.dumps(event.message.properties))
        if "messageID" in event.message.properties:
            mid = event.message.properties["messageID"]
        elif "errorID" in event.message.properties:
            mid = event.message.properties["errorID"]
        with open(f'{self.outdir}/{mid}.dat', mode="ba") as f:
            body = event.message.body
            if isinstance(body, str):
                body = body.encode('UTF-8')
            f.write(body)


queue = "ecp.endpoint.inbox"

parser = argparse.ArgumentParser(description="ECP AMQP consumer")
parser.add_argument("-a", "--address", default="127.0.0.1", help="IP address to connect to")
parser.add_argument("-p", "--port", default="5672", help="TCP port to connect to")
parser.add_argument("-q", "--queue", default="ecp.endpoint.inbox", help="Queue to consume from broker")
parser.add_argument("-u", "--user", default="", help="Username used for authentication (password to be provided via AMQP_PASSWORD environment variable)")
parser.add_argument("-d", "--directory", default="", help="Path of directory to write messages to. If empty, the current directory will be used.")
args = parser.parse_args()

passwd = os.environ.get("AMQP_PASSWORD")

if len(sys.argv) >= 2:
    queue = sys.argv[1]
Container(HelloWorld(f"amqps://{args.address}:{args.port}", args.queue, args.user, passwd, args.directory)).run()
