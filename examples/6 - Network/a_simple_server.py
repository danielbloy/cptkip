#
# This example uses biplane to run a simple server that can respond to a
# single route.
#
import time

import cptkip.core.logging as log
from cptkip.network.biplane import Server, Response
from cptkip.task import memory_monitor_task
from network import server_task

log.set_log_level(log.INFO)

server = Server()


@server.route("/", "GET")
def main(query_parameters, headers, body):
    return Response("<b>Hello, world!</b>", content_type="text/html")


monitor_task = memory_monitor_task.create(4, 1, lambda: True)
listen_task = server_task.create(server, lambda: True)

finish = time.monotonic() + 120

while time.monotonic() < finish:
    _ = listen_task()
    _ = monitor_task()
