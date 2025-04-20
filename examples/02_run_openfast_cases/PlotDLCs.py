import os
import matplotlib.pyplot as plt
from openfast_io.FAST_output_reader import FASTOutputFile

THISDIR = os.path.dirname(os.path.abspath(__file__))
DLC = "1.5"


def main():
    outpath = os.path.join(THISDIR, "outputs", f"DLC{DLC.replace('.','')}", "openfast_runs")
    outpathfiles = os.listdir(outpath)
    outfiles = [file for file in outpathfiles if ((os.path.splitext(file)[1] == ".outb") & file.startswith(f"DLC{DLC}_0_weis_job_"))]
    outfiles.sort()
    print(f'Found {len(outfiles)} outfiles for DLC {DLC}')
    plotdf(outpath,outfiles)


def plotdf(outpath,outfiles):
    xvar = "Time_[s]"
    vars = [
        "Wind1VelX_[m/s]",
        "Wind1VelY_[m/s]",
        "Wave1Elev_[m]",
        "BldPitch1_[deg]",
        "GenTq_[kN-m]",
        "GenSpeed_[rpm]",
        "TwrBsMyt_[kN-m]",
    ]
    nvars = len(vars)
    f, ax = plt.subplots(nvars, 1, figsize=(10, 2 * nvars), sharex=True)
    ax = [ax] if nvars == 1 else ax

    for outfile in outfiles:
        outfile = os.path.join(outpath, outfile)
        df = FASTOutputFile(outfile).toDataFrame()

        for i in range(nvars):
            var = vars[i]
            label = os.path.splitext(os.path.basename(outfile))[0]
            ax[i].plot(df[xvar], df[var],label=label)
            ax[i].set_ylabel(f"{var.split('_')[0]}\n{var.split('_')[1]}")
            ax[i].grid(True)
    ax[-1].set_xlabel(f"{xvar.split('_')[0]} {xvar.split('_')[1]}")
    ax[-1].legend(loc='lower center', bbox_to_anchor=(0.5, -0.5), ncol=3)
    ax[0].set_title(f"DLC {DLC} Demo")
    f.tight_layout()
    f.savefig(os.path.join(THISDIR, f"DLC{DLC.replace('.','')}.png"))


if __name__ == "__main__":
    main()
