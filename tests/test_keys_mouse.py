"""
Unit tests for Mouse key functionality.
Tests mouse click, press, and movement operations.
"""

from unittest.mock import MagicMock
from mkx.keys_mouse import KeysMouse, LMB, RMB, MMB, BMB, FMB


class TestKeysMouse:
    """Test suite for KeysMouse class"""

    def test_keys_mouse_initialization(self):
        """Test KeysMouse initializes correctly"""
        mouse = KeysMouse("LEFT_CLICK", "click", 1)

        assert mouse.key_name == "LEFT_CLICK"
        assert mouse.mouse_action == "click"
        assert mouse.args == (1,)
        assert mouse._is_pressed is False
        assert mouse._x_move == 1
        assert mouse._y_move == 1
        assert mouse._scroll == 1

    def test_keys_mouse_x_modifier(self):
        """Test KeysMouse X modifier"""
        mouse = KeysMouse("MOVE", "move", 10, 0, 0)

        mouse.X(5)

        assert mouse._x_move == 5

    def test_keys_mouse_y_modifier(self):
        """Test KeysMouse Y modifier"""
        mouse = KeysMouse("MOVE", "move", 0, 10, 0)

        mouse.Y(3)

        assert mouse._y_move == 3

    def test_keys_mouse_s_modifier(self):
        """Test KeysMouse S (scroll) modifier"""
        mouse = KeysMouse("SCROLL", "move", 0, 0, 10)

        mouse.S(2)

        assert mouse._scroll == 2

    def test_keys_mouse_modifier_chaining(self):
        """Test KeysMouse modifier chaining"""
        mouse = KeysMouse("MOVE", "move", 1, 1, 1)

        result = mouse.X(5).Y(3).S(2)

        assert result is mouse  # Should return self for chaining
        assert mouse._x_move == 5
        assert mouse._y_move == 3
        assert mouse._scroll == 2

    def test_keys_mouse_on_press_click(self, mock_keyboard, layer_manager):
        """Test KeysMouse on_press with click action"""
        mouse = KeysMouse("LEFT_CLICK", "click", 1)
        mouse.mouse = MagicMock()

        mouse.on_press(layer_manager, mock_keyboard, 0)

        mouse.mouse.click.assert_called_once_with(1)

    def test_keys_mouse_on_press_press(self, mock_keyboard, layer_manager):
        """Test KeysMouse on_press with press action"""
        mouse = KeysMouse("LEFT_PRESS", "press", 1)
        mouse.mouse = MagicMock()

        mouse.on_press(layer_manager, mock_keyboard, 0)

        mouse.mouse.press.assert_called_once_with(1)

    def test_keys_mouse_on_press_release(self, mock_keyboard, layer_manager):
        """Test KeysMouse on_press with release action"""
        mouse = KeysMouse("LEFT_RELEASE", "release", 1)
        mouse.mouse = MagicMock()

        mouse.on_press(layer_manager, mock_keyboard, 0)

        mouse.mouse.release.assert_called_once_with(1)

    def test_keys_mouse_on_press_move(self, mock_keyboard, layer_manager):
        """Test KeysMouse on_press with move action"""
        mouse = KeysMouse("MOVE_RIGHT", "move", 10, 0, 0)
        mouse.mouse = MagicMock()

        mouse.on_press(layer_manager, mock_keyboard, 0)

        mouse.mouse.move.assert_called_once()

    def test_keys_mouse_on_release_press_action(self, mock_keyboard, layer_manager):
        """Test KeysMouse on_release with press action (releases the button)"""
        mouse = KeysMouse("LEFT_PRESS", "press", 1)
        mouse.mouse = MagicMock()

        mouse.on_release(layer_manager, mock_keyboard, 0)

        mouse.mouse.release.assert_called_once_with(1)

    def test_keys_mouse_on_release_other_actions(self, mock_keyboard, layer_manager):
        """Test KeysMouse on_release with non-press actions (does nothing)"""
        mouse = KeysMouse("LEFT_CLICK", "click", 1)
        mouse.mouse = MagicMock()

        mouse.on_release(layer_manager, mock_keyboard, 0)

        # Should not call anything
        mouse.mouse.click.assert_not_called()
        mouse.mouse.press.assert_not_called()
        mouse.mouse.release.assert_not_called()

    def test_lmb_predefined(self):
        """Test LMB (Left Mouse Button) predefined key"""
        assert LMB.key_name == "LMB"
        assert LMB.mouse_action == "click"
        assert LMB._is_pressed is False

    def test_rmb_predefined(self):
        """Test RMB (Right Mouse Button) predefined key"""
        assert RMB.key_name == "RMB"
        assert RMB.mouse_action == "click"

    def test_mmb_predefined(self):
        """Test MMB (Middle Mouse Button) predefined key"""
        assert MMB.key_name == "MMB"
        assert MMB.mouse_action == "click"

    def test_bmb_predefined(self):
        """Test BMB (Back Mouse Button) predefined key"""
        assert BMB.key_name == "BMB"
        assert BMB.mouse_action == "click"

    def test_fmb_predefined(self):
        """Test FMB (Forward Mouse Button) predefined key"""
        assert FMB.key_name == "FMB"
        assert FMB.mouse_action == "click"

    def test_keys_mouse_press_release_cycle(self, mock_keyboard, layer_manager):
        """Test full mouse key press-release cycle"""
        mouse = KeysMouse("LEFT_CLICK", "click", 1)

        mouse.press(layer_manager, mock_keyboard, 0)
        assert mouse._is_pressed is True

        mouse.release(layer_manager, mock_keyboard, 100)
        assert mouse._is_pressed is False
