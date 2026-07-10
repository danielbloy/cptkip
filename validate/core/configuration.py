# NOTE: For the tests in here to pass, the file `validate/config.py` needs to be
#       copied to the root of the CircuitPython drive.

def execute():
    import cptkip.core.logging as log

    # Import the configuration file and validate that the log level is
    # set to what is in the config file which should be INFO (the default
    # level is WARNING).
    #
    # NOTE: The config log level is only loaded once so if a previous script
    #       loads config, that initial loading would set the config. this is
    #       here in case this script is run completely independently.
    import cptkip.config.configuration as config

    # This tests that the logging level is loaded from the config file along with other properties.
    assert config.LOG_LEVEL == log.INFO
    assert config.TEST_VALUE == 123.456
    assert config.TEST_STRING == "Hello world!"
    assert config.DEBUG
    print('VALIDATE : Log level info should be output')
    log.info('Log level info should be output')

    # Debug should not be output.
    log.debug('FAIL FAIL FAIL FAIL FAIL FAIL FAIL FAIL FAIL FAIL FAIL FAIL FAIL FAIL FAIL FAIL FAIL FAIL FAIL FAIL')


if __name__ == '__main__':
    execute()
