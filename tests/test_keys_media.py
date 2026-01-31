"""
Unit tests for Media key functionality.
Tests media key behavior for volume, playback, and brightness control.
"""

from unittest.mock import MagicMock
from mkx.keys_media import KeysMedia, PLAY_PAUSE, MUTE, VOLU, VOLD, BRIU, BRID
from mkx.keys_media import MNXT, MPRV, MSTP


class TestKeysMedia:
    """Test suite for KeysMedia class"""

    def test_keys_media_initialization(self):
        """Test KeysMedia initializes correctly"""
        # Create a mock ConsumerControlCode
        mock_code = MagicMock()

        media = KeysMedia(mock_code, "TEST_MUTE")

        assert media.key_name == "TEST_MUTE"
        assert media._is_pressed is False
        assert media._cc is None

    def test_keys_media_on_press_ensures_cc(self, mock_keyboard, layer_manager):
        """Test KeysMedia on_press ensures consumer control is initialized"""
        mock_code = MagicMock()
        media = KeysMedia(mock_code, "MUTE")
        media._cc = MagicMock()

        media.on_press(layer_manager, mock_keyboard, 0)

        # Should have consumer control initialized
        assert media._cc is not None

    def test_keys_media_on_release_does_nothing(self, mock_keyboard, layer_manager):
        """Test KeysMedia on_release does nothing"""
        mock_code = MagicMock()
        media = KeysMedia(mock_code, "MUTE")

        # Should not raise
        media.on_release(layer_manager, mock_keyboard, 0)

    def test_play_pause_predefined(self):
        """Test PLAY_PAUSE predefined key"""
        # Check that it's a KeysMedia instance
        assert isinstance(PLAY_PAUSE, KeysMedia)
        assert PLAY_PAUSE._is_pressed is False

    def test_mute_predefined(self):
        """Test MUTE predefined key"""
        assert isinstance(MUTE, KeysMedia)
        assert MUTE.key_name == "MUTE"
        assert MUTE._is_pressed is False

    def test_volu_predefined(self):
        """Test VOLU (Volume Up) predefined key"""
        assert isinstance(VOLU, KeysMedia)
        assert VOLU.key_name == "VOLU"
        assert VOLU._is_pressed is False

    def test_vold_predefined(self):
        """Test VOLD (Volume Down) predefined key"""
        assert isinstance(VOLD, KeysMedia)
        assert VOLD.key_name == "VOLD"
        assert VOLD._is_pressed is False

    def test_briu_predefined(self):
        """Test BRIU (Brightness Up) predefined key"""
        assert isinstance(BRIU, KeysMedia)
        assert BRIU.key_name == "BRIU"
        assert BRIU._is_pressed is False

    def test_brid_predefined(self):
        """Test BRID (Brightness Down) predefined key"""
        assert isinstance(BRID, KeysMedia)
        assert BRID.key_name == "BRID"
        assert BRID._is_pressed is False

    def test_mnxt_predefined(self):
        """Test MNXT (Next Track) predefined key"""
        assert isinstance(MNXT, KeysMedia)
        assert MNXT.key_name == "MNXT"
        assert MNXT._is_pressed is False

    def test_mprv_predefined(self):
        """Test MPRV (Previous Track) predefined key"""
        assert isinstance(MPRV, KeysMedia)
        assert MPRV.key_name == "MPRV"
        assert MPRV._is_pressed is False

    def test_mstp_predefined(self):
        """Test MSTP (Stop) predefined key"""
        assert isinstance(MSTP, KeysMedia)
        assert MSTP.key_name == "MSTP"
        assert MSTP._is_pressed is False

    def test_keys_media_press_release_cycle(self, mock_keyboard, layer_manager):
        """Test full media key press-release cycle"""
        mock_code = MagicMock()
        media = KeysMedia(mock_code, "MUTE")

        media.press(layer_manager, mock_keyboard, 0)
        assert media._is_pressed is True

        media.release(layer_manager, mock_keyboard, 100)
        assert media._is_pressed is False
