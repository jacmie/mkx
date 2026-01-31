"""
Unit tests for Diode Orientation functionality.
Tests diode orientation constants and usage.
"""

from mkx.diode_orientation import DiodeOrientation


class TestDiodeOrientation:
    """Test suite for DiodeOrientation"""

    def test_diode_col2row_value(self):
        """Test COL2ROW orientation value"""
        assert DiodeOrientation.COL2ROW == 0
        assert DiodeOrientation.COLUMNS == 0

    def test_diode_row2col_value(self):
        """Test ROW2COL orientation value"""
        assert DiodeOrientation.ROW2COL == 1
        assert DiodeOrientation.ROWS == 1

    def test_col2row_alias_columns(self):
        """Test that COL2ROW and COLUMNS are equivalent"""
        assert DiodeOrientation.COL2ROW == DiodeOrientation.COLUMNS

    def test_row2col_alias_rows(self):
        """Test that ROW2COL and ROWS are equivalent"""
        assert DiodeOrientation.ROW2COL == DiodeOrientation.ROWS

    def test_orientation_values_are_different(self):
        """Test that the two orientation values are different"""
        assert DiodeOrientation.COL2ROW != DiodeOrientation.ROW2COL
        assert DiodeOrientation.COLUMNS != DiodeOrientation.ROWS

    def test_orientation_integer_conversion(self):
        """Test that orientation values can be used as integers"""
        col2row = DiodeOrientation.COL2ROW
        row2col = DiodeOrientation.ROW2COL

        # Should be usable in integer operations
        assert col2row + 1 == 1
        assert row2col + 1 == 2

    def test_orientation_boolean_context(self):
        """Test orientation values in boolean context"""
        col2row = DiodeOrientation.COL2ROW
        row2col = DiodeOrientation.ROW2COL

        # COL2ROW (0) is falsy
        assert not col2row

        # ROW2COL (1) is truthy
        assert row2col
