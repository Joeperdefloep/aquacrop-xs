import numpy as np
import xsimlab as xs


@xs.process
class Crop:
    pass


@xs.process
class Soil:
    """
    Class that contains soil parameters. These can vary in x,y,z directions, but
    not in time.

    **variables**:


    """

    curve_number = xs.variable(
        dims=[("x", "y", "z"), ("x", "z"), ("z")],
        intent="inout",
        description="Curve number for runoff calculations",
        attrs={"units": "-"},
    )

    th_wp = xs.variable(dims=[("x", "y", "z"), ("x", "z"), ("z")], intent="in")
    th_fc = xs.variable(dims=[("x", "y", "z"), ("x", "z"), ("z")], intent="in")
    th_sat = xs.variable(dims=[("x", "y", "z"), ("x", "z"), ("z")], intent="in")
    k_sat = xs.variable(dims=[("x", "y", "z"), ("x", "z"), ("z")], intent="in")


@xs.process
class SoilFromTexture:
    """
    Class that determines soiltypes for :class:`Soil` based on structural
    parameters. Based on Saxton and Rawls (2006): *Soil Water Characteristic
    Estimates by Texture and Organic Matter for Hydrologic Solutions*. In the
    paper, organic matter should be transfer
    """

    sand = xs.variable(
        dims=[("x", "y", "z"), ("x", "z"), "z"],
        intent="in",
        description="Volumetric Sand content",
    )
    clay = xs.variable(
        dims=[("x", "y", "z"), ("x", "z"), "z"],
        intent="in",
        description="Volumetric Clay content",
    )
    organic_matter = xs.variable(
        dims=[("x", "y", "z"), ("x", "z"), "z"],
        intent="in",
        description="Organic matter content",
    )

    th_wp = xs.foreign(Soil, var_name="th_wp", intent="out")
    th_fc = xs.foreign(Soil, var_name="th_fc", intent="out")
    th_sat = xs.foreign(Soil, var_name="th_sat", intent="out")
    k_sat = xs.foreign(Soil, var_name="k_sat", intent="out")

    th_wp_t = xs.variable(dims="z", intent="out")

    def initialize(self):
        # calculate wilting point
        self.th_wp_t = (
            -0.024 * self.sand
            + 0.487 * self.clay
            + 0.6 * self.organic_matter
            + 0.5 * self.sand * self.organic_matter
            - 1.3 * self.clay * self.organic_matter
            + 0.068 * self.sand * self.clay
            + 0.031
        )
        self.th_wp = self.th_wp_t + 0.14 * self.th_wp_t - 0.02
        # calculate field capacity
        th_fc_t = (
            -0.251 * self.sand
            + 0.195 * self.clay
            + 1.1 * self.organic_matter
            + 0.6 * self.sand * self.organic_matter
            - 2.7 * self.clay * self.organic_matter
            + 0.452 * self.sand * self.clay
            + 0.299
        )
        self.th_fc = th_fc_t + 1.283 * th_fc_t ** 2 - 0.374 * th_fc_t - 0.015
        # calculate S-FC moisture content
        th_s_fc_t = (
            0.278 * self.sand
            + 0.034 * self.clay
            + 2.2 * self.organic_matter
            - 1.8 * self.sand * self.organic_matter
            - 2.7 * self.clay * self.organic_matter
            - 0.584 * self.sand * self.clay
            + 0.078
        )
        th_s_fc = th_s_fc_t + (0.636 * th_s_fc_t - 0.107)
        # calculate Saturation moisture content
        self.th_sat = self.th_fc + th_s_fc - 0.097 * self.sand + 0.043
        # calculate
        B = (np.log(1500) - np.log(33)) / (np.log(self.th_fc) - np.log(self.th_wp))
        # A = np.exp(np.log(33) + B * np.log(self.th_fc))

        lmbda = 1 / B
        self.k_sat = 1930 * (self.th_sat - self.th_fc) ** (3 - lmbda)
