"""
analysis.py: Functions to read and interpret figures from the batch simulation results.
"""
import json
import pickle
import pandas as pd
import numpy as np
import os
from os import makedirs
import re
from collections import OrderedDict
from itertools import product
import plotly.graph_objects as go
import plotly_express as px
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
df = dfss = filenamepkl = None


class NumpyEncode(json.JSONEncoder):
    """convert numpy data types for use in JSON format"""

    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return super(NumpyEncode, self).default(obj)


def readAllData(filename, dfonly=True):
    """read _allData.json routine to get params and data"""
    global params, data, df
    with open(filename, "r") as fileObj:
        dataLoad = json.load(fileObj, object_pairs_hook=OrderedDict)
    params, data, df = (
        dataLoad["params"],
        dataLoad["data"],
        toPandas(dataLoad["params"], dataLoad["data"]),
    )
    return df if dfonly else params, data, df


# readBatchData(dataFolder, batchLabel, target=None, saveAll=True, vars=None, maxCombs=None, listCombs=None)
def readBatchData(
    dataFolder,
    batchLabel,
    paramFile="params.csv",
    target=None,
    saveAll=True,
    vars=None,
    maxCombs=None,
    listCombs=None,
    EPSPsOnly=False,
):
    """gather data from dataFolder with batchLabel and save back to dataFolder or to target"""
    params, data = None, None
    # read the batch file and cfg
    batchFile = f"{dataFolder}/{batchLabel}_batch.json"
    with open(batchFile, "r") as fileObj:
        b = json.load(fileObj)["batch"]

    if b["method"] == "grid":
        if isinstance(listCombs, str):
            filename = str(listCombs)
            with open(filename, "r") as fileObj:
                dataLoad = json.load(fileObj)
            listCombs = dataLoad["paramsMatch"]

        # read params labels and ranges
        params = b["params"]

        # reorder so grouped params come first
        preorder = [p for p in params if "group" in p and p["group"]]
        for p in params:
            if p not in preorder:
                preorder.append(p)
        params = preorder

        # read vars from all files - store in dict
        labelList, valuesList = list(zip(*[(p["label"], p["values"]) for p in params]))
        valueCombinations = product(*(valuesList))
        indexCombinations = product(*[list(range(len(x))) for x in valuesList])
        data = {}
        print("Reading data...")
        missing = 0
        for i, (iComb, pComb) in enumerate(zip(indexCombinations, valueCombinations)):
            if (not maxCombs or i <= maxCombs) and (
                not listCombs or list(pComb) in listCombs
            ):
                print(i, iComb)
                # read output file
                iCombStr = "".join(["".join("_" + str(i)) for i in iComb])
                simLabel = b["batchLabel"] + iCombStr
                outFile = b["saveFolder"] + "/" + simLabel + "_data.json"
                try:
                    with open(outFile, "r") as fileObj:
                        output = json.load(fileObj, object_pairs_hook=OrderedDict)
                    # save output file in data dict
                    data[iCombStr] = {}
                    data[iCombStr]["paramValues"] = pComb  # store param values
                    if not vars:
                        vars = list(output.keys())

                    for key in vars:
                        if isinstance(key, tuple):
                            container = output
                            for ikey in range(len(key) - 1):
                                container = container[key[ikey]]
                            data[iCombStr][key[1]] = container[key[-1]]

                        elif isinstance(key, str):
                            data[iCombStr][key] = output[key]

                except:
                    print("... file missing")
                    missing = missing + 1
                    output = {}
            else:
                missing = missing + 1

        print("%d files missing" % (missing))
    elif b["method"] == "list":
        fileList = [
            x.name for x in os.scandir(dataFolder) if x.name.endswith("_data.json")
        ]
        fileList.sort(key=lambda x: int(re.split(f"{batchLabel}|[_.]", x)[1]))
        dfParam = pd.read_csv(paramFile, delimiter=",")
        data = {}
        if len(dfParam) != len(fileList):
            raise Exception(
                f"The number of files in {dataFolder} and the no. of parameters in {paramFile} do not match. {paramFile} cannot be read"
            )
        labelList = list(dfParam.columns)
        params = []
        for lab in labelList:
            params.append({"label": lab, "values": list(dfParam[lab])})
        for (iloc, datafile), paralist in zip(enumerate(fileList), dfParam.values):
            outFile = f"{dataFolder}/{datafile}"
            indexComb = int(re.split(f"{batchLabel}|[_.]", datafile)[1])
            data[indexComb] = {}
            paraComb = tuple(paralist)
            data[indexComb]["paramValues"] = paraComb
            with open(outFile, "r") as fileObj:
                output = json.load(fileObj, object_pairs_hook=OrderedDict)
                if all(
                    [
                        output["simConfig"][x] != y
                        for x, y in zip(labelList, dfParam.loc[iloc])
                    ]
                ):
                    raise Exception(
                        f"Parameter values in {paramFile} and in the json files do not match"
                    )
                if EPSPsOnly:
                    EPSPdata = processEPSPs(output)

            if not vars:
                vars = list(output.keys())
            if EPSPsOnly:
                for key in vars:
                    if key == "simData":
                        continue
                    data[indexComb][key] = output[key]
                for key in EPSPdata:
                    data[indexComb][key] = EPSPdata[key]
            else:
                for key in vars:
                    data[indexComb][key] = output[key]

    # pass

    else:
        raise Exception(
            f"Method {b['method'] if b['method'] else 'No method'} files cannot be read."
        )
    # save
    if saveAll:
        print("Saving to single file with all data")
        filename = f"{batchLabel}_allData.json"
        dataSave = {"params": params, "data": data}
        with open(filename, "w") as fileObj:
            json.dump(dataSave, fileObj, cls=NumpyEncode)
    else:
        return params, data


# toPandas(params, data) convert data to Pandas
def toPandas(params, data):
    if "simData" in data[list(data.keys())[0]]:
        rows = [
            list(d["paramValues"]) + [s for s in list(d["simData"].values())]
            for d in list(data.values())
        ]
        cols = [str(d["label"]) for d in params] + [
            s for s in list(data[list(data.keys())[0]]["simData"].keys())
        ]
    else:
        rows = [
            list(d["paramValues"]) + [s for s in list(d.values())]
            for d in list(data.values())
        ]
        cols = [str(d["label"]) for d in params] + [
            s for s in list(data[list(data.keys())[0]].keys())
        ]

    df = pd.DataFrame(rows, columns=cols)
    df["simLabel"] = list(data.keys())

    colRename = []
    for col in list(df.columns):
        if col.startswith("[u'"):
            colName = (
                col.replace(", u'", "_'")
                .replace("[u", "")
                .replace("'", "")
                .replace("]", "")
                .replace(", ", "_")
            )
            colRename.append(colName)
        else:
            colRename.append(col)
    df.columns = colRename

    return df


# spikeStats(), save, load
""" example usage:
df1 = spikeStats() # assuming df has been read
plt.scatter(df1.hz, df1.avgRate) # a scatter plot
df1.scnt.describe() # stats on the stats eg: count 460.000000 mean 1.886957 std 4.674625 min 0.000000 25% 1.000000 50% 1.000000 75% 1.000000 max 27.000000
"""


def spikeStats(df=df):
    # syntax example: dfss.spk1, dfss.f1
    dfss = df[["amp", "cellnum", "avgRate"]].copy()  # note double brackets
    dfss.scnt = df.spkt.apply(
        len
    )  # number of spikes (spikecount) * IGNORE WARNING, creates dfss.scnt anyway
    dfss["scnt"] = df.spkt.apply(len)
    dfss["spk1"] = df.spkt.apply(
        lambda x: x[0] if len(x) > 0 else -1
    )  # spk1; time of first spike
    dfss["f1"] = df.spkt.apply(
        lambda x: 1e3 / (x[1] - x[0]) if len(x) > 1 else 0
    )  # f1: freq for 1st ISI
    dfss["f2"] = df.spkt.apply(
        lambda x: 1e3 / (x[2] - x[1]) if len(x) > 2 else 0
    )  # f2: freq for 2nd ISI
    dfss["sdur"] = df.spkt.apply(
        lambda x: x[-1] - x[0] if len(x) > 1 else 0
    )  # sdur: duration of spiking
    dfss["hz"] = dfss.scnt.div(dfss.sdur).mul(1e3).replace(np.inf, 0)  # >>> NaN
    # dfss['fend'] = df.spkt.apply(lambda x: 1e3/(x[len(x)] - x[len(x)-1]) if len(x)>3 else 0) # fend: freq for last ISI
    # dfss['fend0'] = df.spkt.apply(lambda x: 1e3/(x[len(x-1)] - x[len(x)-2]) if len(x)>4 else 0) # fend-1: freq for 2nd tp last ISI
    # dfss['sfa'] = (statistics.mean(f_last))/(statistics.mean(f_first)) #spike freq adaptation ration = (mean(fend, fend-1))/((mean (f1, f2)) Suter et al.
    return dfss


def svSpikeStats(dataFolder, batchLabel, dfss=dfss):
    filenamejson = "%s/%s_spkStats.json" % (dataFolder, batchLabel)
    filenamepkl = "%s/%s_spkStats.pkl" % (dataFolder, batchLabel)
    dfss.to_pickle(filenamepkl)
    dfss.to_json(filenamejson)


def ldSpikeStats(f=filenamepkl):
    return pd.read_pickle(f)


def allAnalysis(df=df):
    # Spiking Data
    dfss = df[["cellnum", "avgRate"]].copy()  # note double brackets
    dfss.scnt = df.spkt.apply(
        len
    )  # number of spikes (spikecount) * IGNORE WARNING, creates dfss.scnt anyway
    dfss["scnt"] = df.spkt.apply(len)
    dfss["spk1"] = df.spkt.apply(
        lambda x: x[0] if len(x) > 0 else -1
    )  # spk1; time of first spike
    dfss["f1"] = df.spkt.apply(
        lambda x: 1e3 / (x[1] - x[0]) if len(x) > 1 else 0
    )  # f1: freq for 1st ISI
    dfss["f2"] = df.spkt.apply(
        lambda x: 1e3 / (x[2] - x[1]) if len(x) > 2 else 0
    )  # f2: freq for 2nd ISI
    dfss["sdur"] = df.spkt.apply(
        lambda x: x[-1] - x[0] if len(x) > 1 else 0
    )  # sdur: duration of spiking
    dfss["hz"] = (
        dfss.scnt.div(dfss.sdur).mul(1e3).fillna(0).replace(np.inf, 0)
    )  # >>> NaN

    stim = data[list(data)[0]]["net"]["params"]["stimSourceParams"]["iclamp"]
    stimend = stim["dur"] + stim["delay"]
    dclass = df[["cellnum"]].copy()
    dclass["Vlist"] = df.V_soma.apply(lambda x: x["cell_0"])
    dclass["Vrmp"] = dclass.Vlist.apply(lambda x: x[0])
    dclass["spkend"] = df.spkt.apply(lambda x: x[len(x) - 1] if len(x) > 0 else -1)

    dclass["Vsubth"] = dclass.Vlist.apply(lambda x: 2 ** 0 if max(x) < 0 else np.nan)
    dclass["Vph"] = dfss.scnt.apply(lambda x: 2 ** 1 if 0 < x <= 3 else np.nan)
    dclass["Vton"] = df.spkt.apply(
        lambda x: 2 ** 2
        if len(x) > 3 and stim["delay"] <= x[-1] <= stimend + 5
        else np.nan
    )
    dclass["Vton_susps"] = dclass.spkend.apply(
        lambda x: 2 ** 3
        if stimend + 5 <= x >= data[list(data)[0]]["simConfig"]["duration"] - 50
        else np.nan
    )
    dclass["Vton_brfps"] = dclass.spkend.apply(
        lambda x: 2 ** 4
        if stimend + 5 <= x <= data[list(data)[0]]["simConfig"]["duration"] - 50
        else np.nan
    )

    # Plotting

    f = go.Figure()
    f.add_trace(
        go.Scatter(
            x=dclass["cellnum"],
            y=dclass["Vsubth"],
            mode="markers",
            marker=dict(
                color="beige", size=20, line=dict(color="MediumPurple", width=2)
            ),
            text=dclass.cellnum,
            name="Subthreshold",
            showlegend=True,
        )
    )
    f.add_trace(
        go.Scatter(
            x=dclass["cellnum"],
            y=dclass["Vph"],
            mode="markers",
            marker=dict(
                color="LightPink", size=20, line=dict(color="MediumPurple", width=2)
            ),
            text=dclass.cellnum,
            name="Phasic",
            showlegend=True,
        )
    )
    f.add_trace(
        go.Scatter(
            x=dclass["cellnum"],
            y=dclass["Vton"],
            mode="markers",
            marker=dict(
                color="LightSkyBlue", size=20, line=dict(color="MediumPurple", width=2)
            ),
            text=dclass.cellnum,
            name="Tonic",
            showlegend=True,
        )
    )
    f.add_trace(
        go.Scatter(
            x=dclass["cellnum"],
            y=dclass["Vton_susps"],
            mode="markers",
            marker=dict(
                color="LightSteelBlue",
                size=20,
                line=dict(color="MediumPurple", width=2),
            ),
            text=dclass.cellnum,
            name="Tonic with Sustained Post-stim",
            showlegend=True,
        )
    )
    f.add_trace(
        go.Scatter(
            x=dclass["cellnum"],
            y=dclass["Vton_brfps"],
            mode="markers",
            marker=dict(
                color="LightSeagreen", size=20, line=dict(color="MediumPurple", width=2)
            ),
            text=dclass.cellnum,
            name="Tonic with Brief Post-stim",
            showlegend=True,
        )
    )
    f.update_layout(title="Classification of Responses", legend_orientation="h")
    f.update_xaxes(title="Cell Number")
    f.write_image("classification.png")
    return


def processEPSPs(data, do_fit=True):
    """extract EPSP times and amplitude from synaptic stimulus"""
    sd = data["simData"]
    sd["t"] = np.array(sd["t"])
    delay = data["simConfig"]["delay"]
    tau1 = data["simConfig"]["tau1"]
    dt = data["simConfig"]["recordStep"]
    times = [
        int(np.argmin(abs(sd["t"] - (i + delay)))) for i in sd["stims"]["cell_0"]["bkg"]
    ]
    amps = [
        -sd["V_soma"]["cell_0"][i]
        + max(sd["V_soma"]["cell_0"][i + int(tau1 / dt) : i + int(3 * tau1 / dt)])
        for i in times
    ]
    if "isyn" in sd:
        stims = [
            max(
                sd["isyn"]["cell_0"]["soma_0.5"][
                    i + int(tau1 / dt) : i + int(3 * tau1 / dt)
                ]
            )
            for i in times
        ]
    else:
        stims = None
    process_data = {"times": times, "epsps": amps, "stims": stims}
    if do_fit:
        amps = np.array(amps[1:])
        t = np.diff(times)*dt*1e-3  # fit for time in sec
        ftA, _ = curve_fit(lambda x,a,b: a*x**b,t,amps,p0=[1,1])
        famps = amps[amps<80]
        tt = t[amps<80]
        ftB, _ = curve_fit(lambda x,a,b: a*x**b,tt,famps,p0=[1,1])
        process_data['full_fit'] = ftA
        process_data['filter_fit'] =  ftB
    return process_data


def plotEpas(df=df):
    stim = data[list(data)[0]]["net"]["params"]["stimSourceParams"]["iclamp"]
    if stim["amp"] and stim["dur"] and stim["delay"] == 0:
        raise Exception(
            "Epas cannot be computed in the presence of an ongoing stimulus"
        )
    elif (
        stim["amp"]
        and stim["dur"]
        and stim["delay"] <= data[list(data)[0]]["simConfig"]["duration"]
    ):
        for i in df["t"][0]:
            if i < stim["delay"]:
                indx = df["t"][0].index(i)
    else:
        indx = -1
    # import IPython; IPython.embed()
    print(indx)
    cells = df["cellnum"].tolist()
    vm = {}
    pasv = {}
    for c in cells:
        vm[c] = df["V_soma"][c]["cell_0"][indx]
        pasv[c] = df["epas"][c]["cell_0"][indx]

    fig, axs = plt.subplots(2, 1)
    axs[0].scatter(list(pasv), list(pasv.values()), c="red")
    axs[0].set_title("epas (mV)")
    axs[1].scatter(list(vm), list(vm.values()))
    axs[1].set_title("membrane voltage (mV)")
    plt.xlabel("Cell Numbers")
    plt.savefig(batchLabel + "_epas.png")
    return


def plotRin(df=df):
    ripk = {}

    stim = data[list(data)[0]]["net"]["params"]["stimSourceParams"]["iclamp"]
    cells = df["cellnum"].tolist()
    for i in df["t"][0]:  # dt is same so time array is same for all cells
        if i < (stim["delay"]):
            init = df["t"][0].index(i)
        if i < (stim["delay"] + stim["dur"]):
            end = df["t"][0].index(i)
    d = df[["cellnum", "V_soma"]].copy()
    d["ripk"] = d.V_soma.apply(
        lambda x: (min(x["cell_0"][init:end]) - x["cell_0"][init]) / stim["amp"]
    )
    fr = px.scatter(
        d,
        x="cellnum",
        y="ripk",
        hover_data=["cellnum", "ripk", df.index],
        labels={"cellnum": "Cell Number", "ripk": "Rin (MOhm)"},
        title="Calculated from Negative Peak",
        template="simple_white",
    )
    fr.show()
    return


def plotVm(df, batchLabel):
    makedirs(f"{batchLabel}/vmPlots")
    for indx in df.index:
        f = plt.figure()
        plt.plot(df["t"][indx], df["V_soma"][indx]["cell_0"], c="C0")
        plt.xlabel("Time (ms)")
        plt.ylabel("Membrane Voltage (mV)")
        plt.title(f"Cell Number: {df['cellnum'][indx]}")
        plt.savefig(f"{batchLabel}/vmPlots/{df['simLabel'][indx]}.png")
        plt.close()
    return
