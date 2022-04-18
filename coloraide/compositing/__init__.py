"""
Compositing and RGB blend modes.

https://www.w3.org/TR/compositing/
"""
from . import porter_duff
from . import blend_modes
from .. import algebra as alg
from ..types import Vector
from ..gamut.bounds import GamutBound, Bounds
from typing import Optional, Union, List, Type, TYPE_CHECKING

if TYPE_CHECKING:  # pragma: no cover
    from ..color import Color


def clip_channel(coord: float, bounds: Bounds) -> float:
    """Clipping channel."""

    a = bounds.lower  # type: Optional[float]
    b = bounds.upper  # type: Optional[float]
    is_bound = isinstance(bounds, GamutBound)

    # These parameters are unbounded
    if not is_bound:  # pragma: no cover
        # Will not execute unless we have a space that defines some coordinates
        # as bound and others as not. We do not currently have such spaces.
        a = None
        b = None

    # Fit value in bounds.
    return alg.clamp(coord, a, b)


def apply_compositing(
    color1: 'Color',
    color2: 'Color',
    blender: Optional[Type[blend_modes.Blend]],
    operator: Union[str, bool]
) -> 'Color':
    """Perform the actual blending."""

    # Get the color coordinates
    csa = alg.no_nan(color1.alpha)
    cba = alg.no_nan(color2.alpha)
    coords1 = alg.no_nans(color1.coords())
    coords2 = alg.no_nans(color2.coords())

    # Setup compositing
    compositor = None  # type: Optional[porter_duff.PorterDuff]
    cra = csa
    if isinstance(operator, str):
        compositor = porter_duff.compositor(operator)(cba, csa)
        cra = compositor.ao()
    elif operator is True:
        compositor = porter_duff.compositor('source-over')(cba, csa)
        cra = compositor.ao()

    # Perform compositing
    bounds = color1._space.BOUNDS
    coords = []  # type: Vector

    # Blend each channel. Afterward, clip and apply alpha compositing.
    i = 0
    for cb, cr in zip(coords2, blender.blend(coords2, coords1) if blender else coords1):
        cr = (1 - cba) * cr + cba * cr if blender else cr
        cr = clip_channel(cr, bounds[i])
        coords.append(compositor.co(cb, cr) if compositor else cr)
        i += 1

    return color1.update(color1.space(), coords, cra)


def compose(
    color: 'Color',
    backdrop: List['Color'],
    blend: Union[str, bool] = True,
    operator: Union[str, bool] = True,
    space: Optional[str] = None
) -> 'Color':
    """Blend colors using the specified blend mode."""

    # We need to go ahead and grab the blender as we need to check what type of blender it is.
    blender = None  # Optional[blend_modes.Blend]
    if isinstance(blend, str):
        blender = blend_modes.get_blender(blend)
    elif blend is True:
        blender = blend_modes.get_blender('normal')
    is_seperable = blender is not None and issubclass(blender, blend_modes.NonSeperableBlend)

    # If we are doing non-separable, we are converting to a special space that
    # can only be done from sRGB, so we have to force sRGB anyway.
    space = 'srgb' if space is None or is_seperable else space.lower()

    if not backdrop:
        return color

    if len(backdrop) > 1:
        dest = backdrop[-1].convert(space)
        for x in range(len(backdrop) - 2, -1, -1):
            src = backdrop[x].convert(space)
            dest = apply_compositing(src, dest, blender, operator)
    else:
        dest = backdrop[0].convert(space)

    src = color.convert(space)

    return apply_compositing(src, dest, blender, operator)
