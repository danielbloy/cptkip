from cptkip.core.control import SEND_MESSAGE_TIMEOUT
from cptkip.network.biplane import Server, Response
from cptkip.network.requests import requests


# TODO: Replace this with our own set of routes to be compatible with pico-interactive.

def routes(server: Server):
    @server.route("/hi", "GET")
    def main(query_parameters, headers, body):
        return Response("<b>hi!</b>", content_type="text/html")


HEADER_NAME = 'name'  # Name of the sender.
HEADER_ROLE = 'role'  # Role of the sender.

HEADERS = {
    HEADER_NAME: "configuration.NODE_NAME",  # TODO: This should come from configuration
    HEADER_ROLE: "configuration.NODE_ROLE",  # TODO: This should come from configuration
}


def send_message(path: str, host: str,
                 protocol: str = "http", method="GET",
                 data=None, json=None):
    """
    Sends a message with the provided payload to the specified node, ensuring headers are included.
    """
    return requests.request(method, f"{protocol}://{host}/{path}",
                            headers=HEADERS, data=data, json=json,
                            timeout=SEND_MESSAGE_TIMEOUT)
