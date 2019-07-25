import scipy.io as sio
import numpy as np
import os
from GetData.Behavioral_to_DF import get_dataframes
from GetData.Finalize_DF import finalize

"""Relevant Function below the init sequence"""

PATH_POSNER = r"C:\Users\jojou\OneDrive\Dokumente\Uni\BACHELORARBEIT\Analysis\Data_Posner"
PATH_POSNER_ONLINE = r"C:\Users\jojou\OneDrive\Dokumente\Uni\BACHELORARBEIT\Analysis\Data_Posner_Online"
PATH_DIRECTOR = r"C:\Users\jojou\OneDrive\Dokumente\Uni\BACHELORARBEIT\Analysis\Data_Director"
PATH_DIRECTOR_ONLINE = r"C:\Users\jojou\OneDrive\Dokumente\Uni\BACHELORARBEIT\Analysis\Data_Director_Online"
PATH_NF = r"C:\Users\jojou\OneDrive\Dokumente\Uni\BACHELORARBEIT\Analysis\NF"

down_reg = ["010", "017", "006", "007", "008", "011", "012", "018", "020", "028", "032", "035", "037", "038"]  # defines the probands in the downregulation-group
male = ["003", "004", "005", "010", "013", "016", "017", "020", "026", "027", "028", "032", "035", "036", "037"]  # defines the male participants.
exclude = ["009", "011"]


def get_behavioral():
    """Extracts the Data from the behavioral .mat files into a dictionary"""
    # create the lists in which the data shall append later. They are empty for now
    proband = []
    sex = []
    rt_valid_pre = []
    rt_valid_post = []
    rt_invalid_pre = []
    rt_invalid_post = []
    correct_valid_pre = []
    correct_valid_post = []
    correct_invalid_pre = []
    correct_invalid_post = []
    misses_pre_posner = []
    misses_post_posner = []
    regulation = []
    misses_pre_director = []
    misses_post_director = []
    rt_npt_pre = []
    rt_npt_post = []
    rt_pt_pre = []
    rt_pt_post = []
    rt_total_pre = []
    rt_total_post = []
    acc_npt_pre = []
    acc_npt_post = []
    acc_pt_pre = []
    acc_pt_post = []
    acc_total_pre = []
    acc_total_post = []
    perspective_pre = []
    no_perspective_pre = []
    pers_vs_nopers_pre = []
    perspective_post = []
    no_perspective_post = []
    pers_vs_nopers_post = []
    valid_pre = []
    invalid_pre = []
    inval_vs_val_pre = []
    valid_post = []
    invalid_post = []
    inval_vs_val_post = []
    Source_of_Threshold = []
    Threshold = []
    FinalThreshold = []

    os.chdir(PATH_POSNER)
    # loop through every file in the folder
    for file in os.listdir():
        data = sio.loadmat(file)  # load the file

        if file[-5] == "1":  # for pre-runs.
            proband.append(file[0:3])
            rt_valid_pre.append(data.get("rt_valid_trimmed")[0][0])
            rt_invalid_pre.append(data.get("rt_invalid_trimmed")[0][0])
            correct_valid_pre.append(data.get("correct_valid")[0][0])
            correct_invalid_pre.append(data.get("correct_invalid")[0][0])
            misses_pre_posner.append(data.get("misses")[0][0])

        elif file[-5] == "2":  # for post-runs
            rt_valid_post.append(data.get("rt_valid_trimmed")[0][0])
            rt_invalid_post.append(data.get("rt_invalid_trimmed")[0][0])
            correct_valid_post.append(data.get("correct_valid")[0][0])
            cip = data.get("correct_invalid")[0][0]
            if cip != 0:
                correct_invalid_post.append(cip)
            else:
                correct_invalid_post.append(0.00001)
            misses_post_posner.append(data.get("misses")[0][0])

            regulation.append(2) if file[:3] in down_reg else regulation.append(1)  # when the participant is in the down-reg group

            sex.append("m") if file[:3] in male else sex.append("w")  # when the participant is male

    # Perform some calculations
    reorienting_effect_pre = np.array(rt_invalid_pre) - np.array(rt_valid_pre)
    reorienting_effect_post = np.array(rt_invalid_post) - np.array(rt_valid_post)
    diff_reorienting = reorienting_effect_post - reorienting_effect_pre
    diff_acc_val = np.array(correct_valid_post) - np.array(correct_valid_pre)
    diff_acc_inv = np.array(correct_invalid_post) - np.array(correct_invalid_pre)
    Inv_eff_sc_valid_pre = np.array(rt_valid_pre) / np.array(correct_valid_pre)
    Inv_eff_sc_valid_post = np.array(rt_valid_post) / np.array(correct_valid_post)
    Inv_eff_sc_invalid_pre = np.array(rt_invalid_pre) / np.array(correct_invalid_pre)
    Inv_eff_sc_invalid_post = np.array(rt_invalid_post) / np.array(correct_invalid_post)
    Diff_inv_eff_sc_valid = Inv_eff_sc_valid_post - Inv_eff_sc_valid_pre
    Diff_inv_eff_sc_invalid = Inv_eff_sc_invalid_post - Inv_eff_sc_invalid_pre

    os.chdir(PATH_DIRECTOR)
    for file in os.listdir():
        data = sio.loadmat(file)  # load the file

        if file[-5] == "1":  # for pre-runs.
            rt_npt_pre.append(data.get("rt_npt_trimmed")[0][0])
            rt_pt_pre.append(data.get("rt_pt_trimmed")[0][0])
            rt_total_pre.append(data.get("rt_total")[0][0])
            acc_npt_pre.append(data.get("acc_npt")[0][0])
            acc_pt_pre.append(data.get("acc_pt")[0][0])
            acc_total_pre.append(data.get("acc_total")[0][0])

            # calculate the number of misses, based on number of NaNs in rt
            misses = 0
            for x in data.get("rt"):
                for num in x:
                    if np.isnan(num):
                        misses += 1
            misses_pre_director.append(misses)

        elif file[-5] == "2":  # for post-runs.
            rt_npt_post.append(data.get("rt_npt_trimmed")[0][0])
            rt_pt_post.append(data.get("rt_pt_trimmed")[0][0])
            rt_total_post.append(data.get("rt_total")[0][0])
            acc_npt_post.append(data.get("acc_npt")[0][0])
            acc_pt_post.append(data.get("acc_pt")[0][0])
            acc_total_post.append(data.get("acc_total")[0][0])

            # calculate the misses, based on number of NaNs in rt
            misses = 0
            for x in data.get("rt"):
                for num in x:
                    misses += 1 if np.isnan(num) else 0

            misses_post_director.append(misses)

    # Perform some calculations
    diff_rt_pt = np.array(rt_pt_post) - np.array(rt_pt_pre)
    diff_rt_npt = np.array(rt_npt_post) - np.array(rt_npt_pre)
    diff_rt_total = np.array(rt_total_post) - np.array(rt_total_pre)
    diff_acc_pt = np.array(acc_pt_post) - np.array(acc_pt_pre)
    diff_acc_npt = np.array(acc_npt_post) - np.array(acc_npt_pre)
    diff_acc_total = np.array(acc_total_post) - np.array(acc_total_pre)
    inv_eff_sc_npt_pre = np.array(rt_npt_pre) / np.array(acc_npt_pre)
    inv_eff_sc_npt_post = np.array(rt_npt_post) / np.array(acc_npt_post)
    inv_eff_sc_pt_pre = np.array(rt_pt_pre) / np.array(acc_pt_pre)
    inv_eff_sc_pt_post = np.array(rt_pt_post) / np.array(acc_pt_post)
    diff_inv_eff_sc_pt = inv_eff_sc_pt_post - inv_eff_sc_pt_pre
    diff_inv_eff_sc_npt = inv_eff_sc_npt_post - inv_eff_sc_npt_pre

    os.chdir(PATH_DIRECTOR_ONLINE)
    for file in os.listdir():
        data = sio.loadmat(file)

        if file[-5] == "1":
            perspective_pre.append(data.get("perspective")[0][0])
            no_perspective_pre.append(data.get("noperspective")[0][0])
            pers_vs_nopers_pre.append(data.get("perspective_vs_noperspective")[0][0])

        elif file[-5] == "2":
            perspective_post.append(data.get("perspective")[0][0])
            no_perspective_post.append(data.get("noperspective")[0][0])
            pers_vs_nopers_post.append(data.get("perspective_vs_noperspective")[0][0])

    os.chdir(PATH_POSNER_ONLINE)

    # Navigate to the Posner Online Path
    for file in os.listdir():
        data = sio.loadmat(file)

        if file[-5] == "1":
            valid_pre.append(data.get("valid")[0][0])
            invalid_pre.append(data.get("invalid")[0][0])
            inval_vs_val_pre.append(data.get("invalid_vs_valid")[0][0])

        elif file[-5] == "2":
            valid_post.append(data.get("valid")[0][0])
            invalid_post.append(data.get("invalid")[0][0])
            inval_vs_val_post.append(data.get("invalid_vs_valid")[0][0])

    os.chdir(PATH_NF)
    for file in os.listdir():
        data = sio.loadmat(file)  # open the file

        if file[10:12] == "12":  # only append the values for one subject
            Source_of_Threshold.append(data.get("Performance")[0][0][8][0])
            Threshold.append(data.get("Performance")[0][0][9][0][0])
            FinalThreshold.append(data.get("Performance")[0][0][10][0][0])

    # return a dictionary, containing the lists.
    output = {
        "Proband": proband,
        "Sex": sex,
        "Regulation": regulation,
        #"Threshold_Src": Source_of_Threshold,
        "Threshold": Threshold,
        "Final Threshold_Prop": FinalThreshold,

        "rt_valid_pre": rt_valid_pre,
        "rt_valid_post": rt_valid_post,
        "rt_invalid_pre": rt_invalid_pre,
        "rt_invalid_post": rt_invalid_post,
        "reorienting_effect_pre": reorienting_effect_pre,
        "reorienting_effect_post": reorienting_effect_post,
        "diff_reorienting": diff_reorienting,
        "correct_valid_pre": correct_valid_pre,
        "correct_valid_post": correct_valid_post,
        "correct_invalid_pre": correct_invalid_pre,
        "correct_invalid_post": correct_invalid_post,
        "diff_acc_val": diff_acc_val,
        "diff_acc_inv": diff_acc_inv,
        "misses_pre_posner": misses_pre_posner,
        "misses_post_posner": misses_post_posner,
        "Inv_eff_sc_valid_pre": Inv_eff_sc_valid_pre,
        "Inv_eff_sc_valid_post": Inv_eff_sc_valid_post,
        "Inv_eff_sc_invalid_pre": Inv_eff_sc_invalid_pre,
        "Inv_eff_sc_invalid_post": Inv_eff_sc_invalid_post,
        "Diff_inv_eff_sc_valid": Diff_inv_eff_sc_valid,
        "Diff_inv_eff_sc_invalid": Diff_inv_eff_sc_invalid,

        "rt_npt_pre": rt_npt_pre,
        "rt_npt_post": rt_npt_post,
        "diff_rt_npt": diff_rt_npt,
        "rt_pt_pre": rt_pt_pre,
        "rt_pt_post": rt_pt_post,
        "diff_rt_pt": diff_rt_pt,
        "rt_total_pre": rt_total_pre,
        "rt_total_post": rt_total_post,
        "diff_rt_total": diff_rt_total,
        "acc_npt_pre": acc_npt_pre,
        "acc_npt_post": acc_npt_post,
        "diff_acc_npt": diff_acc_npt,
        "acc_pt_pre": acc_pt_pre,
        "acc_pt_post": acc_pt_post,
        "diff_acc_pt": diff_acc_pt,
        "acc_total_pre": acc_total_pre,
        "acc_total_post": acc_total_post,
        "diff_acc_total": diff_acc_total,
        "misses_pre_director": misses_pre_director,
        "misses_post_director": misses_post_director,
        "Inv_eff_sc_npt_pre": inv_eff_sc_npt_pre,
        "Inv_eff_sc_npt_post": inv_eff_sc_npt_post,
        "Inv_eff_sc_pt_pre": inv_eff_sc_pt_pre,
        "Inv_eff_sc_pt_post": inv_eff_sc_pt_post,
        "Diff_Inv_eff_sc_npt": diff_inv_eff_sc_npt,
        "Diff_Inv_eff_sc_pt": diff_inv_eff_sc_pt,

        "pre_TPJ_pt": perspective_pre,
        "pre_TPJ_npt": no_perspective_pre,
        "pre_TPJ_pt_vs_npt": pers_vs_nopers_pre,
        "post_TPJ_pt": perspective_post,
        "post_TPJ_npt": no_perspective_post,
        "post_TPJ_pt_vs_npt": pers_vs_nopers_post,

        "pre_TPJ_valid": valid_pre,
        "pre_TPJ_invalid": invalid_pre,
        "pre_TPJ_invalid_vs_valid": inval_vs_val_pre,
        "post_TPJ_valid": valid_post,
        "post_TPJ_invalid": invalid_post,
        "post_TPJ_invalid_vs_valid": inval_vs_val_post,
    }

    df = get_dataframes(output)

    return finalize(df)


if __name__ == "__main__":
    g = get_behavioral()
