import numpy as np

import xsaquacrop as ac


def test_soil_from_structural_parameters():
    """
    Test whether the soil transfer functions are the same as in the table.
    """

    soil = ac.SoilFromTexture(
        sand=np.array([0.88, 0.8, 0.65, 0.4, 0.2, 0.1, 0.6, 0.3, 0.1, 0.1, 0.5, 0.25]),
        clay=np.array(
            [0.05, 0.05, 0.1, 0.2, 0.15, 0.05, 0.25, 0.35, 0.35, 0.45, 0.40, 0.5]
        ),
        organic_matter=0.025 * np.ones(12),
    )
    soil.initialize()

    print(np.round(soil.th_wp, 2))
    np.testing.assert_allclose(
        np.round(soil.th_wp, 2),
        np.array([5, 5, 8, 14, 11, 6, 17, 22, 22, 27, 25, 30]) * 0.01,
    )
    np.testing.assert_allclose(
        np.round(soil.th_fc, 2),
        np.array([10, 12, 18, 28, 31, 30, 27, 36, 38, 41, 36, 42]) * 0.01,
    )
    np.testing.assert_allclose(
        np.round(soil.th_sat, 2),
        np.array([46, 46, 45, 46, 48, 48, 43, 48, 51, 52, 44, 50]) * 0.01,
    )
    np.testing.assert_allclose(
        np.round(soil.k_sat, 1),
        np.array([108.1, 96.7, 50.3, 15.5, 16.1, 22.0, 11.3, 4.3, 5.7, 3.7, 1.4, 1.1]),
    )
