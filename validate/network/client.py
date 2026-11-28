def execute():
    import validate.utils as utils
    from cptkip.core.environment import is_running_in_ci, is_running_on_microcontroller

    if is_running_on_microcontroller():
        try:
            import wifi  # noqa: F401
        except ImportError:
            raise utils.Skip("WiFi is not available on this device")

    # Don't make requests to an external service from CI: it makes the build depend
    # on that service being up. (The local server is validated by server.py.)
    utils.skip_unless(not is_running_in_ci(), "external HTTP requests are not made in CI")

    from cptkip.network.requests import requests
    from cptkip.task.periodic_task import create

    responses = []

    def request():
        with requests.request("GET", "https://httpbin.org/get") as response:
            print(f"Status ..... : {response.status_code}")
            print(f"Reason ..... : {response.reason}")
            if response.status_code == 200:
                print(f"Text ....... : {response.json()}")
            responses.append(response.status_code)

    # One request per second rather than as many as possible: this validates the
    # requests wrapper without hammering a public service.
    utils.execute(create(request, frequency=1, continue_func=utils.continue_func))

    assert responses, "no requests were made"
    assert 200 in responses, f"no successful responses: {responses}"


if __name__ == '__main__':
    execute()
