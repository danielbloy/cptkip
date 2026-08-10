def execute():
    from cptkip.network.biplane import Server, Response
    import validate.utils as utils

    server = Server()

    @server.route("/", "GET")
    def main(query_parameters, headers, body):
        return Response("<b>Hello, world!</b>", content_type="text/html")

    listen = server.create_task(lambda: True)
    utils.execute(listen)


if __name__ == '__main__':
    execute()
