def execute():
    import validate.utils as utils
    from cptkip.task.triggered_events_task import create, Trigger

    begin_count: int = 0
    values = []
    end_count: int = 0

    # Executed once at the beginning of the trigger.
    def begin() -> None:
        nonlocal begin_count
        begin_count += 1

    # Executed for the events
    def fallback(value) -> None:
        values.append(f"Fallback .... : {value}")

    def callback_a(value) -> None:
        values.append(f"Callback A .. : {value}")

    def callback_b(value) -> None:
        values.append(f"Callback B .. : {value}")

    # Executed once at the end of the trigger.
    def end() -> None:
        nonlocal end_count
        end_count += 1

    trigger = Trigger(True)
    task = create(
        trigger,
        events=[
            (0.0, "1", callback_a),
            (0.2, "2"),
            (0.8, "3", callback_b),
            (1.5, "4", callback_a),
            (2.0, "5")
        ],
        begin=begin,
        callback=fallback,
        end=end,
        continue_func=utils.continue_func)

    utils.execute(task)

    assert begin_count == 1
    assert values == [
        "Callback A .. : 1",
        "Fallback .... : 2",
        "Callback B .. : 3",
        "Callback A .. : 4",
        "Fallback .... : 5",
    ]
    assert end_count == 1


if __name__ == '__main__':
    execute()
