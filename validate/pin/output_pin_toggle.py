def execute():
    from time import monotonic
    import validate.utils as utils
    import cptkip.config.configuration as config
    import cptkip.pin.output_pin as output_pin

    utils.require_pins(config.LED_PIN)

    # Uses toggle() rather than setting value; the LED flashes and the returned
    # state must alternate.
    with output_pin.OutputPin(config.LED_PIN, invert=config.LED_INVERT) as pin:
        states = []
        next_change = monotonic()

        def task():
            nonlocal next_change
            if monotonic() >= next_change:
                next_change += 0.25
                states.append(pin.toggle())

        print("LED will flash using toggle()")
        utils.execute(task)
        pin.off()

        assert len(states) > 4
        assert all(states[i] != states[i + 1] for i in range(len(states) - 1))


if __name__ == '__main__':
    execute()
