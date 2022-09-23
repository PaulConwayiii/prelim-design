import numpy as np


def main():
    r_E = 6371000  # m
    alt = 35786 * 1000  # m

    r_O = r_E + alt

    arc = 2 * r_O * np.arcsin(r_E / (2 * r_O))

    circum = 2 * np.pi * r_O

    orbit_in_sun = 100 * (circum - arc) / circum

    print(orbit_in_sun)


if __name__ == "__main__":
    main()
