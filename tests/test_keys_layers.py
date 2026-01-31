"""
Unit tests for Layer key functionality.
Tests layer switching, momentary layers, and default layer behavior.
"""

from mkx.keys_layers import KeysLayer, DF, RL, MO
from mkx.keys_standard import KeysStandard
from tests.conftest import MockKeycode


class TestKeysLayer:
    """Test suite for KeysLayer base class"""

    def test_keys_layer_initialization(self):
        """Test KeysLayer initializes correctly"""
        layer = KeysLayer(2)

        assert layer.layer == 2
        assert layer.key_name == "LAY"
        assert layer._is_pressed is False

    def test_keys_layer_on_press_does_nothing(self, mock_keyboard, layer_manager):
        """Test KeysLayer on_press does nothing"""
        layer = KeysLayer(1)

        # Should not raise
        layer.on_press(layer_manager, mock_keyboard, 0)

    def test_keys_layer_on_release_does_nothing(self, mock_keyboard, layer_manager):
        """Test KeysLayer on_release does nothing"""
        layer = KeysLayer(1)

        # Should not raise
        layer.on_release(layer_manager, mock_keyboard, 0)


class TestDefaultLayerKey:
    """Test suite for DF (Default Layer) key"""

    def test_df_initialization(self):
        """Test DF initializes correctly"""
        df = DF(2)

        assert df.layer == 2
        assert df.jump is True
        assert df.key_name == "DF(2)"

    def test_df_initialization_no_jump(self):
        """Test DF with jump=False"""
        df = DF(3, jump=False)

        assert df.layer == 3
        assert df.jump is False

    def test_df_press_sets_default_layer_with_jump(self, mock_keyboard, layer_manager):
        """Test DF press sets default layer and jumps"""
        df = DF(2, jump=True)

        assert layer_manager.default_layer == 0
        assert layer_manager.get_top_layer() == 0

        df.on_press(layer_manager, mock_keyboard, 0)

        assert layer_manager.default_layer == 2
        assert layer_manager.get_top_layer() == 2
        assert layer_manager.active_layers == [2]

    def test_df_press_sets_default_layer_without_jump(
        self, mock_keyboard, layer_manager
    ):
        """Test DF press sets default layer without jumping"""
        layer_manager.activate_layer(1)
        df = DF(2, jump=False)

        df.on_press(layer_manager, mock_keyboard, 0)

        assert layer_manager.default_layer == 2
        # Active layers should have 2 inserted at bottom
        assert 2 in layer_manager.active_layers


class TestReplaceLayerKey:
    """Test suite for RL (Replace Layer) key"""

    def test_rl_initialization(self):
        """Test RL initializes correctly"""
        rl = RL(2)

        assert rl.layer == 2
        assert rl.key_name == "RL(2)"

    def test_rl_press_replaces_top_layer(self, mock_keyboard, layer_manager):
        """Test RL press replaces the top layer"""
        layer_manager.activate_layer(1)
        layer_manager.activate_layer(2)

        assert layer_manager.active_layers == [0, 1, 2]

        rl = RL(3)
        rl.on_press(layer_manager, mock_keyboard, 0)

        assert layer_manager.active_layers == [0, 1, 3]

    def test_rl_press_with_only_default_layer(self, mock_keyboard, layer_manager):
        """Test RL press when only default layer is active"""
        rl = RL(1)

        assert layer_manager.active_layers == [0]

        rl.on_press(layer_manager, mock_keyboard, 0)

        # Should add the layer instead of replacing
        assert layer_manager.active_layers == [0, 1]


class TestMomentaryLayerKey:
    """Test suite for MO (Momentary Layer) key"""

    def test_mo_initialization(self):
        """Test MO initializes correctly"""
        mo = MO(1)

        assert mo.layer == 1
        assert mo.mod is None
        assert mo.key_name == "MO(1)"

    def test_mo_initialization_with_modifier(self):
        """Test MO initializes with modifier"""
        mod_key = KeysStandard(MockKeycode.LEFT_SHIFT, "LSFT")
        mo = MO(2, mod=mod_key)

        assert mo.layer == 2
        assert mo.mod == mod_key

    def test_mo_press_activates_layer(self, mock_keyboard, layer_manager):
        """Test MO press activates layer"""
        mo = MO(1)

        assert layer_manager.get_top_layer() == 0

        mo.on_press(layer_manager, mock_keyboard, 0)

        assert layer_manager.get_top_layer() == 1
        assert 1 in layer_manager.active_layers

    def test_mo_release_deactivates_layer(self, mock_keyboard, layer_manager):
        """Test MO release deactivates layer"""
        mo = MO(1)

        mo.on_press(layer_manager, mock_keyboard, 0)
        assert 1 in layer_manager.active_layers

        mo.on_release(layer_manager, mock_keyboard, 100)

        assert layer_manager.get_top_layer() == 0
        assert 1 not in layer_manager.active_layers

    def test_mo_with_modifier_press_activates_mod(self, mock_keyboard, layer_manager):
        """Test MO with modifier activates modifier on press"""
        mod_key = KeysStandard(MockKeycode.LEFT_SHIFT, "LSFT")
        mo = MO(2, mod=mod_key)

        mo.on_press(layer_manager, mock_keyboard, 0)

        assert 2 in layer_manager.active_layers
        # Modifier should be pressed (or released after being pressed)
        assert (
            MockKeycode.LEFT_SHIFT in mock_keyboard.pressed_keys
            or MockKeycode.LEFT_SHIFT in mock_keyboard.released_keys
        )

    def test_mo_with_modifier_release_deactivates_mod(
        self, mock_keyboard, layer_manager
    ):
        """Test MO with modifier deactivates modifier on release"""
        mod_key = KeysStandard(MockKeycode.LEFT_SHIFT, "LSFT")
        mo = MO(2, mod=mod_key)

        mo.on_press(layer_manager, mock_keyboard, 0)
        mo.on_release(layer_manager, mock_keyboard, 100)

        assert 2 not in layer_manager.active_layers

    def test_mo_press_release_cycle(self, mock_keyboard, layer_manager):
        """Test full MO press-release cycle"""
        mo = MO(1)

        mo.press(layer_manager, mock_keyboard, 0)
        assert mo._is_pressed is True
        assert 1 in layer_manager.active_layers

        mo.release(layer_manager, mock_keyboard, 100)
        assert mo._is_pressed is False
        assert 1 not in layer_manager.active_layers
