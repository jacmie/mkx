# MKX Testing Guide

## Setup

Install test dependencies from the tests directory:

```bash
cd tests
pip install -r requirements-test.txt
```

## Running Tests

Run tests from the **tests** directory:
```bash
cd tests
```

### Run all tests
```bash
pytest
```

### Run specific test file
```bash
pytest test_keys_standard.py -v
```

### Run with markers
```bash
pytest -m unit          # Run only unit tests
pytest -m integration   # Run only integration tests
```

## Test Structure

### Unit Tests
- `test_keys_standard.py` - Standard key press/release behavior
- `test_manager_layers.py` - Layer activation, deactivation, toggling
- `test_keys_holdtap.py` - Hold-tap key timing logic
- `test_matrix_scanner.py` - Matrix initialization and configuration

### Integration Tests
- `test_integration_keys_layers.py` - Keys working with layer manager

### Fixtures (conftest.py)
- `mock_keyboard` - Mock HID keyboard for testing key output
- `mock_pin` - Mock GPIO pins
- `mock_pins_5x5` - Pre-configured 5x5 matrix pins
- `layer_manager` - Pre-configured layer manager instance

## Mocking Strategy

The test suite uses comprehensive mocking to avoid hardware dependencies:

1. **CircuitPython Libraries** - Adafruit HID, keypad, and digitalio are mocked
2. **Hardware Pins** - GPIO pins are replaced with MagicMock objects
3. **Keyboard Device** - MockKeyboard tracks press/release events

This allows testing the entire library on a desktop without CircuitPython or hardware.

## Code Quality

### Linting
```bash
flake8 mkx/
pylint mkx/
```

### Type checking
```bash
mypy mkx/ --ignore-missing-imports
```

## Coverage Report

To generate a coverage report:
```bash
coverage run -m pytest
coverage report -m
```

This will show which lines are covered/uncovered by tests. 

## Adding New Tests

1. Create test file in `tests/` with name `test_*.py`
2. Use pytest fixtures from `conftest.py`
3. Follow naming convention: `TestClassName` for classes, `test_function_name` for functions
4. Add docstrings explaining test purpose

Example:
```python
def test_new_feature(mock_keyboard, layer_manager):
    """Describe what this test does"""
    # Arrange
    key = KeysStandard(MockKeycode.A, "A")
    
    # Act
    key.press(layer_manager, mock_keyboard, 0)
    
    # Assert
    assert MockKeycode.A in mock_keyboard.pressed_keys
```
