"""Colors."""
from .srgb import _SRGB
from .hsl import _HSL
from .hwb import _HWB
from .lab import _LAB
from .lch import _LCH
from ...colors import _HSV
from ...colors import _Display_P3
from ...colors import _A98_RGB
from ...colors import _ProPhoto_RGB
from ...matcher import color_fullmatch, color_match

__all__ = ("SRGB", "HSL", "HWB", "LAB", "LCH", "HSV", "Display_P3", "a98-rgb", "prophoto-rgb")

SPACES = frozenset({"srgb", "hsl", "hsv", "hwb", "lch", "lab", "display-p3", "a98-rgb", "prophoto-rgb"})

CS_MAP = {}


class HSV(_HSV):
    """HSV color class."""

    spaces = CS_MAP


class SRGB(_SRGB):
    """RGB color class."""

    spaces = CS_MAP


class HSL(_HSL):
    """HSL color class."""

    spaces = CS_MAP


class HWB(_HWB):
    """HWB color class."""

    spaces = CS_MAP


class LAB(_LAB):
    """HWB color class."""

    spaces = CS_MAP


class LCH(_LCH):
    """HWB color class."""

    spaces = CS_MAP


class Display_P3(_Display_P3):
    """Display-p3 color class."""

    spaces = CS_MAP


class A98_RGB(_A98_RGB):
    """A98 RGB color class."""

    spaces = CS_MAP


class ProPhoto_RGB(_ProPhoto_RGB):
    """ProPhoto RGB color class."""

    spaces = CS_MAP


SUPPORTED = (HSL, HWB, LAB, LCH, SRGB, HSV, Display_P3, A98_RGB, ProPhoto_RGB)
for obj in SUPPORTED:
    CS_MAP[obj.space()] = obj


def colorcss(string, spaces=SPACES):
    """Match a color and return a match object."""

    return color_fullmatch(string, SUPPORTED, spaces)


def colorcss_match(string, start=0, fullmatch=False, spaces=SPACES):
    """Match a color and return a match object."""

    return color_match(string, start, fullmatch, SUPPORTED, spaces)
