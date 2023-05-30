"""Color matching functions."""

# CIE 1931 2 degree observer
# http://www-cvrl.ucsd.edu/cmfs.htm
cie_2_deg_observer = {
    360: (0.0001299, 0.000003917, 0.0006061),
    365: (0.0002321, 0.000006965, 0.001086),
    370: (0.0004149, 0.00001239, 0.001946),
    375: (0.0007416, 0.00002202, 0.003486),
    380: (0.001368, 0.000039, 0.006450001),
    385: (0.002236, 0.000064, 0.01054999),
    390: (0.004243, 0.00012, 0.02005001),
    395: (0.00765, 0.000217, 0.03621),
    400: (0.01431, 0.000396, 0.06785001),
    405: (0.02319, 0.00064, 0.1102),
    410: (0.04351, 0.00121, 0.2074),
    415: (0.07763, 0.00218, 0.3713),
    420: (0.13438, 0.004, 0.6456),
    425: (0.21477, 0.0073, 1.0390501),
    430: (0.2839, 0.0116, 1.3856),
    435: (0.3285, 0.01684, 1.62296),
    440: (0.34828, 0.023, 1.74706),
    445: (0.34806, 0.0298, 1.7826),
    450: (0.3362, 0.038, 1.77211),
    455: (0.3187, 0.048, 1.7441),
    460: (0.2908, 0.06, 1.6692),
    465: (0.2511, 0.0739, 1.5281),
    470: (0.19536, 0.09098, 1.28764),
    475: (0.1421, 0.1126, 1.0419),
    480: (0.09564, 0.13902, 0.8129501),
    485: (0.05795001, 0.1693, 0.6162),
    490: (0.03201, 0.20802, 0.46518),
    495: (0.0147, 0.2586, 0.3533),
    500: (0.0049, 0.323, 0.272),
    505: (0.0024, 0.4073, 0.2123),
    510: (0.0093, 0.503, 0.1582),
    515: (0.0291, 0.6082, 0.1117),
    520: (0.06327, 0.71, 0.07824999),
    525: (0.1096, 0.7932, 0.05725001),
    530: (0.1655, 0.862, 0.04216),
    535: (0.2257499, 0.9148501, 0.02984),
    540: (0.2904, 0.954, 0.0203),
    545: (0.3597, 0.9803, 0.0134),
    550: (0.4334499, 0.9949501, 0.008749999),
    555: (0.5120501, 1.0, 0.005749999),
    560: (0.5945, 0.995, 0.0039),
    565: (0.6784, 0.9786, 0.002749999),
    570: (0.7621, 0.952, 0.0021),
    575: (0.8425, 0.9154, 0.0018),
    580: (0.9163, 0.87, 0.001650001),
    585: (0.9786, 0.8163, 0.0014),
    590: (1.0263, 0.757, 0.0011),
    595: (1.0567, 0.6949, 0.001),
    600: (1.0622, 0.631, 0.0008),
    605: (1.0456, 0.5668, 0.0006),
    610: (1.0026, 0.503, 0.00034),
    615: (0.9384, 0.4412, 0.00024),
    620: (0.8544499, 0.381, 0.00019),
    625: (0.7514, 0.321, 0.0001),
    630: (0.6424, 0.265, 0.00004999999),
    635: (0.5419, 0.217, 0.00003),
    640: (0.4479, 0.175, 0.00002),
    645: (0.3608, 0.1382, 0.00001),
    650: (0.2835, 0.107, 0.0),
    655: (0.2187, 0.0816, 0.0),
    660: (0.1649, 0.061, 0.0),
    665: (0.1212, 0.04458, 0.0),
    670: (0.0874, 0.032, 0.0),
    675: (0.0636, 0.0232, 0.0),
    680: (0.04677, 0.017, 0.0),
    685: (0.0329, 0.01192, 0.0),
    690: (0.0227, 0.00821, 0.0),
    695: (0.01584, 0.005723, 0.0),
    700: (0.01135916, 0.004102, 0.0),
    705: (0.008110916, 0.002929, 0.0),
    710: (0.005790346, 0.002091, 0.0),
    715: (0.004106457, 0.001484, 0.0),
    720: (0.002899327, 0.001047, 0.0),
    725: (0.00204919, 0.00074, 0.0),
    730: (0.001439971, 0.00052, 0.0),
    735: (0.0009999493, 0.0003611, 0.0),
    740: (0.0006900786, 0.0002492, 0.0),
    745: (0.0004760213, 0.0001719, 0.0),
    750: (0.0003323011, 0.00012, 0.0),
    755: (0.0002348261, 0.0000848, 0.0),
    760: (0.0001661505, 0.00006, 0.0),
    765: (0.000117413, 0.0000424, 0.0),
    770: (0.00008307527, 0.00003, 0.0),
    775: (0.00005870652, 0.0000212, 0.0),
    780: (0.00004150994, 0.00001499, 0.0),
    785: (0.00002935326, 0.0000106, 0.0),
    790: (0.00002067383, 0.0000074657, 0.0),
    795: (0.00001455977, 0.0000052578, 0.0),
    800: (0.00001025398, 0.0000037029, 0.0),
    805: (0.000007221456, 0.0000026078, 0.0),
    810: (0.000005085868, 0.0000018366, 0.0),
    815: (0.000003581652, 0.0000012934, 0.0),
    820: (0.000002522525, 0.00000091093, 0.0),
    825: (0.000001776509, 0.00000064153, 0.0),
    830: (0.000001251141, 0.00000045181, 0.0)
}

# CIE 1931 2 degree observer
# http://www-cvrl.ucsd.edu/cmfs.htm
cie_10_deg_observer = {
    360: (0.0000001222, 0.000000013398, 0.000000535027),
    365: (0.00000091927, 0.00000010065, 0.0000040283),
    370: (0.0000059586, 0.0000006511, 0.0000261437),
    375: (0.000033266, 0.000003625, 0.00014622),
    380: (0.000159952, 0.000017364, 0.000704776),
    385: (0.00066244, 0.00007156, 0.0029278),
    390: (0.0023616, 0.0002534, 0.0104822),
    395: (0.0072423, 0.0007685, 0.032344),
    400: (0.0191097, 0.0020044, 0.0860109),
    405: (0.0434, 0.004509, 0.19712),
    410: (0.084736, 0.008756, 0.389366),
    415: (0.140638, 0.014456, 0.65676),
    420: (0.204492, 0.021391, 0.972542),
    425: (0.264737, 0.029497, 1.2825),
    430: (0.314679, 0.038676, 1.55348),
    435: (0.357719, 0.049602, 1.7985),
    440: (0.383734, 0.062077, 1.96728),
    445: (0.386726, 0.074704, 2.0273),
    450: (0.370702, 0.089456, 1.9948),
    455: (0.342957, 0.106256, 1.9007),
    460: (0.302273, 0.128201, 1.74537),
    465: (0.254085, 0.152761, 1.5549),
    470: (0.195618, 0.18519, 1.31756),
    475: (0.132349, 0.21994, 1.0302),
    480: (0.080507, 0.253589, 0.772125),
    485: (0.041072, 0.297665, 0.5706),
    490: (0.016172, 0.339133, 0.415254),
    495: (0.005132, 0.395379, 0.302356),
    500: (0.003816, 0.460777, 0.218502),
    505: (0.015444, 0.53136, 0.159249),
    510: (0.037465, 0.606741, 0.112044),
    515: (0.071358, 0.68566, 0.082248),
    520: (0.117749, 0.761757, 0.060709),
    525: (0.172953, 0.82333, 0.04305),
    530: (0.236491, 0.875211, 0.030451),
    535: (0.304213, 0.92381, 0.020584),
    540: (0.376772, 0.961988, 0.013676),
    545: (0.451584, 0.9822, 0.007918),
    550: (0.529826, 0.991761, 0.003988),
    555: (0.616053, 0.99911, 0.001091),
    560: (0.705224, 0.99734, 0.0),
    565: (0.793832, 0.98238, 0.0),
    570: (0.878655, 0.955552, 0.0),
    575: (0.951162, 0.915175, 0.0),
    580: (1.01416, 0.868934, 0.0),
    585: (1.0743, 0.825623, 0.0),
    590: (1.11852, 0.777405, 0.0),
    595: (1.1343, 0.720353, 0.0),
    600: (1.12399, 0.658341, 0.0),
    605: (1.0891, 0.593878, 0.0),
    610: (1.03048, 0.527963, 0.0),
    615: (0.95074, 0.461834, 0.0),
    620: (0.856297, 0.398057, 0.0),
    625: (0.75493, 0.339554, 0.0),
    630: (0.647467, 0.283493, 0.0),
    635: (0.53511, 0.228254, 0.0),
    640: (0.431567, 0.179828, 0.0),
    645: (0.34369, 0.140211, 0.0),
    650: (0.268329, 0.107633, 0.0),
    655: (0.2043, 0.081187, 0.0),
    660: (0.152568, 0.060281, 0.0),
    665: (0.11221, 0.044096, 0.0),
    670: (0.0812606, 0.0318004, 0.0),
    675: (0.05793, 0.0226017, 0.0),
    680: (0.0408508, 0.0159051, 0.0),
    685: (0.028623, 0.0111303, 0.0),
    690: (0.0199413, 0.0077488, 0.0),
    695: (0.013842, 0.0053751, 0.0),
    700: (0.00957688, 0.00371774, 0.0),
    705: (0.0066052, 0.00256456, 0.0),
    710: (0.00455263, 0.00176847, 0.0),
    715: (0.0031447, 0.00122239, 0.0),
    720: (0.00217496, 0.00084619, 0.0),
    725: (0.0015057, 0.00058644, 0.0),
    730: (0.00104476, 0.00040741, 0.0),
    735: (0.00072745, 0.000284041, 0.0),
    740: (0.000508258, 0.00019873, 0.0),
    745: (0.00035638, 0.00013955, 0.0),
    750: (0.000250969, 0.000098428, 0.0),
    755: (0.00017773, 0.000069819, 0.0),
    760: (0.00012639, 0.000049737, 0.0),
    765: (0.000090151, 0.0000355405, 0.0),
    770: (0.0000645258, 0.000025486, 0.0),
    775: (0.000046339, 0.0000183384, 0.0),
    780: (0.0000334117, 0.000013249, 0.0),
    785: (0.000024209, 0.0000096196, 0.0),
    790: (0.0000176115, 0.0000070128, 0.0),
    795: (0.000012855, 0.0000051298, 0.0),
    800: (0.00000941363, 0.00000376473, 0.0),
    805: (0.000006913, 0.00000277081, 0.0),
    810: (0.00000509347, 0.00000204613, 0.0),
    815: (0.0000037671, 0.00000151677, 0.0),
    820: (0.00000279531, 0.00000112809, 0.0),
    825: (0.000002082, 0.00000084216, 0.0),
    830: (0.00000155314, 0.0000006297, 0.0)
}
