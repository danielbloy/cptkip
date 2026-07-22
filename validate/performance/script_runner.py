def execute_next_script(current_script: str | None = None):
    """
    Executes the next script based on the script that has just run.
    If no script is specified then the first script is executed.
    """
    # noinspection PyUnresolvedReferences
    import supervisor
    scripts = [
        "/validate/performance/a_start.py",
        "/validate/performance/b_environment.py",
        "/validate/performance/c_logging_adafruit.py",
        "/validate/performance/c_logging_cptkip.py",
        "/validate/performance/d_memory.py",
        "/validate/performance/e_configuration.py",
        "/validate/performance/f_cpu.py",
        "/validate/performance/g_adafruit_asyncio.py",
        "/validate/performance/h_basic_runner.py",
        "/validate/performance/h_basic_runner_async.py",
        "/validate/performance/i_periodic_task.py",
        "/validate/performance/i_periodic_task_async.py",
        "/validate/performance/k_output_pin.py",
        "/validate/performance/k_input_pin.py",
        "/validate/performance/k_pwm_pin.py",
        "/validate/performance/k_buzzer_pin.py",
        "/validate/performance/l_button.py",
        "/validate/performance/m_led.py",
        "/validate/performance/m_pixels.py",
        "/validate/performance/n_buzzer.py",
        "/validate/performance/n_melody.py",
        "/validate/performance/n_pwm_audio.py",
        "/validate/performance/o_blink.py",
        "/validate/performance/o_flicker.py",
        "/validate/performance/z_finish.py"
    ]

    index = 0
    if current_script:
        if not current_script in scripts:
            raise Exception(f"script {current_script} does not exist")

        index = scripts.index(current_script)
        index += 1

    supervisor.set_next_code_file(scripts[index])
    supervisor.reload()
