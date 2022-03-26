"""Oklch class."""
from .. import oklch as base
from ...css import parse
from ...css import serialize
from ...types import MutableVector
from typing import Union, Optional, Tuple, Any, TYPE_CHECKING

if TYPE_CHECKING:  # pragma: no cover
    from ...color import Color


class Oklch(base.Oklch):
    """Oklch class."""

    def to_string(
        self,
        parent: 'Color',
        *,
        alpha: Optional[bool] = None,
        precision: Optional[int] = None,
        fit: Union[str, bool] = True,
        none: bool = False,
        **kwargs: Any
    ) -> str:
        """Convert to CSS."""

        return serialize.serialize_css(
            parent,
            func='oklch',
            alpha=alpha,
            precision=precision,
            fit=fit,
            none=none,
            color=kwargs.get('color', False),
            percent=True
        )

    @classmethod
    def match(
        cls,
        string: str,
        start: int = 0,
        fullmatch: bool = True
    ) -> Optional[Tuple[Tuple[MutableVector, float], int]]:
        """Match a CSS color string."""

        return parse.parse_css(cls, string, start, fullmatch)
