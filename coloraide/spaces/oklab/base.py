"""
Oklab class.

Adapted to ColorAide Python and ColorAide by Isaac Muse (2021)

---- License ----

Copyright (c) 2021 Björn Ottosson

Permission is hereby granted, free of charge, to any person obtaining a copy of
this software and associated documentation files (the "Software"), to deal in
the Software without restriction, including without limitation the rights to
use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies
of the Software, and to permit persons to whom the Software is furnished to do
so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""
from ...spaces import Space, RE_DEFAULT_MATCH, GamutUnbound, OptionalPercent, Labish
from ..srgb_linear import SRGBLinear
from ..xyz import XYZ
from ... import util
import re

# sRGB Linear to LMS
SRGBL_TO_LMS = [
    [0.4122214694707628, 0.5363325372617349, 0.0514459932675022],
    [0.2119034958178251, 0.6806995506452344, 0.10739695353694052],
    [0.08830245919005637, 0.2817188391361215, 0.6299787016738223]
]

# LMS to sRGB Linear
LMS_TO_SRGBL = [
    [4.076741636075959, -3.3077115392580634, 0.23096990318210434],
    [-1.2684379732850315, 2.609757349287688, -0.34131937600265705],
    [-0.004196076138675551, -0.703418617935936, 1.7076146940746113]
]

# LMS ** 1/3 to Oklab
LMS3_TO_OKLAB = [
    [0.2104542553, 0.793617785, -0.0040720468],
    [1.9779984951, -2.428592205, 0.4505937099],
    [0.0259040371, 0.7827717662, -0.808675766]
]

# Oklab to LMS ** 1/3
OKLAB_TO_LMS3 = [
    [0.9999999984505199, 0.3963377921737679, 0.2158037580607588],
    [1.0000000088817607, -0.10556134232365635, -0.06385417477170591],
    [1.0000000546724108, -0.08948418209496575, -1.2914855378640917]
]

# XYZ D65 to LMS
XYZD65_TO_LMS = [
    [0.819022437996703, 0.3619062600528904, -0.1288737815209879],
    [0.03298365393238847, 0.9292868615863434, 0.03614466635064236],
    [0.04817718935962421, 0.2642395317527308, 0.6335478284694309]
]

# LMS to XYZ
LMS_TO_XYZD65 = [
    [1.2268798758459243, -0.5578149944602171, 0.2813910456659647],
    [-0.04057574521480085, 1.112286803280317, -0.07171105806551636],
    [-0.07637293667466007, -0.4214933324022432, 1.5869240198367816]
]


def oklab_to_linear_srgb(lab):
    """Convert from Oklab to linear sRGB."""

    return util.dot(LMS_TO_SRGBL, [c ** 3 for c in util.dot(OKLAB_TO_LMS3, lab)])


def linear_srgb_to_oklab(rgb):
    """Linear sRGB to Oklab."""

    return util.dot(LMS3_TO_OKLAB, [util.cbrt(c) for c in util.dot(SRGBL_TO_LMS, rgb)])


def oklab_to_xyz_d65(lab):
    """Convert from Oklab to XYZ D65."""

    return util.dot(LMS_TO_XYZD65, [c ** 3 for c in util.dot(OKLAB_TO_LMS3, lab)])


def xyz_d65_to_oklab(xyz):
    """XYZ D65 to Oklab."""

    return util.dot(LMS3_TO_OKLAB, [util.cbrt(c) for c in util.dot(XYZD65_TO_LMS, xyz)])


class Oklab(Labish, Space):
    """Oklab class."""

    SPACE = "oklab"
    SERIALIZE = ("--oklab",)
    CHANNEL_NAMES = ("l", "a", "b", "alpha")
    CHANNEL_ALIASES = {
        "lightness": "l"
    }
    DEFAULT_MATCH = re.compile(RE_DEFAULT_MATCH.format(color_space='|'.join(SERIALIZE), channels=3))
    WHITE = "D65"

    RANGE = (
        GamutUnbound([OptionalPercent(0), OptionalPercent(1)]),
        GamutUnbound([-0.5, 0.5]),
        GamutUnbound([-0.5, 0.5])
    )

    @property
    def l(self):
        """L channel."""

        return self._coords[0]

    @l.setter
    def l(self, value):
        """Get true luminance."""

        self._coords[0] = self._handle_input(value)

    @property
    def a(self):
        """A channel."""

        return self._coords[1]

    @a.setter
    def a(self, value):
        """A axis."""

        self._coords[1] = self._handle_input(value)

    @property
    def b(self):
        """B channel."""

        return self._coords[2]

    @b.setter
    def b(self, value):
        """B axis."""

        self._coords[2] = self._handle_input(value)

    @classmethod
    def _to_srgb(cls, parent, oklab):
        """To sRGB."""

        return SRGBLinear._to_srgb(parent, cls._to_srgb_linear(parent, oklab))

    @classmethod
    def _from_srgb(cls, parent, srgb):
        """From sRGB."""

        return cls._from_srgb_linear(parent, SRGBLinear._from_srgb(parent, srgb))

    @classmethod
    def _to_srgb_linear(cls, parent, oklab):
        """To sRGB Linear."""

        return oklab_to_linear_srgb(oklab)

    @classmethod
    def _from_srgb_linear(cls, parent, srgbl):
        """From SRGB Linear."""

        return linear_srgb_to_oklab(srgbl)

    @classmethod
    def _to_xyz(cls, parent, oklab):
        """To XYZ."""

        return parent.chromatic_adaptation(cls.WHITE, XYZ.WHITE, oklab_to_xyz_d65(oklab))

    @classmethod
    def _from_xyz(cls, parent, xyz):
        """From XYZ."""

        return xyz_d65_to_oklab(parent.chromatic_adaptation(XYZ.WHITE, cls.WHITE, xyz))