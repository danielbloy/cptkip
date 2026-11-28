import validate.device.audio_queue_controls as audio_queue_controls
import validate.device.button as button
import validate.device.buzzer as buzzer
import validate.device.buzzer_beeps as buzzer_beeps
import validate.device.i2s_audio as i2s_audio
import validate.device.led as led
import validate.device.melody as melody
import validate.device.melody_controls as melody_controls
import validate.device.pixels as pixels
import validate.device.pwm_audio as pwm_audio
import validate.utils as utils

modules = [button, led, pixels, buzzer, buzzer_beeps, melody, melody_controls, pwm_audio, i2s_audio,
           audio_queue_controls]

if __name__ == '__main__':
    utils.exit_on_failure(utils.execute_modules(modules))
