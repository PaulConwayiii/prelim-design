import numpy as np  # type: ignore
import modules.Orbit as Orb


def main() -> None:
    orbit_1 = Orb.Orbit(0, 35786 * 1000)
    orbit_1.hohmann_transfer(Orb.Orbit(0, orbit_1.alt + 1000 * 1000))

    print(orbit_1.dv)
    print(orbit_1.get_period() / (60 * 60))
    print(orbit_1.get_day_time() / (60 * 60))
    print(orbit_1.get_night_time() / (60))


if __name__ == "__main__":
    main()
