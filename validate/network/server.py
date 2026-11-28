def execute():
    import validate.utils as utils
    from cptkip.core.environment import is_running_on_desktop, is_running_on_microcontroller

    if is_running_on_microcontroller():
        try:
            import wifi  # noqa: F401
        except ImportError:
            raise utils.Skip("WiFi is not available on this device")

    from cptkip.network.biplane import Server, Response, get_host, get_port

    server = Server()

    @server.route("/", "GET")
    def main(query_parameters, headers, body):
        return Response("<b>Hello, world!</b>", content_type="text/html")

    host, port = get_host(), get_port()
    listen = server.create_task(lambda: True, listen_on=(host, port))

    results = []
    if is_running_on_desktop():
        # On a desktop, check the server really answers by requesting from another
        # thread while the server runs on this one. On a device, browse to the
        # device to check it manually (requests would block the single thread).
        from threading import Thread
        from time import sleep

        def client():
            import requests
            sleep(0.5)
            results.append(requests.get(f"http://{host}:{port}/", timeout=2).text)

        Thread(target=client, daemon=True).start()
    else:
        print(f"Browse to http://{host}:{port}/ to check the server responds")

    utils.execute(listen)

    if is_running_on_desktop():
        assert results == ["<b>Hello, world!</b>"], results


if __name__ == '__main__':
    execute()
