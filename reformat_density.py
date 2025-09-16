import pickle as pkl
import numpy as np
import json
import matplotlib.pyplot as plt


def main(ssp: int, path: str, plot: bool = False):
    '''Convert atmospheric density data for various SSPs into pySSEM format

    Arguments:
    ssp -- int [1,5], which major shared socioeconomic pathway to consider
    path -- filepath to save data to
    '''
    with open('data/dens_forecast_ssp_v3_msis2.pkl', 'rb') as file:
        data = pkl.load(file)

    # data assignments: [dens_ssp1_19_rs, dens_ssp1_26_rs, dens_ssp2_45_rs,
    #  dens_ssp3_70_rs, dens_ssp3_70_lowNTCF_rs, dens_ssp4_34_rs,
    #  dens_ssp4_60_rs, dens_ssp5_34_over_rs, dens_ssp5_85_rs, dens_rs,
    #  alt_rs, year_rs]

    # parse the desired SSP from Parker et al. data
    match ssp:
        case 0:     #
            sspdata = data[9]
        case 1:
            sspdata = data[1]
        case 2:
            sspdata = data[2]
        case 3:
            sspdata = data[3]
        case 4:
            sspdata = data[6]
        case 5:
            sspdata = data[8]
        case _:
            print("Invalid SSP. Choose 1-5.")
            exit()

    # turn altitudes into list of strings
    str_alts = data[10].astype(str)
    # turn decimal years into list of strings YYYY-MM
    str_years = np.empty(data[11].shape, dtype='<U10')
    for i, frac in enumerate(data[11]):
        year = np.floor(frac)
        mo = np.round((frac - year) * 12) + 1
        str_years[i] = f'{year:4.0f}-{mo:02.0f}'

    # create top-level dict, values empty
    tojson = dict.fromkeys(str_years)
    # create sub-dicts, filling in keys and values
    for i, str_year in enumerate(str_years):
        tojson[str_year] = dict(zip(str_alts, sspdata[i, :]))

    with open(path, 'w') as file:
        json.dump(tojson, file, indent=4)

    if plot:
        # plot atmospheric density data to confirm with Parker et al.
        alt = '600'         # plot data at 400km in altitude
        j = np.where(str_alts == alt)[0][0]
        plt.semilogy(range(0, len(str_years)),
                     data[9][:, j], linestyle=':', color='k', label='Baseline')
        plt.semilogy(range(0, len(str_years)),
                     data[1][:, j], color='teal', label='SSP1-2.6')
        plt.semilogy(range(0, len(str_years)),
                     data[2][:, j], color='goldenrod', label='SSP2-4.5')
        plt.semilogy(range(0, len(str_years)),
                     data[8][:, j], color='firebrick', label='SSP5-8.5')
        plt.xlabel("Date")
        plt.xlim(0, len(str_years))
        spacing = range(0, len(str_years), 12*10)
        plt.xticks(spacing, [text[0:4] for text in str_years[spacing]])
        plt.ylabel("Density (kg/m^3)")
        plt.title(f"Atmospheric density at {alt} km over time")
        plt.grid(which='major')
        plt.legend()
        plt.show()

    return


if __name__ == '__main__':
    main(0, 'pyssem/pyssem/utils/drag/dens_baseline_2000-2100.json')
