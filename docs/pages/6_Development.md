@page p_6 6 Development
@tableofcontents


@section p_6_1 6.1 Code rules
- keep files structure flat
- place the library on board in the default **CIRCUITPYTHON/lib** directory

To add functionality, inherit from the **Abstract** classes if possible, and use them like the already implemented functions and keys.  

@section p_6_2 6.2 Build Binary MKX Library

Install *Adafruit* **mpy-cross** *for CircuitPython*, see @ref p_2
Use the **build** tool from the **MKX** repository:

```
usage: build.py [-h] [-d DRIVE] [--compile] [--upload] [--clean] [--tidy]

Compile/upload mkx to a CIRCUITPY device.

options:
  -h, --help            show this help message and exit
  -d DRIVE, --drive DRIVE
                        Name of the mounted drive (default: CIRCUITPY) or full mount path
  --compile             Compile .py files to .mpy (use with --upload to compile before upload)
  --upload              Upload compiled .mpy files to the drive (does not compile unless --compile given)
  --clean               Remove compiled files (.compiled)
  --tidy                Removing all content from the mkx dir on the MCU mountpoint
```

@section p_6_3 6.3 Synchronize Github repository with the CIRCUITPY drive

Install **watchdog** tool, see @ref p_2
Use the **auto_sync** tool from the **MKX** repository:

```
usage: auto_sync.py [-h] [-d DRIVE] [--diff] [--Vdiff] [--build] [--clean] [--tidy]

Sync mkx local files to a CIRCUITPY device.

options:
  -h, --help            show this help message and exit
  -d DRIVE, --drive DRIVE
                        Name of the mounted drive (default: CIRCUITPY)
  --diff                Which files are different and should be updated.
  --Vdiff               Verbose differences between files.
  --build               Build .mpy binaries using build.py and upload instead of .py files.
  --clean               Remove compiled files (.compiled directory).
  --tidy                Remove all uploaded content from the MCU mountpoint.
```

@section p_6_4 6.4 Testing

Before deploying to hardware, use the included test suite to verify functionality.

Install testing tools see @ref p_2_5_3

@subsection p_6_4_1 6.4.1 Run Tests

From the **tests** directory, run the test suite:

```
cd tests
pytest -v
```

To see which features are being tested:

```
pytest -v --collect-only
```

@subsection p_6_4_2 6.4.2 Code Coverage

Check code coverage to identify untested functionality:

```
coverage run -m pytest
coverage report -m
```

This shows a detailed coverage report for each file.

@subsection p_6_4_3 6.4.3 Write New Tests

Tests are located in the **tests** directory. Use existing test files as templates:

- `test_keys_standard.py` - Example: testing basic key press/release
- `test_manager_layers.py` - Example: testing layer management
- `test_keys_holdtap.py` - Example: testing timing logic
- `test_custom_key_template.py` - Template for creating new tests

Key points for writing tests:

1. Use the provided pytest fixtures from `conftest.py`:
   - `mock_keyboard` - Simulated keyboard for tracking key events
   - `mock_digitalio` - Simulated GPIO pins
   - `layer_manager` - Pre-configured layer manager
   - `timed_key_tracker` - For testing time-dependent keys

2. Tests mock all CircuitPython hardware dependencies, so tests run on desktop without hardware

3. Follow naming convention: `test_*.py` files with `test_*()` functions

Example test:

```python
def test_my_feature(mock_keyboard, layer_manager):
    """Test my feature with mocked hardware."""
    # Your test code here
    assert mock_keyboard.press_count >= 1
```

@section p_6_5 6.5 Build HTML docs

The documentation is build with Doxygen:  
https://www.doxygen.nl/

From the **docs** directory, run:
```
doxygen ./Doxyfile
```
Open the documentation **docs/html/index.html**  

If you update the content of the documentation run **doxygen** again.  
Don't close the browser, just refresh the documentation page - **F5**.

