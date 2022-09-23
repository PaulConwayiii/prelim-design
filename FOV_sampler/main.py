import numpy as np  # type: ignore
import pandas as pd
from random import random as rd
import time


def main() -> None:
    start_time = time.perf_counter()

    # Import data file
    catalog = pd.read_csv("tycho_RA_DEC_VT_ID.csv")

    # FOV deltas to test. Given as a tuple of RA and DEC tuples.
    # Each sub-tuple defines the RA and DEC FOV to test
    # Endpoints included
    deltas = ((2, 2), (1.5, 1.5), (1, 1), (0.5, 0.5))

    # Defines how many samples to take
    samples = 5000

    # Defines min and max DECs to test.
    # Defined in a similar way to deltas
    # Endpoints included
    # Note that there is some weirdness around -90 and 90 if the FOV passes through this
    dec_lims = ((-90, 90), (-60, 60), (-45, 45), (-30, 30), (-15, 15))

    # Magnitude thresholds when parsing data
    mags = (99, 12, 11, 10, 9, 8, 7, 6, 5, 4)

    # Looping for each declination range
    for i, limit in enumerate(dec_lims):
        print(
            f"Testing {i+1} of {len(dec_lims)} declination ranges: {limit[0]} to"
            f" {limit[1]} degrees"
        )

        # Initializing df to contain results
        rows = []
        for mag in mags:
            rows = rows + [f"VT <= {mag}"]
        columns = []
        for delta in deltas:
            columns = columns + [
                f"n_avg, ({delta[0]}, {delta[1]})",
                f"n_std, ({delta[0]}, {delta[1]})",
                f"n_min, ({delta[0]}, {delta[1]})",
                f"n_max, ({delta[0]}, {delta[1]})",
            ]
        results = pd.DataFrame(index=rows, columns=columns)

        # Filter catalog to only values within limit
        filtered_catalog = catalog[
            (catalog["DEmdeg"] >= limit[0]) & (catalog["DEmdeg"] <= limit[1])
        ]

        # Looping for each delta range
        for j, delta in enumerate(deltas):
            print(
                f"\tTesting {j+1} of {len(deltas)} FOV ranges: {delta[0]} by"
                f" {delta[1]} degrees"
            )

            # Initializing results values
            n_list = []
            for mag in mags:
                n_list = n_list + [np.zeros(samples)]

            # Looping for each sample
            print(f"\tTaking {samples} samples...")
            for sample in range(samples):
                # Generating a random point
                ra = rd() * 360  # From 0 to 360 degrees
                dec = (rd() - 0.5) * (limit[1] - limit[0])  # Within declination limit

                # Accounting for the fact that right ascension loops back around
                if ra + delta[0] > 360:
                    ra_loop = ra + delta[0] - 360
                else:
                    ra_loop = -1

                # declination looping around is not accounted for!

                # Sampling catalog for RA in range of FOV
                sampled_catalog = filtered_catalog[
                    (filtered_catalog["RAmdeg"] >= ra)
                    & (filtered_catalog["RAmdeg"] <= ra + delta[0])
                    | (filtered_catalog["RAmdeg"] <= ra_loop)
                ]
                # Sampling catalog for DEC in range of FOV
                sampled_catalog = sampled_catalog[
                    (sampled_catalog["DEmdeg"] >= dec)
                    & (sampled_catalog["DEmdeg"] <= dec + delta[1])
                ]

                # print(sampled_catalog.to_string())

                # Filtering each magnitude threshold
                for k, mag in enumerate(mags):
                    mag_filtered_sampled_catalog = sampled_catalog[
                        (sampled_catalog["VTmag"] <= mag)
                    ]
                    n_list[k][sample] = len(mag_filtered_sampled_catalog.index)

            # Calculating results and saving results for each magnitude type
            for k, mag in enumerate(mags):
                results.loc[
                    f"VT <= {mag}", f"n_avg, ({delta[0]}, {delta[1]})"
                ] = np.average(n_list[k])
                results.loc[
                    f"VT <= {mag}", f"n_std, ({delta[0]}, {delta[1]})"
                ] = np.std(n_list[k])
                results.loc[
                    f"VT <= {mag}", f"n_min, ({delta[0]}, {delta[1]})"
                ] = np.min(n_list[k])
                results.loc[
                    f"VT <= {mag}", f"n_max, ({delta[0]}, {delta[1]})"
                ] = np.max(n_list[k])

        # Saving results to a file
        file_name = f"DEC_{limit[0]}_{limit[1]}.csv"
        results.to_csv(file_name)
        print(f"Results saved to: {file_name}\n")

    print(f"\nFinished in {time.perf_counter() - start_time:.2f} seconds")

    # Loop import data for n times
    # for each loop, find a random point (p)
    # Define FOV based on F_d and p (F)
    # Loop through all import data, if I_x and I_y in F
    # Add I_x to Y
    # Add len(Y) to Z, set Y = []

    # Find average in Y

    # Write program to calculate best orbit, dv to retire, time in sun


if __name__ == "__main__":
    main()
