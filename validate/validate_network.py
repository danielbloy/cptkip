import validate.network.client as client
import validate.network.server as server

import validate.utils as utils

modules = [client, server]

if __name__ == '__main__':
    utils.execute_modules(modules)
