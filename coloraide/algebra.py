"""
Math related methods.

Includes various math related functions to aide in color translation and manipulation.

We actually also implement a number of matrix methods. This is mainly to avoid requiring
all of `numpy` as a dependency. While `numpy` would be faster and more feature rich,
avoiding it keeps our dependencies light.

Often, we will borrow the API interface of `numpy`, but functionality may not be the same.
We will often reduce complexity to handle simple 2D matrices as that is all we ever need
for colors (so far). We will also abandon features if we don't want to figure them out as
we aren't suing them :).
"""
import sys
import math
import operator
from functools import reduce
from itertools import zip_longest as zipl
from .types import Array, Matrix, Vector, MutableArray, MutableMatrix, MutableVector, SupportsFloatOrInt
from typing import Optional, Callable, Sequence, List, Union, Iterator, Tuple, Any, Iterable, cast

NaN = float('nan')
INF = float('inf')
PY38 = (3, 8) <= sys.version_info

if sys.version_info >= (3, 8):
    prod = math.prod
else:
    def prod(values: Iterable[SupportsFloatOrInt]) -> SupportsFloatOrInt:
        """Get the product of a list of numbers."""

        return reduce((lambda x, y: x * y), values)


A2D = (2, 2)
A1D = (1, 1)
A1D_A2D = (1, 2)
A2D_A1D = (2, 1)
NUM_A1D = (0, 1)
A1D_NUM = (1, 0)
NUM_A2D = (0, 2)
A2D_NUM = (2, 0)
NUM_NUM = (0, 0)
ND_MD = (3, 3)


################################
# General math
################################
def is_nan(obj: float) -> bool:
    """Check if "not a number"."""

    return math.isnan(obj)


def no_nans(value: Vector, default: float = 0.0) -> MutableVector:
    """Ensure there are no `NaN` values in a sequence."""

    return [(default if is_nan(x) else x) for x in value]


def no_nan(value: float, default: float = 0.0) -> float:
    """Convert list of numbers or single number to valid numbers."""

    return default if is_nan(value) else value


def round_half_up(n: float, scale: int = 0) -> float:
    """Round half up."""

    mult = 10.0 ** scale
    return math.floor(n * mult + 0.5) / mult


def clamp(
    value: SupportsFloatOrInt,
    mn: Optional[SupportsFloatOrInt] = None,
    mx: Optional[SupportsFloatOrInt] = None
) -> SupportsFloatOrInt:
    """Clamp the value to the the given minimum and maximum."""

    if mn is not None and mx is not None:
        return max(min(value, mx), mn)
    elif mn is not None:
        return max(value, mn)
    elif mx is not None:
        return min(value, mx)
    else:
        return value


def cbrt(n: float) -> float:
    """Calculate cube root."""

    return nth_root(n, 3)


def nth_root(n: float, p: float) -> float:
    """Calculate nth root while handling negative numbers."""

    if p == 0:  # pragma: no cover
        return float('inf')

    if n == 0:
        # Can't do anything with zero
        return 0

    return math.copysign(abs(n) ** (p ** -1), n)


def npow(base: float, exp: float) -> float:
    """Perform `pow` with a negative number."""

    return math.copysign(abs(base) ** exp, base)


################################
# Matrix/linear algebra math
################################
def _vector_dot(a: Vector, b: Vector) -> float:
    """Dot two vectors."""

    return sum([x * y for x, y in zipl(a, b)])


def _extract_dimension(
    m: Array,
    target: int,
    depth: int = 0
) -> Iterator[Array]:
    """
    Extract the requested dimension.

    Mainly used only to extract the last two dimensions of a matrix.
    As not really generalized for "any" dimension, not really good to expose publicly.
    """

    if depth == target:
        if isinstance(m[0], Sequence):
            yield cast(Array, [[cast(Array, x)[r] for x in m] for r in range(len(m[0]))])
        else:
            yield m
    else:
        for m2 in m:
            yield from cast(Array, _extract_dimension(cast(Array, m2), target, depth + 1))


def dot(
    a: Union[float, Array],
    b: Union[float, Array],
    dims: Optional[Tuple[int, int]] = None
) -> Union[float, MutableArray]:
    """
    Get dot product of simple numbers, vectors, and matrices.

    Matrices will be detected and the appropriate logic applied
    unless `dims` is provided. `dims` should simply describe the
    number of dimensions of `a` and `b`: (2, 1) for a 2D and 1D array.
    Providing `dims` will sidestep analyzing the matrix for a more
    performant operation. Anything dimensions above 2 will be treated
    as an ND x MD scenario and the actual dimensions will be extracted
    regardless due to necessity.
    """

    if dims is None or dims[0] > 2 or dims[1] > 2:
        shape_a = shape(a)
        shape_b = shape(b)
        dims_a = len(shape_a)
        dims_b = len(shape_b)

        # Handle matrices of N-D and M-D size
        if dims_a and dims_b and dims_a > 2 or dims_b > 2:
            if dims_a == 1:
                # Dot product of vector and a M-D matrix
                columns1 = list(_extract_dimension(cast(Matrix, b), dims_b - 2))
                shape_c = shape_b[:-2] + shape_b[-1:]
                return cast(
                    MutableMatrix,
                    reshape(
                        [[_vector_dot(cast(Vector, a), cast(Vector, c)) for c in col] for col in columns1],
                        shape_c
                    )
                )
            else:
                # Dot product of N-D and M-D matrices
                # Resultant size: `dot(xy, yz) = xz` or `dot(nxy, myz) = nxmz`
                columns2 = list(_extract_dimension(cast(Array, b), dims_b - 2)) if dims_b > 1 else cast(Array, [[b]])
                rows = list(_extract_dimension(cast(Array, a), dims_a - 1))
                m2 = [
                    [[sum(cast(List[float], multiply(row, c))) for c in cast(Vector, col)] for col in columns2]
                    for row in rows
                ]
                shape_c = shape_a[:-1]
                if dims_b != 1:
                    shape_c += shape_b[:-2] + shape_b[-1:]
                return cast(MutableMatrix, reshape(cast(MutableArray, m2), shape_c))

    else:
        dims_a, dims_b = dims

    # Optimize to handle arrays <= 2-D
    if dims_a == 1:
        if dims_b == 1:
            # Dot product of two vectors
            return _vector_dot(cast(Vector, a), cast(Vector, b))
        elif dims_b == 2:
            # Dot product of vector and a matrix
            return cast(MutableVector, [_vector_dot(cast(Vector, a), col) for col in zipl(*cast(Matrix, b))])

    elif dims_a == 2:
        if dims_b == 1:
            # Dot product of matrix and a vector
            return cast(MutableVector, [_vector_dot(row, cast(Vector, b)) for row in cast(Matrix, a)])
        elif dims_b == 2:
            # Dot product of two matrices
            return cast(
                MutableMatrix,
                [[_vector_dot(row, col) for col in zipl(*cast(Matrix, b))] for row in cast(Matrix, a)]
            )

    # Trying to dot a number with a vector or a matrix, so just multiply
    return multiply(a, b, (dims_a, dims_b))


def _vector_math(op: Callable[..., float], a: Vector, b: Vector) -> MutableVector:
    """Divide two vectors."""

    # Broadcast the vector
    if len(a) == 1:
        a = [a[0]] * len(b)
    elif len(b) == 1:
        b = [b[0]] * len(a)

    return [op(x, y) for x, y in zipl(a, b)]


def _math(
    op: Callable[..., float],
    a: Union[float, Array],
    b: Union[float, Array],
    dims: Optional[Tuple[int, int]] = None
) -> Union[float, MutableArray]:
    """
    Reuse same logic for basic, multiplication, division, addition and subtraction.

    Optimized methods are provided for:
    - equal size matrices
    - operations between two inputs whose number of dimensions are below 2
    - operations involving at least one scalar

    Matrices will be detected and the appropriate logic applied
    unless `dims` is provided. `dims` should simply describe the
    number of dimensions of `a` and `b`: (2, 1) for a 2D and 1D array.
    Providing `dims` will sidestep analyzing the matrix for a more
    performant operation. Anything dimensions above 2 will be treated
    as an ND x MD scenario and the actual dimensions will be extracted
    regardless due to necessity.
    """

    if not dims or dims[0] > 2 or dims[1] > 2:
        shape_a = shape(a)
        shape_b = shape(b)
        dims_a = len(shape_a)
        dims_b = len(shape_b)

        # Handle matrices of N-D and M-D size
        if dims_a > 2 or dims_b > 2:
            if dims_a == dims_b:
                # Apply math to two N-D matrices
                return cast(
                    MutableMatrix,
                    reshape([op(x, y) for x, y in zip(flatiter(cast(Array, a)), flatiter(cast(Array, b)))], shape_a)
                )
            elif not dims_a or not dims_b:
                if not dims_a:
                    # Apply math to a number and an N-D matrix
                    return cast(MutableMatrix, reshape([op(a, x) for x in flatiter(cast(Array, b))], shape_b))
                # Apply math to an N-D matrix and a number
                return cast(MutableMatrix, reshape([op(x, b) for x in flatiter(cast(Array, a))], shape_a))

            # Apply math to an N-D matrix and an M-D matrix by broadcasting to a common shape.
            bcast = broadcast(cast(Array, a), cast(Array, b))
            return cast(MutableMatrix, reshape([op(x, y) for x, y in bcast], bcast.shape))
    else:
        dims_a, dims_b = dims

    # Inputs are of equal size and shape
    if dims_a == dims_b:
        if dims_a == 1:
            # Apply math to two vectors
            return _vector_math(op, cast(Vector, a), cast(Vector, b))
        elif dims_a == 2:
            # Apply math to two 2-D matrices
            return cast(MutableMatrix, [_vector_math(op, ra, rb) for ra, rb in zipl(cast(Matrix, a), cast(Matrix, b))])
        return op(a, b)

    # Inputs containing a scalar on either side
    elif not dims_a or not dims_b:
        if dims_a == 1:
            # Apply math to a vector and number
            return cast(MutableVector, [op(i, cast(float, b)) for i in cast(Vector, a)])
        elif dims_b == 1:
            # Apply math to a number and a vector
            return cast(MutableVector, [op(cast(float, a), i) for i in cast(Vector, b)])
        elif dims_a == 2:
            # Apply math to 2-D matrix and number
            return cast(MutableVector, [[op(i, cast(float, b)) for i in row] for row in cast(Matrix, a)])
        # Apply math to a number and a matrix
        return cast(MutableVector, [[op(cast(float, a), i) for i in row] for row in cast(Matrix, b)])

    # Inputs are at least 2-D dimensions or below on both sides
    if dims_a == 1:
        # Apply math to vector and 2-D matrix
        return cast(MutableMatrix, [_vector_math(op, cast(Vector, a), row) for row in cast(Matrix, b)])
    # Apply math to 2-D matrix and a vector
    return cast(MutableMatrix, [_vector_math(op, row, cast(Vector, b)) for row in cast(Matrix, a)])


def divide(
    a: Union[float, Array],
    b: Union[float, Array],
    dims: Optional[Tuple[int, int]] = None
) -> Union[float, MutableArray]:
    """Divide simple numbers, vectors, and 2D matrices."""

    return _math(operator.truediv, a, b, dims)


def multiply(
    a: Union[float, Array],
    b: Union[float, Array],
    dims: Optional[Tuple[int, int]] = None
) -> Union[float, MutableArray]:
    """Multiply simple numbers, vectors, and 2D matrices."""

    return _math(operator.mul, a, b, dims)


def add(
    a: Union[float, Array],
    b: Union[float, Array],
    dims: Optional[Tuple[int, int]] = None
) -> Union[float, MutableArray]:
    """Add simple numbers, vectors, and 2D matrices."""

    return _math(operator.add, a, b, dims)


def subtract(
    a: Union[float, Array],
    b: Union[float, Array],
    dims: Optional[Tuple[int, int]] = None
) -> Union[float, MutableArray]:
    """Subtract simple numbers, vectors, and 2D matrices."""

    return _math(operator.sub, a, b, dims)


class BroadcastTo:
    """
    Broadcast to a shape.

    By flattening the data, we are able to slice out the bits we need in the order we need
    and duplicate them to expand the matrix to fit the provided shape.

    We need 4 things to do this:
    - The original array.
    - The original array shape.
    - The stage 1 array shape (with prepended 1s). This helps us calculate our loop iterations.
    - The new shape.
    """

    def __init__(self, array: Array, orig: Tuple[int, ...], old: Tuple[int, ...], new: Tuple[int, ...]) -> None:
        """Initialize."""

        self._loop1 = 0
        self._loop2 = 0
        self._chunk_subindex = 0
        self._chunk_max = 0
        self._chunk_index = 0
        self._chunk = []  # type: List[float]

        # Unravel the data as it will be quicker to slice the data in a flattened form
        # than iterating over the dimensions to replicate the data.
        self.data = ravel(array)
        self.shape = new

        # Is the new shape actually different than the original?
        self.different = old != new

        if self.different:
            # Calculate the shape of the data.
            if len(old) > 1:
                self.amount = prod(old[:-1])
                self.length = old[-1]
            else:
                # Vectors have to be handled a bit special as they only have 1-D
                self.amount = old[-1]
                self.length = 1

            # Calculate how many times we should replicate data both horizontally and vertically
            # We need to flip them based on whether the original shape has an even or odd number of
            # dimensions.
            delta_rank = len(new) - len(old)
            counters = [int(x / y) if y else y for x, y in zip(new[delta_rank:], old)]
            repeat = prod(counters[:-1]) if len(old) > 1 else 1
            expand = counters[-1]
            if len(orig) % 2:
                self.expand = repeat
                self.repeat = expand
            else:
                self.expand = expand
                self.repeat = repeat
        else:
            # There is no modifications that need to be made on this array,
            # So we'll be chunking it without any cleverness.
            self.amount = len(self.data)
            self.length = 1
            self.expand = 1
            self.repeat = 1

        self.reset()

    def reset(self) -> None:
        """Reset."""

        # Setup and return the iterator.
        self._loop1 = self.repeat
        self._loop2 = self.expand
        self._chunk_subindex = 0
        self._chunk_max = self.amount * self.length
        self._chunk_index = 0
        self._chunk = self._chunk_data()

    def _chunk_data(self) -> List[float]:
        """Chunk the source data using are pre-calculated understanding of data amounts and length."""

        return self.data[self._chunk_index:self._chunk_index + self.length]

    def __next__(self) -> float:
        """Next."""

        if self._loop1:
            # Get the data.
            d = self._chunk[self._chunk_subindex]

            self._chunk_subindex += 1
            if self._chunk_subindex >= self.length:
                # We've processed the entirety of the current chunk
                # Let's see if we need to process it again.
                self._loop2 -= 1
                self._chunk_subindex = 0
                if not self._loop2:
                    # We've finished processing this chunk, let's get the next.
                    self._chunk_index += self.length
                    self._loop2 = self.expand

                    if self._chunk_index >= self._chunk_max:
                        # We are actually at then of all the data, let's see
                        # if we need to process all the data again.
                        self._loop1 -= 1
                        if self._loop1:
                            # We need to keep going
                            self._chunk_index = 0
                            self._chunk = self._chunk_data()
                    else:
                        # Still not at the end of the data, so get the next chunk
                        self._chunk = self._chunk_data()

            # Return the current data
            return d

        # We have nothing more to give
        raise StopIteration

    def __iter__(self) -> Iterator[float]:
        """Return the broadcasted array, piece by piece."""

        return self


class Broadcast:
    """Broadcast."""

    def __init__(self, *arrays: Array) -> None:
        """Broadcast."""

        # Determine maximum dimensions
        shapes = []
        arrays2 = []
        max_dims = 0
        for a in arrays:
            arrays2.append([a] if not isinstance(a, Sequence) else a)
            s = shape(arrays2[-1])
            dims = len(s)
            if dims > max_dims:
                max_dims = dims
            shapes.append(s)

        # Adjust array shapes by padding out with '1's until matches max dimensions
        stage1_shapes = []
        for s in shapes:
            dims = len(s)
            if dims < max_dims:
                stage1_shapes.append(((1,) * (max_dims - dims)) + s)
            else:
                stage1_shapes.append(s)

        # Determine a common shape, if possible
        s2 = []
        for dim in zip(*stage1_shapes):
            maximum = max(dim)
            if not all([d == 1 or d == maximum for d in dim]):
                raise ValueError("Could not broadcast arrays as shapes are incompatible")
            s2.append(maximum)
        common = tuple(s2)

        # Create iterators to "broadcast to"
        self.iters = []
        for a, s0, s1 in zip(arrays2, shapes, stage1_shapes):
            self.iters.append(BroadcastTo(a, s0, s1, common))

        # I don't think this is done the same way as `numpy`.
        # But shouldn't matter for what we do.
        self.shape = common
        self.ndims = max_dims
        self.size = prod(common)
        self._init()

    def _init(self) -> None:
        """Setup main iterator."""

        self._iter = zipl(*self.iters)

    def reset(self) -> None:
        """Reset iterator."""

        # Reset all the child iterators.
        for i in self.iters:
            i.reset()
        self._init()

    def __next__(self) -> Tuple[float, float]:
        """Next."""

        # Get the next chunk of data
        return cast(Tuple[float, float], next(self._iter))

    def __iter__(self) -> 'Broadcast':
        """Iterate."""

        # Setup and and return the iterator.
        return self


def broadcast(*arrays: Array) -> Broadcast:
    """Broadcast."""

    return Broadcast(*arrays)


def broadcast_to(a: Array, s: Union[int, Sequence[int]]) -> MutableArray:
    """Broadcast array to a shape."""

    if not isinstance(s, Sequence):
        s = (s,)

    if not isinstance(a, Sequence):
        a = [a]

    s_orig = shape(a)
    ndim_orig = len(s_orig)
    ndim_target = len(s)
    if ndim_orig > ndim_target:
        raise ValueError("Cannot broadcast {} to {}".format(s_orig, s))

    s1 = list(s_orig)
    if ndim_orig < ndim_target:
        s1 = ([1] * (ndim_target - ndim_orig)) + s1

    for d1, d2 in zip(s1, s):
        if d1 != d2 and (d1 != 1 or d1 > d2):
            raise ValueError("Cannot broadcast {} to {}".format(s_orig, s))

    return cast(MutableArray, reshape(list(BroadcastTo(a, s_orig, tuple(s1), tuple(s))), s))


def full(array_shape: Union[int, Sequence[int]], fill_value: Union[float, Array]) -> MutableArray:
    """Create and fill a shape with the given values."""

    # Ensure `shape` is a sequence of sizes
    array_shape = tuple([array_shape]) if not isinstance(array_shape, Sequence) else tuple(array_shape)

    # Normalize `fill_value` to be an array.
    if not isinstance(fill_value, Sequence):
        return cast(MutableArray, reshape([fill_value] * prod(array_shape), array_shape))

    # If the shape doesn't fit the data, try and broadcast it.
    # If it does fit, just reshape it.
    if shape(fill_value) != tuple(array_shape):
        return broadcast_to(fill_value, array_shape)
    return cast(MutableArray, reshape(fill_value, array_shape))


def ones(array_shape: Union[int, Sequence[int]]) -> MutableArray:
    """Create and fill a shape with ones."""

    return full(array_shape, 1.0)


def zeros(array_shape: Union[int, Sequence[int]]) -> MutableArray:
    """Create and fill a shape with zeros."""

    return full(array_shape, 0.0)


def identity(size: int) -> MutableMatrix:
    """Create an identity matrix."""

    return cast(MutableMatrix, diag([1.0] * size))


def _flatiter(array: Array, array_shape: Tuple[int, ...]) -> Iterator[float]:
    """Iterate and return values based on shape."""

    nested = len(array_shape) > 1
    for a in array:
        if nested:
            yield from _flatiter(cast(Array, a), array_shape[1:])
        elif isinstance(a, Sequence):
            raise ValueError('Ragged arrays are not supported')
        else:
            yield a


def flatiter(array: Array) -> Iterator[float]:
    """Traverse an array returning values."""

    yield from _flatiter(array, shape(array))


def ravel(array: Array) -> MutableVector:
    """Return a flattened vector."""

    return list(flatiter(array))


def _frange(start: float, stop: float, step: float) -> Iterator[float]:
    """Float range."""

    x = start
    rev = step < 0.0
    limit = stop - step
    while x >= limit if rev else x <= limit:
        yield x
        x += step


def arange(
    start: SupportsFloatOrInt,
    stop: Optional[SupportsFloatOrInt] = None,
    step: SupportsFloatOrInt = 1
) -> MutableVector:
    """
    Like arrange, but handles floats as well.

    Return will be a list instead of an iterator.
    Due to floating point precision, floats may be inaccurate to some degree.
    """

    if stop is None:
        stop = start
        start = 0

    if isinstance(start, int) and isinstance(stop, int) and isinstance(step, int):
        return list(range(start, stop, step))
    else:
        return list(_frange(float(start), float(stop), float(step)))


def transpose(array: Array) -> MutableArray:
    """
    A simple transpose of a matrix.

    `numpy` offers the ability to specify different axes, but right now,
    we don't have a need for that, nor the desire to figure it out :).
    """

    s = list(reversed(shape(array)))
    total = prod(cast(Iterator[int], s))

    # Create the array
    m = []  # type: Any

    # Calculate data sizes
    dims = len(s)
    length = s[-1]

    # Initialize indexes so we can properly write our data
    idx = [0] * dims

    # Traverse the provided array filling our new array
    for i, v in enumerate(flatiter(array), 0):

        # Navigate to the proper index to start writing data.
        # If the dimension hasn't been created yet, create it.
        t = m  # type: Any
        for d, x in enumerate(range(dims - 1)):
            if not t:
                for _ in range(s[d]):
                    t.append([])
            t = cast(MutableArray, t[idx[x]])

        # Initialize the last dimension
        # so we can index at the correct position
        if not t:
            t[:] = [0] * length

        # Write the data
        t[idx[-1]] = v

        # Update the current indexes if we aren't done copying data.
        if i < (total - 1):
            for x in range(dims):
                if (idx[x] + 1) % s[x] == 0:
                    idx[x] = 0
                    x += 1
                else:
                    idx[x] += 1
                    break

    return cast(MutableArray, m)


def reshape(array: Array, new_shape: Union[int, Sequence[int]]) -> Union[float, Array]:
    """Change the shape of an array."""

    # Normalize shape specifier to a sequence
    if not isinstance(new_shape, Sequence):
        new_shape = [new_shape]

    # Shape to a scalar
    if not new_shape:
        v = ravel(array)
        if len(v) == 1 and not isinstance(v[0], Sequence):
            return v[0]
        else:
            raise ValueError('Shape {} does not match the data total of {}'.format(new_shape, shape(array)))

    # Kick out if the requested shape doesn't match the data
    total = prod(cast(Iterator[int], new_shape))
    if total != prod(shape(array)):
        raise ValueError('Shape {} does not match the data total of {}'.format(new_shape, shape(array)))

    # Create the array
    m = []  # type: Any

    # Calculate data sizes
    dims = len(new_shape)
    length = new_shape[-1]
    count = int(total // length)

    # Initialize indexes so we can properly write our data
    idx = [0] * (dims - 1)

    # Traverse the provided array filling our new array
    data = flatiter(array)
    for i in range(count):

        # Navigate to the proper index to start writing data.
        # If the dimension hasn't been created yet, create it.
        t = m  # type: Any
        for d, x in enumerate(range(dims - 1)):
            if not t:
                for _ in range(new_shape[d]):
                    t.append([])
            t = cast(MutableArray, t[idx[x]])

        # Create the final dimension, writing all the data
        t[:] = [next(data) for _ in range(length)]

        # Update the current indexes if we aren't done copying data.
        if i < (count - 1):
            for x in range(-1, -(dims), -1):
                if idx[x] + 1 == new_shape[x - 1]:
                    idx[x] = 0
                    x += -1
                else:
                    idx[x] += 1
                    break

    return cast(MutableArray, m)


def _shape(array: Array, size: int) -> Tuple[int, ...]:
    """Iterate the array ensuring that all dimensions are consistent and return the sizes if they are."""

    s = (size,)
    s2 = tuple()  # type: Tuple[int, ...]
    size2 = -1
    deeper = True
    for a in array:
        if not isinstance(a, Sequence) or size != len(a):
            return tuple()
        elif deeper:
            if a and isinstance(a[0], Sequence):
                if size2 < 0:
                    size2 = len(a[0])
                s2 = _shape(a, size2)
                if not s2:
                    break
            else:
                deeper = False
                s2 = tuple()
    return s + s2 if s2 else s


def shape(array: Union[float, Array]) -> Tuple[int, ...]:
    """Get the shape of an array."""

    if isinstance(array, Sequence):
        s = (len(array),)
        if not s[0]:
            return tuple()
        elif not isinstance(array[0], Sequence):
            return tuple(s)
        return s + _shape(array, len(array[0]))
    else:
        return tuple()


def fill_diagonal(matrix: MutableMatrix, val: Union[float, Array] = 0.0, wrap: bool = False) -> None:
    """Fill an N-D matrix diagonal."""

    s = shape(matrix)
    if len(s) < 2:
        raise ValueError('Arrays must be 2D or greater')
    if len(s) != 2:
        wrap = False
        if min(s) != max(s):
            raise ValueError('Arrays larger than 2D must have all dimensions of equal length')

    val = [val] if not isinstance(val, Sequence) else ravel(val)
    mx = max(s)
    dlast = len(s) - 1
    dlen = len(val) - 1
    pos = 0

    x = [0] * len(s)
    while x[0] < mx:
        t = matrix  # type: Any
        for idx in range(len(s)):
            r = s[idx]
            current = x[idx]
            if current < r:
                if idx == dlast:
                    t[current] = val[pos]
                else:
                    t = t[current]
                x[idx] += 1
            elif wrap and idx and current == r:
                x[idx] = 0
            else:
                x[0] = mx
                break

        pos = pos + 1 if pos < dlen else 0


def diag(array: Array, k: int = 0) -> MutableArray:
    """Create a diagonal matrix from a vector or return a vector of the diagonal of a matrix."""
    s = shape(array)
    dims = len(s)
    if not dims or dims > 2:
        raise ValueError('Array must be 1-D or 2-D in shape')

    if dims == 1:
        # Calculate size of matrix to accommodate the diagonal
        size = s[0] - k if k < 0 else s[0] + k if k else s[0]
        maximum = size - 1
        minimum = 0

        # Create a diagonal matrix with the provided vector
        m = []  # type: MutableMatrix
        for i in range(size):
            pos = i + k
            idx = i if k >= 0 else pos
            m.append(
                ([0.0] * clamp(pos, minimum, maximum)) +
                [cast(float, array[idx]) if (0 <= pos < size) else 0.0] +
                ([0.0] * clamp(size - pos - 1, minimum, maximum))
            )
        return m
    else:
        # Extract the requested diagonal from a rectangular 2-D matrix
        size = s[1]
        d = []
        for i, r in enumerate(array):
            pos = i + k
            if (0 <= pos < size):
                d.append(cast(Vector, r)[pos])
        return d


def inv(matrix: Matrix) -> MutableMatrix:
    """
    Invert the matrix.

    Derived from https://github.com/ThomIves/MatrixInverse.

    This is free and unencumbered software released into the public domain.

    Anyone is free to copy, modify, publish, use, compile, sell, or
    distribute this software, either in source code form or as a compiled
    binary, for any purpose, commercial or non-commercial, and by any
    means.

    In jurisdictions that recognize copyright laws, the author or authors
    of this software dedicate any and all copyright interest in the
    software to the public domain. We make this dedication for the benefit
    of the public at large and to the detriment of our heirs and
    successors. We intend this dedication to be an overt act of
    relinquishment in perpetuity of all present and future rights to this
    software under copyright law.

    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
    EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
    MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
    IN NO EVENT SHALL THE AUTHORS BE LIABLE FOR ANY CLAIM, DAMAGES OR
    OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
    ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
    OTHER DEALINGS IN THE SOFTWARE.

    For more information, please refer to <http://unlicense.org/>

    ---

    Modified to handle greater than 2 x 2 dimensions.
    """

    # Ensure we have a square matrix
    s = shape(matrix)
    dims = len(s)
    if dims < 2 or min(s) != max(s):
        raise ValueError('Matrix must be a N x N matrix')

    # Handle dimensions greater than 2 x 2
    elif dims > 2:
        invert = []
        cols = list(_extract_dimension(matrix, dims - 2))
        for c in cols:
            invert.append(transpose(inv(cast(MutableMatrix, c))))
        return cast(MutableMatrix, reshape(cast(MutableMatrix, invert), s))

    indices = list(range(s[0]))
    m = [list(x) for x in matrix]

    # Create an identity matrix of the same size as our provided vector
    im = cast(List[List[float]], diag([1] * s[0]))

    # Iterating through each row, we will scale each row by it's "focus diagonal".
    # Then using the scaled row, we will adjust the other rows.
    # ```
    # [[fd, 0,  0 ]
    #  [0,  fd, 0 ]
    #  [0,  0,  fd]]
    # ```
    for fd in indices:
        # We will divide each value in the row by the "focus diagonal" value.
        # If the we have a zero for the given `fd` value, we cannot invert.
        denom = m[fd][fd]
        if denom == 0:
            raise ValueError('Matrix is not invertable')

        # We are converting the matrix to the identity and vice versa,
        # So scale the diagonal such that it will now equal 1.
        # Additionally, the same operations will be applied to the identity matrix
        # and will turn it into `m ** -1` (what we are looking for)
        fd_scalar = 1.0 / denom
        for j in indices:
            m[fd][j] *= fd_scalar
            im[fd][j] *= fd_scalar

        # Now, using the value found at the index `fd` in the remaining rows (excluding `row[fd]`),
        # Where `cr` is the current row under evaluation, subtract `row[cr][fd] * row[fd] from row[cr]`.
        for cr in indices[0:fd] + indices[fd + 1:]:
            # The scalar for the current row
            cr_scalar = m[cr][fd]

            # Scale each item in the `row[fd]` and subtract it from the current row `row[cr]`
            for j in indices:
                m[cr][j] -= cr_scalar * m[fd][j]
                im[cr][j] -= cr_scalar * im[fd][j]

    # The identify matrix is now the inverse matrix and vice versa.
    return im


def vstack(arrays: Tuple[Array, ...]) -> MutableArray:
    """Vertical stack."""

    m = []  # type: List[MutableArray]
    first = True
    dims = 0
    for i in arrays:
        cs = shape(i)
        if first:
            dims = len(cs)
            first = False
            if dims == 0:
                return cast(MutableArray, reshape(cast(Vector, arrays), (len(arrays), 1)))
            elif dims == 1:
                return cast(MutableArray, reshape(cast(Matrix, arrays), (len(arrays), cs[-1])))
        m.append(cast(MutableArray, reshape(i, (prod(cs[:1 - dims]),) + cs[1 - dims:-1] + cs[-1:])))

    if first:
        raise ValueError("'vstack' requires at least one array")

    return sum(cast(Iterable[MutableArray], m), cast(MutableArray, []))


def _hstack_extract(a: MutableArray, s: Tuple[int, ...]) -> Iterator[MutableVector]:
    """Extract data from the second dimension."""

    data = flatiter(a)
    length = prod(s[1:])
    for _ in range(s[0]):
        yield [next(data) for _ in range(length)]


def hstack(arrays: Tuple[Array, ...]) -> MutableArray:
    """Horizontal stack."""

    # Gather up shapes
    columns = 0
    shapes = []
    first = None  # type: Optional[Tuple[int, ...]]
    for a in arrays:
        cs = shape(a)

        # Shortcut out for simple list of numbers or 1-D arrays
        if first is None:
            first = cs
            if not cs:
                return cast(MutableArray, reshape(cast(Vector, arrays), (len(arrays),)))
            elif len(cs) == 1:
                m1 = []  # type: MutableVector
                for a1 in arrays:
                    m1.extend(ravel(a1))
                return cast(MutableArray, reshape(m1, (len(m1),)))

        # Gather up shapes and tally the size of the new second dimension
        columns += cs[1]
        shapes.append(cs)

    if first is None:
        raise ValueError("'hstack' requires at least one array")

    # Iterate the arrays returning the content per second dimension
    m = []  # type: List[MutableArray]
    for data in zipl(*[_hstack_extract(a, s) for a, s in zipl(arrays, shapes)]):
        m.extend(sum(data, []))

    # Shape the data to the new shape
    new_shape = first[:1] + tuple([columns]) + first[2:]
    return cast(MutableArray, reshape(cast(MutableArray, m), new_shape))


def outer(a: Union[float, Array], b: Union[float, Array]) -> MutableMatrix:
    """Compute the outer product of two vectors (or flattened matrices)."""

    v1 = ravel(a) if isinstance(a, Sequence) else [a]
    v2 = ravel(b) if isinstance(b, Sequence) else [b]
    return [[x * y for y in v2] for x in v1]


def inner(a: Union[float, Array], b: Union[float, Array]) -> Union[float, Array]:
    """Compute the inner product of two arrays."""

    shape_a = shape(a)
    shape_b = shape(b)
    dims_a = len(shape_a)
    dims_b = len(shape_b)

    # If both inputs are not scalars, the last dimension must match
    if (shape_a and shape_b and shape_a[-1] != shape_b[-1]):
        raise ValueError('The last dimensions {} and {} do not match'.format(shape_a, shape_b))

    # If we have a scalar, we should just multiply
    if (not dims_a or not dims_b):
        return multiply(a, b, (dims_a, dims_b))

    # Adjust the input so that they can properly be evaluated
    # Scalars will be broadcasted to properly match the last dimension
    # of the other input.
    if dims_a == 1:
        first = [a]  # type: Any
    elif dims_a > 2:
        first = list(_extract_dimension(cast(Array, a), dims_a - 1))
    else:
        first = a

    if dims_b == 1:
        second = [b]  # type: Any
    elif dims_b > 2:
        second = list(_extract_dimension(cast(Array, b), dims_b - 1))
    else:
        second = b

    # Perform the actual inner product
    m = [[sum([x * y for x, y in zipl(cast(Vector, r1), cast(Vector, r2))]) for r2 in second] for r1 in first]
    new_shape = shape_a[:-1] + shape_b[:-1]

    # Shape the data.
    return reshape(m, new_shape)