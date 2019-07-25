import scipy.io as sio
import os
import numpy as np
from GetData.Convert_NF import to_sess, to_run, to_trial

PATH_NF = r"C:\Users\jojou\OneDrive\Dokumente\Uni\BACHELORARBEIT\Analysis\NF"

down_reg = ["010", "017", "006", "007", "008", "011", "012", "018", "020", "028", "032", "035", "037", "038"]  # defines the probands in the downregulation-group
male = ["003", "004", "005", "010", "013", "016", "017", "020", "026", "027", "028", "032", "035", "036", "037"]  # defines the male participants.


def get_NF():
    """Extracts the Data from the Neurofeedback .mat files into a dictionary"""
    proband = []
    sex = []
    regulation = []

    temp_Reg_perf_mean = []
    temp_Reg_perf_md = []
    temp_Reg_perf_std = []
    temp_base_md = []
    temp_base_sd = []
    temp_time_above_thresh = []
    temp_time_above_init_thresh = []

    os.chdir(PATH_NF)

    for file in os.listdir():
        data = sio.loadmat(file)

        if file[10:12] == "01":  # do only once per subject
            proband.append(file[0:3])
            regulation.append(2) if file[:3] in down_reg else regulation.append(1)
            sex.append("m") if file[:3] in male else sex.append("w")

        for datapoint in data.get("Performance")[0][0][0][0]:
            temp_Reg_perf_mean.append(datapoint)

        for datapoint in data.get("Performance")[0][0][1][0]:
            temp_Reg_perf_md.append(datapoint)

        for datapoint in data.get("Performance")[0][0][2][0]:
            temp_Reg_perf_std.append(datapoint)

        for datapoint in data.get("Performance")[0][0][3][0]:
            temp_base_md.append(datapoint)

        for datapoint in data.get("Performance")[0][0][4][0]:
            temp_base_sd.append(datapoint)

        try:
            if file[:3] not in ["001", "002", "003", "004", "005", "006", "007", "008", "009", "010", "011"]:
                for datapoint in data.get("Performance")[0][0][11][0]:
                    temp_time_above_thresh.append(datapoint)
            else:
                for datapoint in np.full(6, np.nan):
                    temp_time_above_thresh.append(datapoint)

        except IndexError:
            for datapoint in np.full(6, np.nan):
                temp_time_above_thresh.append(datapoint)

        try:
            if file[:3] not in ["001", "002", "003", "004", "005", "006", "007", "008", "009", "010", "011"]:
                for datapoint in data.get("Performance")[0][0][12][0]:
                    temp_time_above_init_thresh.append(datapoint)
            else:
                for datapoint in np.full(6, np.nan):
                    temp_time_above_init_thresh.append(datapoint)

        except IndexError:
            for datapoint in np.full(6, np.nan):
                temp_time_above_init_thresh.append(datapoint)

    template_dict = {"Proband": proband, "Regulation": regulation}

    Reg_perf_mean_trial = to_trial(temp_Reg_perf_mean, proband, template_dict)
    Reg_perf_md_trial = to_trial(temp_Reg_perf_md, proband, template_dict)
    Reg_perf_std_trial = to_trial(temp_Reg_perf_std, proband, template_dict)
    base_md_trial = to_trial(temp_base_md, proband, template_dict)
    base_sd_trial = to_trial(temp_base_sd, proband, template_dict)
    time_thresh_trial = to_trial(temp_time_above_thresh, proband, template_dict)
    time_init_thresh_trial = to_trial(temp_time_above_init_thresh, proband, template_dict)

    Reg_perf_mean_run = to_run(temp_Reg_perf_mean, proband, template_dict)
    Reg_perf_md_run = to_run(temp_Reg_perf_md, proband, template_dict)
    Reg_perf_std_run = to_run(temp_Reg_perf_std, proband, template_dict)
    base_md_run = to_run(temp_base_md, proband, template_dict)
    base_sd_run = to_run(temp_base_sd, proband, template_dict)
    time_thresh_run = to_run(temp_time_above_thresh, proband, template_dict)
    time_init_thresh_run = to_run(temp_time_above_init_thresh, proband, template_dict)

    Reg_perf_mean_sess = to_sess(temp_Reg_perf_mean, proband, template_dict)
    Reg_perf_md_sess = to_sess(temp_Reg_perf_md, proband, template_dict)
    Reg_perf_std_sess = to_sess(temp_Reg_perf_std, proband, template_dict)
    base_md_sess = to_sess(temp_base_md, proband, template_dict)
    base_sd_sess = to_sess(temp_base_sd, proband, template_dict)
    time_thresh_sess = to_sess(temp_time_above_thresh, proband, template_dict)
    time_init_thresh_sess = to_sess(temp_time_above_init_thresh, proband, template_dict)

    return [time_thresh_trial, time_thresh_run, time_thresh_sess,
            time_init_thresh_trial, time_init_thresh_run, time_init_thresh_sess,
            Reg_perf_mean_trial, Reg_perf_mean_run, Reg_perf_mean_sess,
            Reg_perf_md_trial, Reg_perf_md_run, Reg_perf_md_sess,
            Reg_perf_std_trial, Reg_perf_std_run, Reg_perf_std_sess,
            base_md_trial, base_md_run, base_md_sess,
            base_sd_trial, base_sd_run, base_sd_sess,
            ]
