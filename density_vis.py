import pickle as pkl
import numpy as np
import json
import matplotlib.pyplot as plt
import matplotlib.patches as patches


def main():
    with open('pyssem/pyssem/utils/drag/dens_baseline_2000-2100.json', 'r') as file:
        base = json.load(file)
    with open('pyssem/pyssem/utils/drag/dens_SSP1-26_2000-2100.json', 'r') as file:
        ssp1 = json.load(file)
    with open('pyssem/pyssem/utils/drag/dens_SSP2-45_2000-2100.json', 'r') as file:
        ssp2 = json.load(file)
    with open('pyssem/pyssem/utils/drag/dens_SSP3-70_2000-2100.json', 'r') as file:
        ssp3 = json.load(file)

    alt = '600'     # altitude to plot data at
    years = list(ssp1.keys())
    basedens = [base[key][alt] for key in base]
    ssp1dens = [ssp1[key][alt] for key in ssp1]
    ssp2dens = [ssp2[key][alt] for key in ssp2]
    ssp3dens = [ssp3[key][alt] for key in ssp3]

    # plot atmospheric density data to confirm with Parker et al.
    alt = '550'         # plot data at 400km in altitude
    fig, ax = plt.subplots()
    # plot actual lines on top of patch
    ax.semilogy(range(0, len(years)),
                basedens, linestyle=':', color='k', label='Baseline', zorder=1)
    ax.semilogy(range(0, len(years)),
                ssp2dens, color='royalblue', label='SSP2-4.5', zorder=2)

    # create SSP bounds for SSP2 density
    ssp1dens = np.array([ssp1dens])
    ssp3dens = np.array([ssp3dens])
    x = np.array([list(range(0, len(years)))])
    vertices = np.concatenate((np.concatenate((x.T, np.flip(x, axis=1).T), axis=0), np.concatenate(
        (ssp1dens.T, np.flip(ssp3dens, axis=1).T), axis=0)), axis=1)
    ax.add_patch(patches.Polygon(vertices, closed=True,
                 ec=None, fc='lightsteelblue', label='Uncertainty', zorder=0))

    plt.annotate('Upper bound is SSP1-2.6', xy=(882, 1.21e-14), xytext=(608, 6.5e-15),
                 arrowprops=dict(fc='0.3', ec='0.3', arrowstyle='-|>'))
    plt.annotate('Lower bound is SSP3-7.0', xy=(882, 7.49e-15), xytext=(800, 5e-15),
                 arrowprops=dict(fc='0.3', ec='0.3', arrowstyle='-|>'))

    lims = ax.get_ylim()
    ax.add_patch(patches.Rectangle(
        (0, lims[1]), 283, lims[0]-lims[1], ec=None, fc='sandybrown', alpha=0.15, zorder=0, label='Historic Data'))

    ax.set_xlabel("Year")
    ax.set_xlim(0, len(years))
    spacing = range(0, len(years), 12*10)
    ax.set_xticks(spacing, [text[0:4] for text in [years[i] for i in spacing]])
    ax.set_ylabel("Density (kg/m$^3$)")
    ax.set_title(f"Historic and projected atmospheric density, {alt} km")
    ax.grid(which='major', color='0.7')
    ax.legend()
    plt.show()
    return


if __name__ == '__main__':
    main()
