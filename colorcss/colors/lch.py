"""LCH class."""
from .base import _Color
from .tools import _ColorTools
from .. import parse
from ..util import convert
from .. import util


class _LCH(_ColorTools, _Color):
    """LCH class."""

    COLORSPACE = "lch"
    DEF_BG = "[0, 0, 0, 1]"

    def __init__(self, color=None):
        """Initialize."""

        super().__init__(color)

        if isinstance(color, _Color):
            if color.get_colorspace() == "lch":
                self._cl, self._cc, self._ch, self._alpha = color._cl, color._cc, color._ch, color._alpha
            elif color.get_colorspace() == "srgb":
                self._cl, self._cc, self._ch = convert.rgb_to_lch(color._cr, color._cg, color._cb)
                self._alpha = color._alpha
            elif color.get_colorspace() == "hsl":
                self._cl, self._cc, self._ch = convert.hsl_to_lch(color._ch, color._cs, color._cl)
                self._alpha = color._alpha
            elif color.get_colorspace() == "hwb":
                self._cl, self._cc, self._ch = convert.hwb_to_lch(color._ch, color._cw, color._cb)
                self._alpha = color._alpha
            elif color.get_colorspace() == "lab":
                self._cl, self._cc, self._ch = convert.lab_to_lch(color._cl, color._ca, color._cb)
                self._alpha = color._alpha
            else:
                raise TypeError("Unexpected color space '{}' received".format(color.get_colorspace()))
        elif isinstance(color, str):
            if color is None:
                color = self.DEF_BG
            values = self.match(color)[0]
            if values is None:
                raise ValueError("'{}' does not appear to be a valid color".format(color))
            self._cl, self._cc, self._ch, self._alpha = values
        elif isinstance(color, (list, tuple)):
            if not (3 <= len(color) <= 4):
                raise ValueError("A list of channel values should be of length 3 or 4.")
            self._cl = color[0]
            self._cc = color[0]
            self._ch = color[2]
            self._alpha = 1.0 if len(color) == 3 else color[3]
        else:
            raise TypeError("Unexpected type '{}' received".format(type(color)))

    @property
    def _cl(self):
        """Lightness channel."""

        return self._c1

    @_cl.setter
    def _cl(self, value):
        """Set lightness channel."""

        self._c1 = util.clamp(value, 0.0, None)

    @property
    def _cc(self):
        """Chroma channel."""

        return self._c2

    @_cc.setter
    def _cc(self, value):
        """Set chroma channel."""

        self._c2 = util.clamp(value, 0.0, None)

    @property
    def _ch(self):
        """Hue channel."""

        return self._c3

    @_ch.setter
    def _ch(self, value):
        """Set B on LAB axis."""

        self._c3 = value if 0.0 <= value <= 360.0 else value % 360.0

    def __str__(self):
        """String."""

        return self.to_string(alpha=True)

    def is_achromatic(self, scale=util.INF):
        """Check if the color is achromatic."""

        return self.round_half_up(self._cc, scale) <= 0

    def _grayscale(self):
        """Convert to grayscale."""

        self._cc = 0

    def _mix(self, color, factor, factor2=1.0):
        """Blend the color with the given color."""

        self._cl = self._mix_channel(self._cl, color._cl, factor, factor2, clamp_range=(0.0, None))
        self._cc = self._mix_channel(self._cc, color._cc, factor, factor2, clamp_range=(0.0, None))
        self._ch = self._hue_mix_channel(self._ch, color._ch, factor, factor2, scale=1.0)

    @property
    def lightness(self):
        """Lightness."""

        return self._cl

    @lightness.setter
    def lightness(self, value):
        """Get true luminance."""

        self._cl = self.tx_channel(0, value) if isinstance(value, str) else float(value)

    @property
    def chroma(self):
        """Chroma."""

        return self._cc

    @chroma.setter
    def chroma(self, value):
        """chroma."""

        self._cc = self.tx_channel(1, value) if isinstance(value, str) else float(value)

    @property
    def hue(self):
        """Hue."""

        return self._ch

    @hue.setter
    def hue(self, value):
        """Shift the hue."""

        self._ch = self.tx_channel(2, value) if isinstance(value, str) else float(value)

    @classmethod
    def tx_channel(cls, channel, value):
        """Translate channel string."""

        if channel in (1, 0, -1):
            return float(value)
        elif channel == 2:
            return parse.norm_deg_channel(value) * 360.0

    @classmethod
    def split_channels(cls, color):
        """Split channels."""

        channels = []
        for i, c in enumerate(parse.RE_COMMA_SPLIT.split(color[1:-1].strip()), 0):
            if i <= 2:
                channels.append(cls.tx_channel(i, c))
            else:
                channels.append(cls.tx_channel(-1, c))
        if len(channels) == 3:
            channels.append(1.0)
        return channels
