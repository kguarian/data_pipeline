from neurodsp.sim.periodic import sim_bursty_oscillation
from neurodsp.sim.aperiodic import sim_powerlaw
import numpy as np
import matplotlib.pyplot as plt


def create_new_cycles():
    freqs = [8, 10, 12, 15]

    mappings = {
        "sine": {"phase": 4, "asym": False, "cyc_kwargs": {}, "durations": [0.5]},
        "sawtooth": {
            "phase": 2,
            "asym": False,
            "cyc_kwargs": {
                "width": 0.5,
            },
            "durations": [0.1, 0.2, 0.3, 0.4, 0.5],
        },
    }
    asym_mappings = {
        "exponent": [1, 2, 3],
        "ratio": [0.5, 0.75, 1.0],
        "burst_prob_enter": [0.25, 0.5, 0.9],
        "burst_prob_exit": [0.2, 0.5, 0.75],
    }
    sigs = np.zeros(
        shape=(
            len(mappings)
            * len(asym_mappings["ratio"])
            * len(freqs)
            * len(asym_mappings["exponent"])
            * len(asym_mappings["burst_prob_enter"]),
            1000,
        )
    )

    from itertools import product

    parameters = product(
        range(len(mappings.keys())),
        range(len(asym_mappings["exponent"])),
        range(len(asym_mappings["ratio"])),
        range(len(asym_mappings["burst_prob_enter"])),
        range(len(freqs)),
    )
    keys = list(mappings.keys())
    ii = 0
    for n, i, j, k, l in parameters:
        asym = {
            "exponent": asym_mappings["exponent"][i],
            "ratio": asym_mappings["ratio"][j],
        }
        local_burst_params = {
            "enter_burst": asym_mappings["burst_prob_enter"][k],
            "leave_burst": asym_mappings["burst_prob_exit"][k],
        }
        sigs[
            ii
        ] = sim_bursty_oscillation(
            n_seconds=2,
            fs=500,
            freq=freqs[l],
            cycle=keys[n],
            phase="min",
            burst_params=local_burst_params,
            **mappings[keys[n]]["cyc_kwargs"],
        ) + asym[
            "ratio"
        ] * sim_powerlaw(
            n_seconds=2, fs=500, exponent=asym["exponent"]
        )
        ii += 1
    
    for i in range(len(sigs)):
        plt.figure()
        plt.plot(sigs[i])

    plt.show()
