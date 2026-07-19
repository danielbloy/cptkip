def execute_next_script(current_script: str | None = None):
    """
    Executes the next script based on the script that has just run.
    If no script is specified then the first script is executed.
    """
    import supervisor
    scripts = [
        "/validate/performance/a_platform.py",
        "/validate/performance/b_environment.py",
        "/validate/performance/c_logging_adafruit.py",
        "/validate/performance/c_logging_cptkip.py",
        "/validate/performance/d_memory.py",
        "/validate/performance/e_configuration.py",
        "/validate/performance/f_cpu.py",
        "/validate/performance/g_adafruit_asyncio.py",
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
