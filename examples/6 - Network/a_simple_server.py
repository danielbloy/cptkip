#
# This example uses biplane to run a simple server that can respond to a
# single route to display "Hello, world!".
#

import cptkip.core.logging as log
from cptkip.core.environment import is_running_under_test
from cptkip.network.biplane import Server, Response
from cptkip.zero.run import run_for

log.set_log_level(log.INFO)

server = Server()


@server.route("/", "GET")
def main(query_parameters, headers, body):
    return Response("<b>Hello, world!</b>", content_type="text/html")


listen = server.create_task(lambda: True)

run_for(10 if is_running_under_test() else 60, listen)
