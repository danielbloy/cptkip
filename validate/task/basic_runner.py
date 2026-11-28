def execute():
    from time import monotonic
    import validate.utils as utils

    # There is nothing much to do because utils.execute() uses basic_runner to
    # execute the task. This will run forever if the cancellation does not work,
    # so also check the runner stopped on time.
    start = monotonic()
    utils.execute(lambda: True)
    elapsed = monotonic() - start
    assert elapsed < utils.RUNTIME + 1, f"runner took {elapsed:.2f}s to stop"


if __name__ == '__main__':
    execute()
