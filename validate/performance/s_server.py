try:
    import wifi
except ImportError:
    print("WiFi not available, skipping script")
    from validate.performance.script_runner import execute_next_script

    execute_next_script(__file__)

from cptkip.network.biplane import Server, Response
from validate.performance.task_runner import execute

server = Server()


@server.route("/", "GET")
def main(query_parameters, headers, body):
    return Response("<b>Hello, world!</b>", content_type="text/html")


listen = server.create_task(lambda: True)
listen()
execute(listen, False)
execute(listen, True)

# Load the next file
from validate.performance.script_runner import execute_next_script

execute_next_script(__file__)
