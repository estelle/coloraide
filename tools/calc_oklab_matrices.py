"""Calculate `oklab` matrices."""
import numpy as np

np.set_printoptions(precision=None, sign='-', floatmode='unique')

# Calculated using our own `calc_xyz_transform.py`
XYZ_TO_RGB = np.asfarray(
    [
        [3.2409699419045226, -1.537383177570094, -0.49861076029300355],
        [-0.9692436362808796, 1.8759675015077202, 0.04155505740717562],
        [0.055630079696993635, -0.2039769588889765, 1.0569715142428784]
    ]
)

SRGBL_TO_LMS = np.asfarray(
    [
        [0.4122214708, 0.5363325363, 0.0514459929],
        [0.2119034982, 0.6806995451, 0.1073969566],
        [0.0883024619, 0.2817188376, 0.6299787005]
    ]
)

LMS3_TO_OKLAB = np.asfarray(
    [
        [0.2104542553, 0.793617785, -0.0040720468],
        [1.9779984951, -2.428592205, 0.4505937099],
        [0.0259040371, 0.7827717662, -0.808675766]
    ]
)


if __name__ == "__main__":
    print('===== sRGB Linear => lms =====')
    print(SRGBL_TO_LMS)
    print('===== lms -> sRGB Linear =====')
    print(np.linalg.inv(SRGBL_TO_LMS))
    xyzd65_to_lms = np.dot(SRGBL_TO_LMS, XYZ_TO_RGB)
    print('===== XYZ D65 Linear => lms =====')
    print(xyzd65_to_lms)
    print('===== lms -> XYZ D65 =====')
    print(np.linalg.inv(xyzd65_to_lms))
    print('===== lms ** 1/3 -> Oklab =====')
    print(LMS3_TO_OKLAB)
    print('===== Oklab -> lms ** 1/3 =====')
    print(np.linalg.inv(LMS3_TO_OKLAB))
