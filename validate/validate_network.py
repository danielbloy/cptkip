import validate.network.client as client
import validate.network.server as server

import validate.utils as utils

modules = [client, server]

if __name__ == '__main__':
    # Each module skips itself when WiFi is unavailable (on a device) or, for the
    # external client requests, when running in CI.
    utils.exit_on_failure(utils.execute_modules(modules))
