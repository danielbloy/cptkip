import validate.network.client as client
import validate.network.server as server

import validate.utils as utils

modules = [client, server]

if __name__ == '__main__':
    try:
        import wifi

        utils.execute_modules(modules)
    except ImportError:
        print("WiFi not available")
