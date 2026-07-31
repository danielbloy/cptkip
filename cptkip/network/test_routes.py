import biplane


def routes(server: biplane.Server):
    @server.route("/hi", "GET")
    def main(query_parameters, headers, body):
        return biplane.Response("<b>hi!</b>", content_type="text/html")
