import numpy as np  # type: ignore


class Orbit:
    """Class containing orbit info and orbital transfer methods"""

    # All units are in SI base units
    # mass: kg
    # distance: m
    # time: s
    # Force: N
    # Energy: J

    def __init__(self, e: float, alt: float, use_km=False):
        """Constructor for Orbit class

        Args:
            e (float): Eccentricity
            alt (float): Altitude above mean Earth radius (m)
            use_km (bool, optional): Inputs and Outputs are expressed in km. Defaults to False.

        Raises:
            NotImplementedError: If use_km is set to truthy value
        """
        if use_km:
            raise NotImplementedError("km inputs and outputs currently not supported")

        # Constants
        self.G = 6.6743015 * 10**-11  # m^3 kg^-1 s^-2
        self.mu = 3.9860044188 * 10**14  # m^3 s^-2
        self.r_E = 6371000  # m
        self.r_geo = 42164 * 1000  # m

        # User arguments
        self.e = 0  # Later I will add the ability to change between elliptical orbits
        self.alt = alt

        # Calculated values
        self.r = self.r_E + self.alt

        # Other properties
        self.dv = 0

    def hohmann_transfer(self, orbit):
        """Transfers current orbit to new orbit using Hohmann transfer

        Args:
            orbit (Orbit): Orbit class instance of destination orbit

        Raises:
            ValueError: Destination orbit eccentricity != 0
            NotImplementedError: Source orbit eccentricity != 0
        """

        if orbit.e != 0:
            raise ValueError(
                "Destination orbits for Hohmann transfers must be circular (e=0)"
            )

        if self.e != 0:
            raise NotImplementedError("Eccentric source orbit not supported")

        dv_1 = np.sqrt(self.mu / self.r) * (
            np.sqrt((2 * orbit.r) / (self.r + orbit.r)) - 1
        )  # from orbit 1 to transfer orbit
        dv_2 = np.sqrt(self.mu / orbit.r) * (
            1 - np.sqrt((2 * self.r) / (self.r + orbit.r))
        )  # From transfer orbit to destination orbit
        self.r = orbit.r
        self.dv = self.dv + dv_1 + dv_2

    def get_period(self) -> float:
        """Returns the period of the orbit

        Returns:
            float: time in seconds
        """

        return 2 * np.pi * np.sqrt(self.r**3 / self.mu)  # s

    def get_day_time(self) -> float:
        """Return the total time in orbit the sun is visible

        Returns:
            float: time in seconds
        """

        arc = 2 * self.r * np.arcsin(self.r_E / (2 * self.r))
        circum = 2 * np.pi * self.r
        day_time_factor = (circum - arc) / circum

        return self.get_period() * day_time_factor

    def get_night_time(self) -> float:
        """Return the total time in orbit the sun is not visible

        Returns:
            float: time in seconds
        """

        return self.get_period() - self.get_day_time()
