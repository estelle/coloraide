"""Test sRGB Linear library."""
import unittest
from . import util
from coloraide import Color
import pytest


class TestsRGBLinear(util.ColorAssertsPyTest):
    """Test sRGB Linear."""

    COLORS = [
        ('red', 'color(srgb-linear 1 0 0)'),
        ('orange', 'color(srgb-linear 1 0.37626 0)'),
        ('yellow', 'color(srgb-linear 1 1 0)'),
        ('green', 'color(srgb-linear 0 0.21586 0)'),
        ('blue', 'color(srgb-linear 0 0 1)'),
        ('indigo', 'color(srgb-linear 0.07036 0 0.22323)'),
        ('violet', 'color(srgb-linear 0.85499 0.22323 0.85499)'),
        ('white', 'color(srgb-linear 1 1 1)'),
        ('gray', 'color(srgb-linear 0.21586 0.21586 0.21586)'),
        ('black', 'color(srgb-linear 0 0 0)')
    ]

    @pytest.mark.parametrize('color1,color2', COLORS)
    def test_colors(self, color1, color2):
        """Test colors."""

        self.assertColorEqual(Color(color1).convert('srgb-linear'), Color(color2))


class TestsRGBLinearProperties(util.ColorAsserts, unittest.TestCase):
    """Test sRGB Linear properties."""

    def test_red(self):
        """Test `red`."""

        c = Color('color(srgb-linear 0.1 0.2 0.3 / 1)')
        self.assertEqual(c['red'], 0.1)
        c['red'] = 0.2
        self.assertEqual(c['red'], 0.2)

    def test_green(self):
        """Test `green`."""

        c = Color('color(srgb-linear 0.1 0.2 0.3 / 1)')
        self.assertEqual(c['green'], 0.2)
        c['green'] = 0.1
        self.assertEqual(c['green'], 0.1)

    def test_blue(self):
        """Test `blue`."""

        c = Color('color(srgb-linear 0.1 0.2 0.3 / 1)')
        self.assertEqual(c['blue'], 0.3)
        c['blue'] = 0.1
        self.assertEqual(c['blue'], 0.1)

    def test_alpha(self):
        """Test `alpha`."""

        c = Color('color(srgb-linear 0.1 0.2 0.3 / 1)')
        self.assertEqual(c['alpha'], 1)
        c['alpha'] = 0.5
        self.assertEqual(c['alpha'], 0.5)
