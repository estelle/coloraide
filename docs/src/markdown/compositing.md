# Compositing and Blending

## Compositing

Alpha compositing and blending are tied together under the umbrella of compositing. Each is just an aspect of
the overall compositing of colors. Blend is run first, followed by alpha compositing.

ColorAide implements both alpha compositing and blending as described in the [Compositing and Blending Level 1][compositing-level-1]
specification. Alpha composting is based on [Porter Duff compositing][porter-duff]. By default, the `compose` method
uses the `normal` blend mode and the `source-over` Porter Duff operator.

### Blending

Blending is the aspect of compositing that calculates the mixing of colors where the source element and backdrop
overlap. Conceptually, the colors in the source element (top layer) are blended in place with the backdrop
(bottom layer).

There are various blend modes, the most common is the `normal` blend mode which is the default blending mode for
browsers when a layer is placed over another layer. The `normal` mode simply returns the top layer's color when two are
overlaid. Some weighting of colors can occur if top layer is semi-transparent.

<span class="isolate blend-normal dual">
  <span class="circle circle-1"></span>
  <span class="circle circle-2"></span>
</span>

But there are many blend modes that could be used, all of which yield different results. If we were to apply a
`multiply` blend mode, we would get something very different:

<span class="isolate blend-multiply dual">
  <span class="circle circle-1"></span>
  <span class="circle circle-2"></span>
</span>

When composing, the blend mode can be controlled separately in ColorAide. Here, we again use the `multiply` example
and replicate it in ColorAide.

!!! note "Display Differences"
    As some browsers apply compositing based on the display's current color space, we've provided examples in both sRGB
    and Display P3 so that the examples can be compared on different displays. Which of the below matches your browser?

<span class="isolate blend-multiply dual">
  <span class="circle circle-1"></span>
  <span class="circle circle-2"></span>
</span>

=== "Display P3"
    ```color
    Color('#07c7ed').compose('#fc3d99', blend='multiply', space="display-p3")
    ```

=== "sRGB"
    ```color
    Color('#07c7ed').compose('#fc3d99', blend='multiply', space="srgb")
    ```

Lastly, if for any reason, it is desired to compose with blending disabled (e.g. just run alpha compositing), then you
can simply set `operator` to `#!py3 False`.

[`multiply`](#multiply) is just one of many blend modes that are offered in ColorAide, check out
[Blend Modes](#blend-modes) to learn about other blend modes.

### Alpha Compositing

Alpha compositing or alpha blending is the process of combining one image with a background to create the appearance of
partial or full transparency.

When dealing with layers, there are many possible ways to handle them:

![Alpha Composition](images/alpha_compositing.svg)

Porter Duff compositing covers all possible configurations of layers. Many of these configurations can be useful for all
sorts of operations, such as masking. While this library [supports all of them](#compositing-operators), the most
commonly used one is [`source-over`](#source-over) which is used to implement simple alpha compositing to simulate
semi-transparent layers on top of each other.

<span class="isolate blend-normal dual">
  <span class="circle circle-1"></span>
  <span class="circle circle-2" style="opacity: 0.5"></span>
</span>

Given two colors, ColorAide can replicate this behavior and determine the resultant color by applying compositing. We
will use the demonstration above and replicate the result in the example below. Below we set the source color to
`#!color Color('#07c7ed').set('alpha', 0.5)` and the backdrop color to `#!color #fc3d99` and run it through the
`compose` method.

!!! note "Display Differences"
    As some browsers apply compositing based on the display's current color space, we've provided examples in both sRGB
    and Display P3 so that the examples can be compared on different displays. Which of the below matches your browser?

<span class="isolate blend-normal dual">
  <span class="circle circle-1"></span>
  <span class="circle circle-2" style="opacity: 0.5"></span>
</span>

=== "Display P3"
    ```color
    Color('#07c7ed').set('alpha', 0.5).compose('#fc3d99', space="display-p3")
    ```

=== "sRGB"
    ```color
    Color('#07c7ed').set('alpha', 0.5).compose('#fc3d99', space="srgb")
    ```

While the average user will be content with the default alpha compositing, Porter Duff offers many other configurations.
If desired, we can change the Porter Duff operator used and apply different composite logic. For instance, in this case
we can get the resultant of the backdrop over the source color by setting the `operator` to `destination-over`. As the
backdrop is fully opaque, we just get the backdrop color unaltered.

<span class="isolate blend-normal dual">
  <span class="circle circle-2" style="opacity: 0.5"></span>
  <span class="circle circle-1"></span>
</span>

=== "Display P3"
    ```color
    Color('#07c7ed').set('alpha', 0.5).compose('#fc3d99', operator='destination-over', space="display-p3")
    ```

=== "sRGB"
    ```color
    Color('#07c7ed').set('alpha', 0.5).compose('#fc3d99', operator='destination-over', space="srgb")
    ```

Lastly, if for any reason, it is desired to run compose with alpha compositing disabled (e.g. just run blending),
then you can simply set `operator` to `#!py3 False`.

Check out [Compositing Operators](#compositing-operators) to learn about the many variations that are supported.

### Complex Compositing

We've covered alpha compositing and blending and have demonstrated their use with simple two color examples, but what if
we have complex scenarios with multiple color layers?

In this example, we will consider circles, each with a unique color: `#!color #07c7ed`, `#!color #fc3d99`, and
`#!color #f5d311`. We apply 50% transparency to all the circles and place them on a `#!color white` background. We then
perform a `multiply` blend on all the circles but isolate them so the `multiply` blend does not apply to the background.
The circles are all represented with CSS. We will now try and replicate the colors with ColorAide.

So in the code below, we work our way from the bottom of the stack to the top. Since the background is isolated from the
`multiply` blending, in each region, we start by performing a `normal` blend on the bottom circle against the
background. We then apply `multiply` blending on each color that is stacked on top. We've provided both the P3 and sRGB
outputs to make it easy to compare in case your browser blends in one instead of the other.

<div style="background: white; display: inline-block; padding: 10px;">
<span class="isolate blend-multiply">
  <span class="circle circle-1" style="opacity: 0.5"></span>
  <span class="circle circle-2" style="opacity: 0.5"></span>
  <span class="circle circle-3" style="opacity: 0.5"></span>
</span>
</div>

=== "Display P3"
    ```color
    c1 = Color('#07c7ed').set('alpha', 0.5)
    c2 = Color('#fc3d99').set('alpha', 0.5)
    c3 = Color('#f5d311').set('alpha', 0.5)

    cw2 = c2.compose('white', blend='normal', space='display-p3')
    cw3 = c3.compose('white', blend='normal', space='display-p3')

    r1 = c2.compose(cw3, blend='multiply', space='display-p3')
    r2 = c1.compose(cw2, blend='multiply', space='display-p3')
    r3 = c1.compose(cw3, blend='multiply', space='display-p3')

    r1, r2, r3

    c1.compose(r1, blend='multiply', space='display-p3')
    ```

=== "sRGB"
    ```color
    c1 = Color('#07c7ed').set('alpha', 0.5)
    c2 = Color('#fc3d99').set('alpha', 0.5)
    c3 = Color('#f5d311').set('alpha', 0.5)

    cw2 = c2.compose('white', blend='normal', space='srgb')
    cw3 = c3.compose('white', blend='normal', space='srgb')

    r1 = c2.compose(cw3, blend='multiply', space='srgb')
    r2 = c1.compose(cw2, blend='multiply', space='srgb')
    r3 = c1.compose(cw3, blend='multiply', space='srgb')

    r1, r2, r3

    c1.compose(r1, blend='multiply', space='srgb')
    ```

Results may vary depending on the browser, but we can see (ignoring rounding differences) that the colors match up. This
was performed on Chrome in macOS using a display that uses `display-p3`.

![Color Meter](images/color_meter.gif)

## Blend Modes

<div class="blend-wrap" markdown="1">
<span class="isolate blend-normal">
  <span class="circle circle-1"></span>
  <span class="circle circle-2"></span>
  <span class="circle circle-3"></span>
</span>

<div class="blend-content" markdown="1">

### Normal

The blending formula simply selects the source color.
</div>
</div>

---

<div class="blend-wrap" markdown="1">
<span class="isolate blend-multiply">
  <span class="circle circle-1"></span>
  <span class="circle circle-2"></span>
  <span class="circle circle-3"></span>
</span>

<div class="blend-content" markdown="1">

### Multiply

The source color is multiplied by the destination color and replaces the destination. The resultant color is always at
least as dark as either the source or destination color. Multiplying any color with black results in black. Multiplying
any color with white preserves the original color.
</div>
</div>

---

<div class="blend-wrap" markdown="1">
<span class="isolate blend-screen">
  <span class="circle circle-1"></span>
  <span class="circle circle-2"></span>
  <span class="circle circle-3"></span>
</span>

<div class="blend-content" markdown="1">

### Screen

Multiplies the complements of the backdrop and source color values, then complements the result. The result color is
always at least as light as either of the two constituent colors. Screening any color with white produces white;
screening with black leaves the original color unchanged. The effect is similar to projecting multiple photographic
slides simultaneously onto a single screen.
</div>
</div>

---

<div class="blend-wrap" markdown="1">
<span class="isolate blend-overlay">
  <span class="circle circle-1"></span>
  <span class="circle circle-2"></span>
  <span class="circle circle-3"></span>
</span>

<div class="blend-content" markdown="1">

### Overlay

Multiplies or screens the colors, depending on the backdrop color value. Source colors overlay the backdrop while
preserving its highlights and shadows. The backdrop color is not replaced but is mixed with the source color to reflect
the lightness or darkness of the backdrop.
</div>
</div>

---

<div class="blend-wrap" markdown="1">
<span class="isolate blend-darken">
  <span class="circle circle-1"></span>
  <span class="circle circle-2"></span>
  <span class="circle circle-3"></span>
</span>

<div class="blend-content" markdown="1">

### Darken

Selects the darker of the backdrop and source colors. The backdrop is replaced with the source where the source is
darker; otherwise, it is left unchanged.
</div>
</div>

---

<div class="blend-wrap" markdown="1">
<span class="isolate blend-lighten">
  <span class="circle circle-1"></span>
  <span class="circle circle-2"></span>
  <span class="circle circle-3"></span>
</span>

<div class="blend-content" markdown="1">

### Lighten

Selects the lighter of the backdrop and source colors. The backdrop is replaced with the source where the source is
lighter; otherwise, it is left unchanged.
</div>
</div>

---

<div class="blend-wrap" markdown="1">
<span class="isolate blend-color-dodge">
  <span class="circle circle-1"></span>
  <span class="circle circle-2"></span>
  <span class="circle circle-3"></span>
</span>

<div class="blend-content" markdown="1">

### Color Dodge

Brightens the backdrop color to reflect the source color. Painting with black produces no changes.
</div>
</div>

---

<div class="blend-wrap" markdown="1">
<span class="isolate blend-color-burn">
  <span class="circle circle-1"></span>
  <span class="circle circle-2"></span>
  <span class="circle circle-3"></span>
</span>

<div class="blend-content" markdown="1">

### Color Burn

Darkens the backdrop color to reflect the source color. Painting with white produces no change.
</div>
</div>

---

<div class="blend-wrap" markdown="1">
<span class="isolate blend-hard-light">
  <span class="circle circle-1"></span>
  <span class="circle circle-2"></span>
  <span class="circle circle-3"></span>
</span>

<div class="blend-content" markdown="1">

### Hard Light

Multiplies or screens the colors, depending on the source color value. The effect is similar to shining a harsh
spotlight on the backdrop.
</div>
</div>

---

<div class="blend-wrap" markdown="1">
<span class="isolate blend-soft-light">
  <span class="circle circle-1"></span>
  <span class="circle circle-2"></span>
  <span class="circle circle-3"></span>
</span>

<div class="blend-content" markdown="1">

### Soft Light

Darkens or lightens the colors, depending on the source color value. The effect is similar to shining a diffused
spotlight on the backdrop.
</div>
</div>

---

<div class="blend-wrap" markdown="1">
<span class="isolate blend-difference">
  <span class="circle circle-1"></span>
  <span class="circle circle-2"></span>
  <span class="circle circle-3"></span>
</span>

<div class="blend-content" markdown="1">

### Difference

Subtracts the darker of the two constituent colors from the lighter color. Painting with white inverts the backdrop
color; painting with black produces no change.
</div>
</div>

---

<div class="blend-wrap" markdown="1">
<span class="isolate blend-exclusion">
  <span class="circle circle-1"></span>
  <span class="circle circle-2"></span>
  <span class="circle circle-3"></span>
</span>

<div class="blend-content" markdown="1">

### Exclusion

Produces an effect similar to that of the Difference mode but lower in contrast. Painting with white inverts the
backdrop color; painting with black produces no change.
</div>
</div>

---

<div class="blend-wrap" markdown="1">
<span class="isolate blend-hue">
  <span class="circle circle-1"></span>
  <span class="circle circle-2"></span>
  <span class="circle circle-3"></span>
</span>

<div class="blend-content" markdown="1">

### Hue

Creates a color with the hue of the source color and the saturation and luminosity of the backdrop color.
</div>
</div>

---

<div class="blend-wrap" markdown="1">
<span class="isolate blend-saturation">
  <span class="circle circle-1"></span>
  <span class="circle circle-2"></span>
  <span class="circle circle-3"></span>
</span>

<div class="blend-content" markdown="1">

### Saturation

Creates a color with the saturation of the source color and the hue and luminosity of the backdrop color. Painting with
this mode in an area of the backdrop that is a pure gray (no saturation) produces no change.
</div>
</div>

---

<div class="blend-wrap" markdown="1">
<span class="isolate blend-luminosity">
  <span class="circle circle-1"></span>
  <span class="circle circle-2"></span>
  <span class="circle circle-3"></span>
</span>

<div class="blend-content" markdown="1">

### Luminosity

Creates a color with the luminosity of the source color and the hue and saturation of the backdrop color. This produces
an inverse effect to that of the Color mode. This mode is the one you can use to create monochrome "tinted" image
effects like the ones you can see in different website headers.
</div>
</div>

---

<div class="blend-wrap" markdown="1">
<span class="isolate blend-color">
  <span class="circle circle-1"></span>
  <span class="circle circle-2"></span>
  <span class="circle circle-3"></span>
</span>

<div class="blend-content" markdown="1">

### Color

Creates a color with the hue and saturation of the source color and the luminosity of the backdrop color. This preserves
the gray levels of the backdrop and is useful for coloring monochrome images or tinting color images.
</div>
</div>

## Compositing Operators

### Clear

No regions are enabled.

![Clear](images/PD_clr.svg)

### Copy

Only the source will be present.

![Clear](images/PD_src.svg)

### Destination

Only the destination will be present.

![Clear](images/PD_dst.svg)

### Source Over

Source is placed over the destination.

![Clear](images/PD_src-over.svg)

### Destination Over

Destination is placed over the source.

![Clear](images/PD_dst-over.svg)

### Source In

The source that overlaps the destination, replaces the destination.

![Clear](images/PD_src-in.svg)

### Destination In

Destination which overlaps the source, replaces the source.

![Destination In](images/PD_dst-in.svg)

### Source Out

Source is placed, where it falls outside of the destination.

![Clear](images/PD_src-out.svg)

### Destination Out

Destination is placed, where it falls outside of the source.

![Clear](images/PD_dst-out.svg)

### Source Atop

Source which overlaps the destination, replaces the destination. Destination is placed elsewhere.

![Clear](images/PD_src-atop.svg)

### Destination Atop

Destination which overlaps the source replaces the source. Source is placed elsewhere.

![Clear](images/PD_dst-atop.svg)

### XOR

Destination which overlaps the source replaces the source. Source is placed elsewhere.

![Clear](images/PD_xor.svg)

### Lighter

Display the sum of the source image and destination image.

--8<-- "refs.txt"
--8<-- "compositing.txt"