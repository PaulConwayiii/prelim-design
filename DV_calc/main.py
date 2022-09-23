import numpy as np # type: ignore
import modules.Orbit as Orb


def main() -> None:
    orbit_1 = Orb.Orbit(0, 35786 * 1000)
    orbit_1.hohmann_transfer(Orb.Orbit(0, orbit_1.alt + 1000 * 1000))

    print(orbit_1.dv)


if __name__ == "__main__":
    main()
