"""Test Interpolation."""
import unittest
from coloraide import Color, NaN, Piecewise
from . import util


class TestInterpolation(util.ColorAsserts, unittest.TestCase):
    """Test interpolation."""

    def test_mix(self):
        """Test interpolation via mixing."""

        self.assertColorEqual(Color('red').mix('blue', 1), Color("rgb(0 0 255)"))
        self.assertColorEqual(Color('red').mix('blue', 0.75), Color("rgb(80.686 71.104 209.56)"))
        self.assertColorEqual(Color('red').mix('blue'), Color("rgb(140.36 83.033 162.31)"))
        self.assertColorEqual(Color('red').mix('blue', 0.25), Color("rgb(197.88 73.02 108.95)"))
        self.assertColorEqual(Color('red').mix('blue', 0.0), Color("rgb(255 0 0)"))

    def test_mix_dict(self):
        """Test mixing with a mapping."""

        c1 = Color('blue')
        self.assertEqual(
            c1.mix("yellow"),
            c1.mix({"space": "srgb", "r": 1, "g": 1, "b": 0})
        )

    def test_bad_mix_input(self):
        """Test bad mix input."""

        with self.assertRaises(TypeError):
            Color('red').mix(1)

    def test_mix_input_piecewise(self):
        """Test mix with piecewise."""

        self.assertColorEqual(
            Color('red').mix(Piecewise('blue'), 0.5, space="srgb"), Color("srgb", [0.5, 0, 0.5])
        )

    def test_mix_space(self):
        """Test color mix in different space."""

        self.assertColorEqual(Color('red').mix('blue', 1, space="srgb"), Color("srgb", [0, 0, 1]))
        self.assertColorEqual(Color('red').mix('blue', 0.75, space="srgb"), Color("srgb", [0.25, 0, 0.75]))
        self.assertColorEqual(Color('red').mix('blue', space="srgb"), Color("srgb", [0.5, 0, 0.5]))
        self.assertColorEqual(Color('red').mix('blue', 0.25, space="srgb"), Color("srgb", [0.75, 0, 0.25]))
        self.assertColorEqual(Color('red').mix('blue', 0.0, space="srgb"), Color("srgb", [1, 0, 0]))

    def test_mix_out_space(self):
        """Test interpolation."""

        self.assertColorEqual(
            Color('red').mix('blue', 1, space="lab", out_space="lab"),
            Color("lab(29.568% 68.287 -112.03)")
        )
        self.assertColorEqual(
            Color('red').mix('blue', 0.75, space="lab", out_space="lab"),
            Color("lab(35.749% 71.417 -66.55)")
        )
        self.assertColorEqual(
            Color('red').mix('blue', space="lab", out_space="lab"),
            Color("lab(41.929% 74.546 -21.069)")
        )
        self.assertColorEqual(
            Color('red').mix('blue', 0.25, space="lab", out_space="lab"),
            Color("lab(48.11% 77.676 24.411)")
        )
        self.assertColorEqual(
            Color('red').mix('blue', 0.0, space="lab", out_space="lab"),
            Color("lab(54.291% 80.805 69.891)")
        )

    def test_mix_alpha(self):
        """Test mixing alpha."""

        self.assertColorEqual(
            Color('color(srgb 1 0 0 / 0.75)').mix('color(srgb 0 0 1 / 0.25)', space="srgb"),
            Color('rgb(127.5 0 127.5 / 0.5)')
        )

    def test_mix_premultiplied_alpha(self):
        """Test premultiplied alpha."""

        self.assertColorEqual(
            Color('color(srgb 1 0 0 / 0.75)').mix('color(srgb 0 0 1 / 0.25)', premultiplied=True, space="srgb"),
            Color('rgb(191.25 0 63.75 / 0.5)')
        )

    def test_mix_premultiplied_no_alpha(self):
        """Test premultiplied alpha."""

        self.assertColorEqual(
            Color('color(srgb 1 0 0)').mix('color(srgb 0 0 1)', premultiplied=True, space="srgb"),
            Color('color(srgb 1 0 0)').mix('color(srgb 0 0 1)', space="srgb")
        )

    def test_mix_premultiplied_cylindrical(self):
        """Test premultiplication in a cylindrical space."""

        self.assertColorEqual(
            Color('color(--hsl 20 30% 75% / 0.5)').mix(
                'color(--hsl 20 60% 10% / 0.75)', premultiplied=True, space="hsl"
            ),
            Color('hsl(20 48% 36% / 0.625)')
        )

    def test_mix_in_place(self):
        """Test mix in place."""

        color = Color('red')
        color2 = color.mix('blue', space="srgb")
        self.assertIsNot(color, color2)
        self.assertColorEqual(color2, Color("srgb", [0.5, 0, 0.5]))
        color = Color('red')
        color2 = color.mix('blue', space="srgb", in_place=True)
        self.assertIs(color, color2)
        self.assertColorEqual(color, Color("srgb", [0.5, 0, 0.5]))

    def test_mix_nan(self):
        """Test mixing with NaN."""

        c1 = Color("srgb", [NaN, 1, 1])
        c2 = Color("srgb", [0.75, 0, 0])
        self.assertColorEqual(c1.mix(c2, space="srgb"), Color("srgb", [0.75, 0.5, 0.5]))
        c1 = Color("srgb", [0.25, 1, 1])
        c2 = Color("srgb", [NaN, 0, 0])
        self.assertColorEqual(c1.mix(c2, space="srgb"), Color("srgb", [0.25, 0.5, 0.5]))
        c1 = Color("srgb", [NaN, 1, 1])
        c2 = Color("srgb", [NaN, 0, 0])
        self.assertColorEqual(c1.mix(c2, space="srgb"), Color("srgb", [0, 0.5, 0.5]))

    def test_mix_mask(self):
        """Test mix adjust method."""

        c1 = Color("color(srgb 0.25 1 1)")
        c2 = Color("color(srgb 0.75 0 0)")
        self.assertColorEqual(c1.mix(c2.mask("red"), space="srgb"), Color("srgb", [0.25, 0.5, 0.5]))

        c1 = Color("color(srgb 0.25 1 1)")
        c2 = Color("color(srgb 0.75 0 0)")
        self.assertColorEqual(c1.mask("red").mix(c2, space="srgb"), Color("srgb", [0.75, 0.5, 0.5]))

        c1 = Color("color(srgb 0.25 1 1)")
        c2 = Color("color(srgb 0.75 0 0)")
        self.assertColorEqual(c1.mask("red").mix(c2.mask("red"), space="srgb"), Color("srgb", [0.0, 0.5, 0.5]))

        c1 = Color("color(srgb 0.25 1 1)")
        c2 = Color("color(srgb 0.75 0 0)")
        self.assertColorEqual(c1.mix(c2.mask(["red", "green"]), space="srgb"), Color("srgb", [0.25, 1, 0.5]))

    def test_mix_mask_invert(self):
        """Test mix adjust method."""

        c1 = Color("color(srgb 0.25 1 1)")
        c2 = Color("color(srgb 0.75 0 0)")
        self.assertColorEqual(
            c1.mix(c2.mask(["green", "blue"], invert=True), space="srgb"),
            Color("srgb", [0.25, 0.5, 0.5])
        )

        c1 = Color("color(srgb 0.25 1 1)")
        c2 = Color("color(srgb 0.75 0 0)")
        self.assertColorEqual(
            c1.mask(["green", "blue"], invert=True).mix(c2, space="srgb"),
            Color("srgb", [0.75, 0.5, 0.5])
        )

        c1 = Color("color(srgb 0.25 1 1)")
        c2 = Color("color(srgb 0.75 0 0)")
        self.assertColorEqual(
            c1.mask(["green", "blue", "alpha"], invert=True).mix(
                c2.mask(["green", "blue", "alpha"], invert=True),
                space="srgb"
            ),
            Color("srgb", [0.0, 0.5, 0.5])
        )

        c1 = Color("color(srgb 0.25 1 1)")
        c2 = Color("color(srgb 0.75 0 0)")
        self.assertColorEqual(
            c1.mix(c2.mask("blue", invert=True), space="srgb"),
            Color("srgb", [0.25, 1, 0.5])
        )

    def test_mix_hue_adjust(self):
        """Test hue adjusting."""

        c1 = Color('rebeccapurple')
        c2 = Color('lch(85% 100 805)')
        self.assertColorEqual(
            c1.mix(c2.mask("hue", invert=True), 0.25, hue="shorter", space="lch"),
            Color("rgb(146.72 -3.9233 106.41)")
        )
        self.assertColorEqual(
            c1.mix(c2.mask("hue", invert=True), 0.25, hue="longer", space="lch"),
            Color("rgb(-86.817 87.629 170)")
        )
        self.assertColorEqual(
            c1.mix(c2.mask("hue", invert=True), 0.25, hue="increasing", space="lch"),
            Color("rgb(146.72 -3.9233 106.41)")
        )
        self.assertColorEqual(
            c1.mix(c2.mask("hue", invert=True), 0.25, hue="decreasing", space="lch"),
            Color("rgb(-86.817 87.629 170)")
        )
        self.assertColorEqual(
            c1.mix(c2.mask("hue", invert=True), 0.25, hue="specified", space="lch"),
            Color("rgb(112.83 63.969 -28.821)")
        )

    def test_hue_shorter_cases(self):
        """Cover shorter hue cases."""

        # c2 - c1 > 180
        c1 = Color('lch(75% 50 40)')
        c2 = Color('lch(30% 30 350)')
        self.assertColorEqual(
            c1.mix(c2.mask("hue", invert=True), 0.50, hue="shorter", space="lch"),
            Color("lch(75% 50 375)")
        )

        # c2 - c1 < -180
        c1 = Color('lch(30% 30 350)')
        c2 = Color('lch(75% 50 40)')
        self.assertColorEqual(
            c1.mix(c2.mask("hue", invert=True), 0.50, hue="shorter", space="lch"),
            Color("lch(30% 30 375)")
        )

    def test_hue_longer_cases(self):
        """Cover longer hue cases."""

        # 0 < (c2 - c1) < 180
        c1 = Color('lch(75% 50 40)')
        c2 = Color('lch(30% 30 60)')
        self.assertColorEqual(
            c1.mix(c2.mask("hue", invert=True), 0.50, hue="longer", space="lch"),
            Color("lch(75% 50 230)")
        )

        # -180 < (c2 - c1) < 0
        c1 = Color('lch(30% 30 60)')
        c2 = Color('lch(75% 50 40)')
        self.assertColorEqual(
            c1.mix(c2.mask("hue", invert=True), 0.50, hue="longer", space="lch"),
            Color("lch(30% 30 230)")
        )

    def test_hue_increasing_cases(self):
        """Cover increasing hue cases."""

        # c2 < c1
        c1 = Color('lch(75% 50 60)')
        c2 = Color('lch(30% 30 40)')
        self.assertColorEqual(
            c1.mix(c2.mask("hue", invert=True), 0.50, hue="increasing", space="lch"),
            Color("lch(75% 50 230)")
        )

    def test_hue_decreasing_cases(self):
        """Cover decreasing hue cases."""

        # c1 < c2
        c1 = Color('lch(75% 50 40)')
        c2 = Color('lch(30% 30 60)')
        self.assertColorEqual(
            c1.mix(c2.mask("hue", invert=True), 0.50, hue="decreasing", space="lch"),
            Color("lch(75% 50 230)")
        )

    def test_mix_hue_adjust_bad(self):
        """Test hue adjusting."""

        c1 = Color('rebeccapurple')
        c2 = Color('lch(85% 100 805)')
        with self.assertRaises(ValueError):
            c1.mix(c2.mask("hue", invert=True), 0.25, hue="bad", space="lch")

    def test_mix_hue_nan(self):
        """Test mix hue with `NaN`."""

        self.assertColorEqual(
            Color('hsl', [NaN, 0, 0.25]).mix(Color('hsl', [NaN, 0, 0.9]), 0.50, space="hsl"),
            Color("hsl(0, 0%, 57.5%)")
        )

        self.assertColorEqual(
            Color('hsl', [NaN, 0, 0.25]).mix(Color('hsl', [120, 0.5, 0.9]), 0.50, space="hsl"),
            Color("hsl(120, 25%, 57.5%)")
        )

        self.assertColorEqual(
            Color('hsl', [120, 0.5, 0.25]).mix(Color('hsl', [NaN, 0, 0.9]), 0.50, space="hsl"),
            Color("hsl(120, 25%, 57.5%)")
        )

    def test_mix_progress(self):
        """Test custom progress."""

        progress = lambda x: x * 3  # noqa: E731
        self.assertColorEqual(
            Color('red').mix('blue', 1, out_space="lab", space="lab", progress=progress),
            Color("lab(-19.876% 43.252 -475.87)")
        )
        self.assertColorEqual(
            Color('red').mix('blue', 0.75, out_space="lab", space="lab", progress=progress),
            Color("lab(-1.3345% 52.64 -339.43)")
        )
        self.assertColorEqual(
            Color('red').mix('blue', 0.5, out_space="lab", space="lab", progress=progress),
            Color("lab(17.207% 62.029 -202.99)")
        )
        self.assertColorEqual(
            Color('red').mix('blue', 0.25, out_space="lab", space="lab", progress=progress),
            Color("lab(35.749% 71.417 -66.55)")
        )
        self.assertColorEqual(
            Color('red').mix('blue', 0, out_space="lab", space="lab", progress=progress),
            Color("lab(54.291% 80.805 69.891)")
        )

    def test_interpolate_fit_required(self):
        """Test interpolation case that requires fitting."""

        self.assertColorEqual(
            Color('color(display-p3 0 1 1)').interpolate('color(display-p3 0 0 1)', space='hsl')(0.5),
            Color('color(display-p3 0.21789 0.49793 0.96522)')
        )

    def test_interpolate(self):
        """Test interpolation."""

        self.assertColorEqual(Color('red').interpolate('blue', space="srgb")(1), Color("srgb", [0, 0, 1]))
        self.assertColorEqual(Color('red').interpolate('blue', space="srgb")(0.75), Color("srgb", [0.25, 0, 0.75]))
        self.assertColorEqual(Color('red').interpolate('blue', space="srgb")(0.5), Color("srgb", [0.5, 0, 0.5]))
        self.assertColorEqual(Color('red').interpolate('blue', space="srgb")(0.25), Color("srgb", [0.75, 0, 0.25]))
        self.assertColorEqual(Color('red').interpolate('blue', space="srgb")(0), Color("srgb", [1, 0, 0]))

    def test_interpolate_channel(self):
        """Test interpolating a specific channel differently."""

        self.assertColorEqual(
            Color('red').interpolate(Color('blue').set('alpha', 0), progress={'alpha': lambda t: t ** 3})(0.5),
            Color('rgb(140.36 83.033 162.31 / 0.875)')
        )

    def test_interpolate_channel_all(self):
        """Test interpolating a specific channel differently, but setting the others via all."""

        self.assertColorEqual(
            Color('red').interpolate(
                Color('blue').set('alpha', 0), progress={
                    'alpha': lambda t: t ** 3,
                    'all': lambda t: 0
                })(0.5),
            Color('rgb(255 0 0 / 0.875)')
        )

    def test_interpolate_channel_aliases(self):
        """Test interpolating a specific channel using a color's channel alias."""

        self.assertColorEqual(
            Color('orange').interpolate(
                Color('purple'),
                progress={
                    'red': lambda t: t ** 3
                },
                space='srgb'
            )(0.5),
            Color('rgb(239.13 82.5 64)')
        )

    def test_interpolate_input_piecewise(self):
        """Test interpolation with piecewise."""

        self.assertColorEqual(
            Color('red').interpolate(Piecewise('blue'), space="srgb")(0.5), Color("srgb", [0.5, 0, 0.5])
        )

    def test_interpolate_stop(self):
        """Test interpolation with piecewise."""

        self.assertColorEqual(
            Color('red').interpolate('blue', space="srgb", stop=0.6)(0.5), Color('red')
        )
        self.assertColorEqual(
            Color('red').interpolate('blue', space="srgb", stop=0.6)(0.7), Color('rgb(191.25 0 63.75)')
        )

    def test_interpolate_space(self):
        """Test color mix in different space."""

        self.assertColorEqual(Color('red').interpolate('blue', space='lab')(1), Color("rgb(0 0 255)"))
        self.assertColorEqual(Color('red').interpolate('blue', space='lab')(0.75), Color("rgb(144.85 -24.864 194.36)"))
        self.assertColorEqual(Color('red').interpolate('blue', space='lab')(0.5), Color("rgb(192.99 -29.503 136.17)"))
        self.assertColorEqual(Color('red').interpolate('blue', space='lab')(0.25), Color("rgb(226.89 -24.304 79.188)"))
        self.assertColorEqual(Color('red').interpolate('blue', space='lab')(0), Color("rgb(255 0 0)"))

    def test_interpolate_empty_list(self):
        """Test interpolate with empty list."""

        self.assertColorEqual(Color('green').interpolate([])(0.5), Color('green'))

    def test_interpolate_piecewise(self):
        """Test multiple inputs for interpolation."""

        func = Color('white').interpolate(['red', 'black'])
        self.assertColorEqual(func(0), Color('white'))
        self.assertColorEqual(func(0.5), Color('red'))
        self.assertColorEqual(func(1), Color('black'))
        self.assertColorEqual(func(-0.1), Color('rgb(248.66 273.11 277.36)'))
        self.assertColorEqual(func(1.1), Color('rgb(-3.2946 0 0)'))

    def test_interpolate_out_space(self):
        """Test interpolation."""

        self.assertColorEqual(
            Color('red').interpolate('blue', out_space="lab", space="lab")(1),
            Color("lab(29.568% 68.287 -112.03)")
        )
        self.assertColorEqual(
            Color('red').interpolate('blue', out_space="lab", space="lab")(0.75),
            Color("lab(35.749% 71.417 -66.55)")
        )
        self.assertColorEqual(
            Color('red').interpolate('blue', out_space="lab", space="lab")(0.5),
            Color("lab(41.929% 74.546 -21.069)")
        )
        self.assertColorEqual(
            Color('red').interpolate('blue', out_space="lab", space="lab")(0.25),
            Color("lab(48.11% 77.676 24.411)")
        )
        self.assertColorEqual(
            Color('red').interpolate('blue', out_space="lab", space="lab")(0),
            Color("lab(54.291% 80.805 69.891)")
        )

    def test_interpolate_alpha(self):
        """Test mixing alpha."""

        self.assertColorEqual(
            Color('color(srgb 1 0 0 / 0.75)').interpolate('color(srgb 0 0 1 / 0.25)', space="srgb")(0.5),
            Color('rgb(127.5 0 127.5 / 0.5)')
        )

    def test_interpolate_premultiplied_alpha(self):
        """Test premultiplied alpha."""

        self.assertColorEqual(
            Color('color(srgb 1 0 0 / 0.75)').interpolate(
                'color(srgb 0 0 1 / 0.25)', space="srgb", premultiplied=True
            )(0.5),
            Color('rgb(191.25 0 63.75 / 0.5)')
        )

    def test_interpolate_premultiplied_alpha_none(self):
        """Test premultiplied alpha when alphas are none."""

        self.assertColorEqual(
            Color('color(srgb 0 0 0 / none)').interpolate(
                'color(srgb 0 1 0 / none)', space="srgb", premultiplied=True
            )(0.5),
            Color('rgb(0 0 0 / 0)')
        )

    def test_interpolate_premultiplied_no_alpha(self):
        """Test premultiplied alpha."""

        self.assertColorEqual(
            Color('color(srgb 1 0 0)').interpolate('color(srgb 0 0 1)', space="srgb", premultiplied=True)(0.5),
            Color('color(srgb 1 0 0)').interpolate('color(srgb 0 0 1)', space="srgb")(0.5)
        )

    def test_interpolate_nan(self):
        """Test mixing with NaN."""

        c1 = Color("srgb", [NaN, 1, 1])
        c2 = Color("srgb", [0.75, 0, 0])
        self.assertColorEqual(c1.interpolate(c2, space="srgb")(0.5), Color("srgb", [0.75, 0.5, 0.5]))
        c1 = Color("srgb", [0.25, 1, 1])
        c2 = Color("srgb", [NaN, 0, 0])
        self.assertColorEqual(c1.interpolate(c2, space="srgb")(0.5), Color("srgb", [0.25, 0.5, 0.5]))
        c1 = Color("srgb", [NaN, 1, 1])
        c2 = Color("srgb", [NaN, 0, 0])
        self.assertColorEqual(c1.interpolate(c2, space="srgb")(0.5), Color("srgb", [0, 0.5, 0.5]))

    def test_interpolate_adjust(self):
        """Test mix adjust method."""

        c1 = Color("color(srgb 0.25 1 1)")
        c2 = Color("color(srgb 0.75 0 0)")
        self.assertColorEqual(
            c1.interpolate(c2.mask("red"), space="srgb")(0.5),
            Color("srgb", [0.25, 0.5, 0.5])
        )

    def test_interpolate_hue_adjust(self):
        """Test hue adjusting."""

        c1 = Color('rebeccapurple')
        c2 = Color('lch(85% 100 805)')
        self.assertColorEqual(
            c1.interpolate(c2.mask("hue", invert=True), hue="shorter", space="lch")(0.25),
            Color("rgb(146.72 -3.9233 106.41)")
        )
        self.assertColorEqual(
            c1.interpolate(c2.mask("hue", invert=True), hue="longer", space="lch")(0.25),
            Color("rgb(-86.817 87.629 170)")
        )
        self.assertColorEqual(
            c1.interpolate(c2.mask("hue", invert=True), hue="increasing", space="lch")(0.25),
            Color("rgb(146.72 -3.9233 106.41)")
        )
        self.assertColorEqual(
            c1.interpolate(c2.mask("hue", invert=True), hue="decreasing", space="lch")(0.25),
            Color("rgb(-86.817 87.629 170)")
        )
        self.assertColorEqual(
            c1.interpolate(c2.mask("hue", invert=True), hue="specified", space="lch")(0.25),
            Color("rgb(112.83 63.969 -28.821)")
        )

    def test_interpolate_progress(self):
        """Test custom progress."""

        progress = lambda x: x * 3  # noqa: E731
        self.assertColorEqual(
            Color('red').interpolate('blue', out_space="lab", space="lab", progress=progress)(1),
            Color("lab(-19.876% 43.252 -475.87)")
        )
        self.assertColorEqual(
            Color('red').interpolate('blue', out_space="lab", space="lab", progress=progress)(0.75),
            Color("lab(-1.3345% 52.64 -339.43)")
        )
        self.assertColorEqual(
            Color('red').interpolate('blue', out_space="lab", space="lab", progress=progress)(0.5),
            Color("lab(17.207% 62.029 -202.99)")
        )
        self.assertColorEqual(
            Color('red').interpolate('blue', out_space="lab", space="lab", progress=progress)(0.25),
            Color("lab(35.749% 71.417 -66.55)")
        )
        self.assertColorEqual(
            Color('red').interpolate('blue', out_space="lab", space="lab", progress=progress)(0),
            Color("lab(54.291% 80.805 69.891)")
        )

    def test_steps(self):
        """Test steps."""

        colors = Color('red').steps('blue', space="srgb", steps=5)
        self.assertColorEqual(colors[4], Color("srgb", [0, 0, 1]))
        self.assertColorEqual(colors[3], Color("srgb", [0.25, 0, 0.75]))
        self.assertColorEqual(colors[2], Color("srgb", [0.5, 0, 0.5]))
        self.assertColorEqual(colors[1], Color("srgb", [0.75, 0, 0.25]))
        self.assertColorEqual(colors[0], Color("srgb", [1, 0, 0]))

    def test_steps_input_piecewise(self):
        """Test steps with piecewise."""

        self.assertColorEqual(
            Color('red').steps(Piecewise('blue'), space="srgb", steps=5)[2], Color("srgb", [0.5, 0, 0.5])
        )

    def test_steps_multi(self):
        """Test steps with multiple color ranges."""

        colors = Color('white').steps(['red', 'black'], steps=3)
        self.assertColorEqual(colors[0], Color('white'))
        self.assertColorEqual(colors[1], Color('red'))
        self.assertColorEqual(colors[2], Color('black'))

    def test_steps_multi_max_delta_e(self):
        """Test steps with multiple color ranges and max_delta_e."""

        colors = Color('red').steps(['green', 'blue'], space="srgb", max_delta_e=10)
        for index, color in enumerate(colors, 0):
            if not index:
                continue
            self.assertTrue(color.delta_e(colors[index - 1]) <= 10)

        colors = Color('red').steps(['green', 'blue'], space="srgb", max_delta_e=3)
        for index, color in enumerate(colors, 0):
            if not index:
                continue
            self.assertTrue(color.delta_e(colors[index - 1]) <= 3)

    def test_steps_custom_delta_e(self):
        """Test a custom delta E input."""

        colors = Color('red').steps(['green', 'blue'], space="srgb", max_delta_e=10, delta_e='99o')
        for index, color in enumerate(colors, 0):
            if not index:
                continue
            self.assertTrue(color.delta_e(colors[index - 1]) <= 10)

        colors = Color('red').steps(['green', 'blue'], space="srgb", max_delta_e=3, delta_e='99o')
        for index, color in enumerate(colors, 0):
            if not index:
                continue
            self.assertTrue(color.delta_e(colors[index - 1]) <= 3)

    def test_steps_custom_delta_compare(self):
        """Test a custom delta E input."""

        colors1 = len(Color('orange').steps('red', space="srgb", max_delta_e=0.2, delta_e='76'))
        colors2 = len(Color('orange').steps('red', space="srgb", max_delta_e=0.2, delta_e='ok'))

        self.assertNotEqual(colors1, colors2)

    def test_steps_empty_list(self):
        """Test steps with empty list."""

        self.assertColorEqual(Color('green').steps([], steps=3)[1], Color('green'))

    def test_steps_space(self):
        """Test steps different space."""

        colors = Color('red').steps('blue', space="lab", steps=5)
        self.assertColorEqual(colors[4], Color("rgb(0 0 255)"))
        self.assertColorEqual(colors[3], Color("rgb(144.85 -24.864 194.36)"))
        self.assertColorEqual(colors[2], Color("rgb(192.99 -29.503 136.17)"))
        self.assertColorEqual(colors[1], Color("rgb(226.89 -24.304 79.188)"))
        self.assertColorEqual(colors[0], Color("rgb(255 0 0)"))

    def test_steps_out_space(self):
        """Test steps with output in different space."""

        colors = Color('red').steps('blue', space="srgb", steps=5, out_space="lab")
        self.assertColorEqual(
            colors[4],
            Color("lab(29.568% 68.287 -112.03)")
        )
        self.assertColorEqual(
            colors[3],
            Color("lab(24.638% 57.331 -83.546)")
        )
        self.assertColorEqual(
            colors[2],
            Color("lab(29.563% 55.954 -36.19)")
        )
        self.assertColorEqual(
            colors[1],
            Color("lab(41.111% 66.202 23.413)")
        )
        self.assertColorEqual(
            colors[0],
            Color("lab(54.291% 80.805 69.891)")
        )

    def test_steps_alpha(self):
        """Test mixing alpha."""

        self.assertColorEqual(
            Color('color(srgb 1 0 0 / 0.75)').steps('color(srgb 0 0 1 / 0.25)', space="srgb", steps=1)[0],
            Color('rgb(127.5 0 127.5 / 0.5)')
        )

    def test_steps_premultiplied_alpha(self):
        """Test premultiplied alpha."""

        self.assertColorEqual(
            Color('color(srgb 1 0 0 / 0.75)').steps(
                'color(srgb 0 0 1 / 0.25)', space="srgb", steps=1, premultiplied=True
            )[0],
            Color('rgb(191.25 0 63.75 / 0.5)')
        )

    def test_steps_premultiplied_no_alpha(self):
        """Test premultiplied alpha."""

        self.assertColorEqual(
            Color('color(srgb 1 0 0)').steps('color(srgb 0 0 1)', space="srgb", steps=1, premultiplied=True)[0],
            Color('color(srgb 1 0 0)').steps('color(srgb 0 0 1)', space="srgb", steps=1)[0]
        )

    def test_steps_nan(self):
        """Test steps with NaN."""

        c1 = Color("srgb", [NaN, 1, 1])
        c2 = Color("srgb", [0.75, 0, 0])
        self.assertColorEqual(c1.steps(c2, space="srgb", steps=1)[0], Color("srgb", [0.75, 0.5, 0.5]))
        c1 = Color("srgb", [0.25, 1, 1])
        c2 = Color("srgb", [NaN, 0, 0])
        self.assertColorEqual(c1.steps(c2, space="srgb", steps=1)[0], Color("srgb", [0.25, 0.5, 0.5]))
        c1 = Color("srgb", [NaN, 1, 1])
        c2 = Color("srgb", [NaN, 0, 0])
        self.assertColorEqual(c1.steps(c2, space="srgb", steps=1)[0], Color("srgb", [0, 0.5, 0.5]))

    def test_steps_adjust(self):
        """Test steps with adjust method."""

        c1 = Color("color(srgb 0.25 1 1)")
        c2 = Color("color(srgb 0.75 0 0)")
        self.assertColorEqual(
            c1.steps(c2.mask("red"), space="srgb", steps=1)[0],
            Color("srgb", [0.25, 0.5, 0.5])
        )

    def test_steps_hue_adjust(self):
        """Test steps with hue adjusting."""

        self.assertColorEqual(
            Color('rebeccapurple').steps(
                Color('lch(85% 100 805)').mask("hue", invert=True), space="lch", steps=5, hue="shorter"
            )[1],
            Color("rgb(146.72 -3.9233 106.41)")
        )
        self.assertColorEqual(
            Color('rebeccapurple').steps(
                Color('lch(85% 100 805)').mask("hue", invert=True), space="lch", steps=5, hue="longer"
            )[1],
            Color("rgb(-86.817 87.629 170)")
        )
        self.assertColorEqual(
            Color('rebeccapurple').steps(
                Color('lch(85% 100 805)').mask("hue", invert=True), space="lch", steps=5, hue="increasing"
            )[1],
            Color("rgb(146.72 -3.9233 106.41)")
        )
        self.assertColorEqual(
            Color('rebeccapurple').steps(
                Color('lch(85% 100 805)').mask("hue", invert=True), space="lch", steps=5, hue="decreasing"
            )[1],
            Color("rgb(-86.817 87.629 170)")
        )
        self.assertColorEqual(
            Color('rebeccapurple').steps(
                Color('lch(85% 100 805)').mask("hue", invert=True), space="lch", steps=5, hue="specified"
            )[1],
            Color("rgb(112.83 63.969 -28.821)")
        )

    def test_steps_progress(self):
        """Test custom progress."""

        progress = lambda x: x * 3  # noqa: E731
        colors = Color('red').steps('blue', steps=5, out_space="lab", space="lab", progress=progress)
        self.assertColorEqual(
            colors[4],
            Color("lab(-19.876% 43.252 -475.87)")
        )
        self.assertColorEqual(
            colors[3],
            Color("lab(-1.3345% 52.64 -339.43)")
        )
        self.assertColorEqual(
            colors[2],
            Color("lab(17.207% 62.029 -202.99)")
        )
        self.assertColorEqual(
            colors[1],
            Color("lab(35.749% 71.417 -66.55)")
        )
        self.assertColorEqual(
            colors[0],
            Color("lab(54.291% 80.805 69.891)")
        )

    def test_steps_max_delta_e(self):
        """Test steps with a max delta e."""

        colors = Color('red').steps('blue', space="srgb", max_delta_e=10)
        for index, color in enumerate(colors, 0):
            if not index:
                continue
            self.assertTrue(color.delta_e(colors[index - 1]) <= 10)

        colors = Color('red').steps('blue', space="srgb", max_delta_e=3)
        for index, color in enumerate(colors, 0):
            if not index:
                continue
            self.assertTrue(color.delta_e(colors[index - 1]) <= 3)

    def test_steps_max_delta_e_steps(self):
        """Test steps with a max delta e."""

        colors = Color('red').steps('blue', space="srgb", max_delta_e=10)
        self.assertTrue(len(colors) > 5)
        colors = Color('red').steps('blue', space="srgb", max_delta_e=10, max_steps=5)
        self.assertTrue(len(colors) == 5)