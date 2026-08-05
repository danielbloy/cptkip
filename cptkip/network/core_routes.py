from cptkip.network.biplane import Server, Response


# TODO: Replace this with our own set of routes to be compatible with pico-interactive.

def routes(server: Server):
    @server.route("/hi", "GET")
    def main(query_parameters, headers, body):
        return Response("<b>hi!</b>", content_type="text/html")
