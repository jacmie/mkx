"""
Unit tests for matrix scanning functionality.
Tests key matrix detection and event generation.
"""

import pytest
from unittest.mock import MagicMock
from mkx.diode_orientation import DiodeOrientation

# Import the mock digitalio (already set up by conftest.py)
import digitalio


class TestMatrixScanner:
    """Test suite for MatrixScanner"""

    @pytest.fixture
    def mock_scanner_pins(self):
        """Create mock pins for a 2x2 matrix"""
        cols = []
        rows = []

        for i in range(2):
            col = MagicMock()
            col.switch_to_output = MagicMock()
            col.switch_to_input = MagicMock()
            col._value = 0
            col.value = property(
                lambda self: self._value, lambda self, v: setattr(self, "_value", v)
            )
            cols.append(col)

            row = MagicMock()
            row.switch_to_output = MagicMock()
            row.switch_to_input = MagicMock()
            row._value = 0
            row.value = property(
                lambda self: self._value, lambda self, v: setattr(self, "_value", v)
            )
            rows.append(row)

        return cols, rows

    def test_matrix_scanner_initialization(self, mock_scanner_pins):
        """Test MatrixScanner initializes with correct pin setup"""
        cols, rows = mock_scanner_pins

        from mkx.matrix_scanner import MatrixScanner

        scanner = MatrixScanner(
            cols=cols,
            rows=rows,
            diode_orientation=DiodeOrientation.COL2ROW,
            pull=digitalio.Pull.DOWN,
            warmup_cycles=0,
        )

        assert scanner.len_cols == 2
        assert scanner.len_rows == 2
        assert len(scanner.state) == 4  # 2x2 matrix

    def test_matrix_scanner_col2row_orientation(self, mock_scanner_pins):
        """Test COL2ROW diode orientation setup"""
        cols, rows = mock_scanner_pins

        from mkx.matrix_scanner import MatrixScanner

        scanner = MatrixScanner(
            cols=cols,
            rows=rows,
            diode_orientation=DiodeOrientation.COL2ROW,
            pull=digitalio.Pull.DOWN,
            warmup_cycles=0,
        )

        assert scanner.anodes == cols
        assert scanner.cathodes == rows

        # With DOWN pull, columns are drive pins
        assert len(scanner.drive_pins) == 2
        assert len(scanner.sense_pins) == 2

    def test_matrix_scanner_row2col_orientation(self, mock_scanner_pins):
        """Test ROW2COL diode orientation setup"""
        cols, rows = mock_scanner_pins

        from mkx.matrix_scanner import MatrixScanner

        scanner = MatrixScanner(
            cols=cols,
            rows=rows,
            diode_orientation=DiodeOrientation.ROW2COL,
            pull=digitalio.Pull.DOWN,
            warmup_cycles=0,
        )

        assert scanner.anodes == rows
        assert scanner.cathodes == cols

    def test_matrix_scanner_pull_up_configuration(self, mock_scanner_pins):
        """Test PULL.UP configuration"""
        cols, rows = mock_scanner_pins

        from mkx.matrix_scanner import MatrixScanner

        scanner = MatrixScanner(
            cols=cols,
            rows=rows,
            diode_orientation=DiodeOrientation.COL2ROW,
            pull=digitalio.Pull.UP,
            warmup_cycles=0,
        )

        # With UP pull, anodes are drive pins, cathodes are sense pins
        assert len(scanner.drive_pins) == 2
        assert len(scanner.sense_pins) == 2

    def test_matrix_scanner_pull_down_configuration(self, mock_scanner_pins):
        """Test PULL.DOWN configuration"""
        cols, rows = mock_scanner_pins

        from mkx.matrix_scanner import MatrixScanner

        scanner = MatrixScanner(
            cols=cols,
            rows=rows,
            diode_orientation=DiodeOrientation.COL2ROW,
            pull=digitalio.Pull.DOWN,
            warmup_cycles=0,
        )

        # With DOWN pull, cathodes are drive pins, anodes are sense pins
        assert len(scanner.drive_pins) == 2
        assert len(scanner.sense_pins) == 2

    def test_matrix_scanner_pin_overlap_detection(self, mock_scanner_pins):
        """Test that overlapping column and row pins raise error"""
        cols, rows = mock_scanner_pins

        from mkx.matrix_scanner import MatrixScanner

        # Use same pin for col and row
        cols_bad = cols + [rows[0]]  # Add a row pin to cols

        with pytest.raises(AssertionError):
            MatrixScanner(
                cols=cols_bad,
                rows=rows,
                diode_orientation=DiodeOrientation.COL2ROW,
                pull=digitalio.Pull.DOWN,
                warmup_cycles=0,
            )

    def test_matrix_scanner_state_initialization(self, mock_scanner_pins):
        """Test matrix state is initialized correctly"""
        cols, rows = mock_scanner_pins

        from mkx.matrix_scanner import MatrixScanner

        scanner = MatrixScanner(
            cols=cols,
            rows=rows,
            diode_orientation=DiodeOrientation.COL2ROW,
            pull=digitalio.Pull.DOWN,
            warmup_cycles=0,
        )

        # State should be all zeros initially (pull down) or ones (pull up)
        assert all(v == 0 for v in scanner.state)

    def test_matrix_scanner_state_with_pull_up(self, mock_scanner_pins):
        """Test matrix state initialization with PULL.UP"""
        cols, rows = mock_scanner_pins

        from mkx.matrix_scanner import MatrixScanner

        scanner = MatrixScanner(
            cols=cols,
            rows=rows,
            diode_orientation=DiodeOrientation.COL2ROW,
            pull=digitalio.Pull.UP,
            warmup_cycles=0,
        )

        # State should be all ones for pull up
        assert all(v == 1 for v in scanner.state)

    def test_matrix_scanner_pin_configuration(self, mock_scanner_pins):
        """Test pins are configured as input/output correctly"""
        cols, rows = mock_scanner_pins

        from mkx.matrix_scanner import MatrixScanner

        scanner = MatrixScanner(
            cols=cols,
            rows=rows,
            diode_orientation=DiodeOrientation.COL2ROW,
            pull=digitalio.Pull.DOWN,
            warmup_cycles=0,
        )

        # Drive pins should be outputs
        for pin in scanner.drive_pins:
            pin.switch_to_output.assert_called_once()

        # Sense pins should be inputs
        for pin in scanner.sense_pins:
            pin.switch_to_input.assert_called()

    def test_matrix_scanner_different_matrix_sizes(self):
        """Test scanner with different matrix sizes"""
        from mkx.matrix_scanner import MatrixScanner

        # Test 3x3 matrix
        cols_3x3 = [MagicMock() for _ in range(3)]
        rows_3x3 = [MagicMock() for _ in range(3)]

        for pin in cols_3x3 + rows_3x3:
            pin.switch_to_output = MagicMock()
            pin.switch_to_input = MagicMock()

        scanner_3x3 = MatrixScanner(
            cols=cols_3x3,
            rows=rows_3x3,
            diode_orientation=DiodeOrientation.COL2ROW,
            pull=digitalio.Pull.DOWN,
            warmup_cycles=0,
        )

        assert scanner_3x3.len_cols == 3
        assert scanner_3x3.len_rows == 3
        assert len(scanner_3x3.state) == 9

    def test_matrix_scanner_single_key_matrix(self):
        """Test scanner with minimal 1x1 matrix"""
        from mkx.matrix_scanner import MatrixScanner

        col = MagicMock()
        col.switch_to_output = MagicMock()
        col.switch_to_input = MagicMock()

        row = MagicMock()
        row.switch_to_output = MagicMock()
        row.switch_to_input = MagicMock()

        scanner = MatrixScanner(
            cols=[col],
            rows=[row],
            diode_orientation=DiodeOrientation.COL2ROW,
            pull=digitalio.Pull.DOWN,
            warmup_cycles=0,
        )

        assert scanner.len_cols == 1
        assert scanner.len_rows == 1
        assert len(scanner.state) == 1


class TestMatrixScannerEdgeCases:
    """Edge case tests for MatrixScanner"""

    def test_ensure_digital_in_out_with_valid_object(self):
        """Test ensure_digital_in_out with valid object"""
        from mkx.matrix_scanner import ensure_digital_in_out

        obj = MagicMock()
        obj.switch_to_input = MagicMock()
        obj.switch_to_output = MagicMock()
        obj.value = 0

        result = ensure_digital_in_out(obj)
        assert result == obj

    def test_invalid_diode_orientation(self):
        """Test that invalid diode orientation raises error"""
        from mkx.matrix_scanner import MatrixScanner

        cols = [MagicMock() for _ in range(2)]
        rows = [MagicMock() for _ in range(2)]

        for pin in cols + rows:
            pin.switch_to_output = MagicMock()
            pin.switch_to_input = MagicMock()

        with pytest.raises(ValueError):
            MatrixScanner(
                cols=cols,
                rows=rows,
                diode_orientation="INVALID",
                pull=digitalio.Pull.DOWN,
                warmup_cycles=0,
            )

    def test_invalid_pull_configuration(self):
        """Test that invalid pull configuration raises error"""
        from mkx.matrix_scanner import MatrixScanner

        cols = [MagicMock() for _ in range(2)]
        rows = [MagicMock() for _ in range(2)]

        for pin in cols + rows:
            pin.switch_to_output = MagicMock()
            pin.switch_to_input = MagicMock()

        with pytest.raises(ValueError):
            MatrixScanner(
                cols=cols,
                rows=rows,
                diode_orientation=DiodeOrientation.COL2ROW,
                pull="INVALID",
                warmup_cycles=0,
            )
