# Validating on a device

The validation scripts are designed to be run on a CircuitPython device to
validate both the correctness of CPTKIP but also validate overall performance.
The validation tests require a human to check the results so have some
interactivity. There is also a `validate_all.py` script which runs all tests.

The following steps are required to be followed to run the validation
on a CircuitPython device.

1. Copy the entire `cptkip` directory to the root of the device.
2. Copy the entire `validate` directory in the root of the device.
3. Create a `lib` directory in the root of the device.
4. Copy the `config.py` file from the root of `cptkip` to the root of your device. 
5. Copy across the contents of `CircuitPython/<version>/lib` into the `lib`
   directory on the device for your version of CircuitPython.
6. Use Thonny to run one of the validate scripts such as`validate_performance.py`.
