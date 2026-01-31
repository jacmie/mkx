"""
Unit tests for Modifier key functionality.
Tests modifier key combinations with standard keys.
"""

import pytest
from mkx.keys_modifiers import MOD, M_LCTL, M_LSFT, M_LALT, M_LGUI
from mkx.keys_modifiers import M_RCTL, M_RSFT, M_RALT, M_RGUI
from mkx.keys_standard import KeysStandard
from tests.conftest import MockKeycode


class TestModifierKeys:
    """Test suite for Modifier key functionality"""

    @pytest.fixture
    def base_key(self):
        """Fixture providing a base key to modify"""
        return KeysStandard(MockKeycode.A, "A")

    @pytest.fixture
    def modifier_key(self):
        """Fixture providing a modifier key (Shift)"""
        return KeysStandard(MockKeycode.LEFT_SHIFT, "LSFT")

    def test_mod_initialization(self, base_key, modifier_key):
        """Test MOD initializes correctly"""
        mod = MOD(modifier_key, base_key, "MOD(LSFT,A)")

        assert mod._key_mod == modifier_key
        assert mod._key_code == base_key
        assert mod.key_name == "MOD(LSFT,A)"

    def test_m_lctl_initialization(self, base_key):
        """Test M_LCTL initializes correctly"""
        m_lctl = M_LCTL(base_key)

        assert m_lctl.key_name == f"M_LCTL({base_key.key_name})"
        assert m_lctl._key_mod.key_code == MockKeycode.LEFT_CONTROL

    def test_m_lsft_initialization(self, base_key):
        """Test M_LSFT initializes correctly"""
        m_lsft = M_LSFT(base_key)

        assert m_lsft.key_name == f"M_LSFT({base_key.key_name})"
        assert m_lsft._key_mod.key_code == MockKeycode.LEFT_SHIFT

    def test_m_lalt_initialization(self, base_key):
        """Test M_LALT initializes correctly"""
        m_lalt = M_LALT(base_key)

        assert m_lalt.key_name == f"M_LALT({base_key.key_name})"
        assert m_lalt._key_mod.key_code == MockKeycode.LEFT_ALT

    def test_m_lgui_initialization(self, base_key):
        """Test M_LGUI initializes correctly"""
        m_lgui = M_LGUI(base_key)

        assert m_lgui.key_name == f"M_LGUI({base_key.key_name})"
        assert m_lgui._key_mod.key_code == MockKeycode.LEFT_GUI

    def test_m_rctl_initialization(self, base_key):
        """Test M_RCTL initializes correctly"""
        m_rctl = M_RCTL(base_key)

        assert m_rctl.key_name == f"M_RCTL({base_key.key_name})"
        assert m_rctl._key_mod.key_code == MockKeycode.RIGHT_CONTROL

    def test_m_rsft_initialization(self, base_key):
        """Test M_RSFT initializes correctly"""
        m_rsft = M_RSFT(base_key)

        assert m_rsft.key_name == f"M_RSFT({base_key.key_name})"
        assert m_rsft._key_mod.key_code == MockKeycode.RIGHT_SHIFT

    def test_m_ralt_initialization(self, base_key):
        """Test M_RALT initializes correctly"""
        m_ralt = M_RALT(base_key)

        assert m_ralt.key_name == f"M_RALT({base_key.key_name})"
        assert m_ralt._key_mod.key_code == MockKeycode.RIGHT_ALT

    def test_m_rgui_initialization(self, base_key):
        """Test M_RGUI initializes correctly"""
        m_rgui = M_RGUI(base_key)

        assert m_rgui.key_name == f"M_RGUI({base_key.key_name})"
        assert m_rgui._key_mod.key_code == MockKeycode.RIGHT_GUI

    def test_mod_on_press_triggers_sequence(
        self, mock_keyboard, layer_manager, base_key, modifier_key
    ):
        """Test MOD on_press triggers modifier + key sequence"""
        mod = MOD(modifier_key, base_key, "MOD_TEST")

        mod.on_press(layer_manager, mock_keyboard, 0)

        # Should have pressed modifier, key, and released both
        assert modifier_key.key_code in mock_keyboard.pressed_keys or (
            modifier_key.key_code in mock_keyboard.released_keys
        )
        assert base_key.key_code in mock_keyboard.released_keys

    def test_mod_on_release_does_nothing(self, mock_keyboard, layer_manager, base_key):
        """Test MOD on_release does nothing"""
        modifier = KeysStandard(MockKeycode.LEFT_SHIFT, "LSFT")
        mod = MOD(modifier, base_key, "MOD_TEST")

        # on_release should do nothing (pass)
        mod.on_release(layer_manager, mock_keyboard, 100)

    def test_m_lctl_press_release(self, mock_keyboard, layer_manager, base_key):
        """Test M_LCTL press-release behavior"""
        m_lctl = M_LCTL(base_key)

        m_lctl.press(layer_manager, mock_keyboard, 0)
        assert m_lctl._is_pressed is True

        m_lctl.release(layer_manager, mock_keyboard, 100)
        assert m_lctl._is_pressed is False
