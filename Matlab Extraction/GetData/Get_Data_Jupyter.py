import scipy.io as sio
import numpy as np
import os
import pandas as pd

"""
The Script requires all data to be in seperate folders with only the data in it!
First Specify in which Folders you got the data. For that, replace the following
paths with the one to your own data folders.
Please mind, that there has to be a "r" in front of the quotes!
"""

PATH_POSNER = r"C:\Users\jojou\OneDrive\Dokumente\Uni\BACHELORARBEIT\Analysis\Data_Posner"
PATH_POSNER_ONLINE = r"C:\Users\jojou\OneDrive\Dokumente\Uni\BACHELORARBEIT\Analysis\Data_Posner_Online"
PATH_DIRECTOR = r"C:\Users\jojou\OneDrive\Dokumente\Uni\BACHELORARBEIT\Analysis\Data_Director"
PATH_DIRECTOR_ONLINE = r"C:\Users\jojou\OneDrive\Dokumente\Uni\BACHELORARBEIT\Analysis\Data_Director_Online"
PATH_NF = r"C:\Users\jojou\OneDrive\Dokumente\Uni\BACHELORARBEIT\Analysis\NF"

down_reg = ["010", "017", "006", "007", "008", "011", "012", "018", "020", "028"]  # defines the probands in the downregulation-group
male = ["003", "004", "005", "010", "013", "016", "017", "020", "026", "027", "028"]  # defines the male participants.


"""
This Part of the Script extracts the Data from the files and creates a
dictionary for all desired data.
"Type" specifies whether the data from posner, posner_online, director or
director_online should be extracted.

I will only thoroughly document the first part
(type == "posner", until type =="director"),
since everything below will follow the same principle and I'm lazy.

# will mark comments, explaining, how the code roughly works.
Triple Quotes will specify what has to be changed where, if you want to get
different data or seomething
"""


def get_dataframes(data):
    df = pd.DataFrame(data)
    return df


def finalize(df):
    df = df.set_index("Proband")  # Set the Proband number as Index of the dataframe

    reg = df.groupby("Regulation")  # Create a new dataframe, where the data is grouped by regulation

    meanstd = pd.concat([reg.mean(), reg.std()])  # Create a new dataframe with mean and std of both regulations
    meanstd.set_index(pd.Index(["Mean_Up", "Mean_Down", "Std_Up", "Std_Down"]), inplace=True)
    meanstd.sort_index(inplace=True)

    empty = pd.DataFrame([[""] * df.shape[1]], columns=df.columns,
                         index=[""])  # Create an empty dataframe for later formatting

    final_df = pd.concat([df, empty, df.describe().iloc[1:], empty, meanstd],
                         sort=False)  # create the final dataframe, that will be written into excel

    return final_df


def get_data(type):
    # First specify if the data is extracted from posner or director datafiles
    if type == "posner":
        # navigate to the folder containing the datafiles
        os.chdir(PATH_POSNER)

        # create the lists in which the data shall append later. They are empty for now
        """If you want to get additional data, specify another extra empty list
        and follow further instructions below"""
        proband = []
        rt_valid_pre = []
        rt_valid_post = []
        rt_invalid_pre = []
        rt_invalid_post = []
        correct_valid_pre = []
        correct_valid_post = []
        correct_invalid_pre = []
        correct_invalid_post = []
        misses_pre = []
        misses_post = []
        regulation = []
        gender = []

        # loop through every file in the folder
        for file in os.listdir():
            data = sio.loadmat(file)  # load the file

            """Now specify the data that shall be appended to the list
            for that, use the following syntax in both if-loops:
                list.append(data.get("DATANAME_IN_MATLAB_FILE")[0][0])"""
            if file[-5] == "1":  # for pre-runs.
                proband.append(file[0:3])
                rt_valid_pre.append(data.get("rt_valid")[0][0])
                rt_invalid_pre.append(data.get("rt_invalid")[0][0])
                correct_valid_pre.append(data.get("correct_valid")[0][0])
                correct_invalid_pre.append(data.get("correct_invalid")[0][0])
                misses_pre.append(data.get("misses")[0][0])

            elif file[-5] == "2":  # for post-runs
                rt_valid_post.append(data.get("rt_valid")[0][0])
                rt_invalid_post.append(data.get("rt_invalid")[0][0])
                correct_valid_post.append(data.get("correct_valid")[0][0])
                correct_invalid_post.append(data.get("correct_invalid")[0][0])
                misses_post.append(data.get("misses")[0][0])

                if file[:3] in down_reg:
                    regulation.append(0)
                else:
                    regulation.append(1)

                if file[:3] in male:
                    gender.append("m")
                else:
                    gender.append("w")


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

        # return a dictionary with the keys being the datanames and values being
        # the datalists
        """Lastly put the datapoint into this dictionary at the desired position.
        The stuff in quotes specifies the name, that will appear in the first
        row of the excel sheet. This is followed by a colon and the name of the
        datalist and a comma.
        """
        output = {"Sex": gender,
                  "Regulation": regulation,
                  "Proband": proband,
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
                  "misses_pre": misses_pre,
                  "misses_post": misses_post,
                  "Inv_eff_sc_valid_pre": Inv_eff_sc_valid_pre,
                  "Inv_eff_sc_valid_post": Inv_eff_sc_valid_post,
                  "Inv_eff_sc_invalid_pre": Inv_eff_sc_invalid_pre,
                  "Inv_eff_sc_invalid_post": Inv_eff_sc_invalid_post,
                  "Diff_inv_eff_sc_valid": Diff_inv_eff_sc_valid,
                  "Diff_inv_eff_sc_invalid": Diff_inv_eff_sc_invalid,
                  }

        df = get_dataframes(output)

        return finalize(df)

    elif type == "director":
        # navigate to the folder containing the data files
        os.chdir(PATH_DIRECTOR)

        # create the lists in which the data shall append later
        proband = []
        misses_pre = []
        misses_post = []
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
        regulation = []
        gender = []

        for file in os.listdir():
            data = sio.loadmat(file)  # load the file

            if file[-5] == "1":  # for pre-runs.
                proband.append(file[0:3])
                rt_npt_pre.append(data.get("rt_npt")[0][0])
                rt_pt_pre.append(data.get("rt_pt")[0][0])
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
                misses_pre.append(misses)


            elif file[-5] == "2": # for post-runs.
                rt_npt_post.append(data.get("rt_npt")[0][0])
                rt_pt_post.append(data.get("rt_pt")[0][0])
                rt_total_post.append(data.get("rt_total")[0][0])
                acc_npt_post.append(data.get("acc_npt")[0][0])
                acc_pt_post.append(data.get("acc_pt")[0][0])
                acc_total_post.append(data.get("acc_total")[0][0])

                #calculate the misses, based on number of NaNs in rt
                misses = 0
                for x in data.get("rt"):
                    for num in x:
                        if np.isnan(num):
                            misses += 1
                misses_post.append(misses)

                if file[:3] in down_reg:
                    regulation.append(0)
                else:
                    regulation.append(1)

                if file[:3] in male:
                    gender.append("m")
                else:
                    gender.append("w")

        # Perform some calculations
        diff_rt_pt = np.array(rt_pt_post) - np.array(rt_pt_pre)
        diff_rt_npt = np.array(rt_npt_post) - np.array(rt_npt_pre)
        diff_rt_total = np.array(rt_total_post) - np.array(rt_total_pre)
        diff_acc_pt = np.array(acc_pt_post) - np.array(acc_pt_pre)
        diff_acc_npt = np.array(acc_npt_post) - np.array(acc_npt_pre)
        diff_acc_total = np.array(acc_total_post) - np.array(acc_total_pre)

        # same procedure - lists in list
        output = {"Sex": gender,
                    "Regulation": regulation,
                    "Proband": proband,
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
                    "misses_pre": misses_pre,
                    "misses_post": misses_post,
                     }

        df = get_dataframes(output)

        return finalize(df)

    elif type == "director_online":
        os.chdir(PATH_DIRECTOR_ONLINE)

        proband = []
        perspective_pre = []
        no_perspective_pre = []
        pers_vs_nopers_pre = []
        perspective_post = []
        no_perspective_post = []
        pers_vs_nopers_post = []
        regulation = []
        gender = []

        for file in os.listdir():
            data = sio.loadmat(file)

            if file[-5] == "1":
                proband.append(file[0:3])
                perspective_pre.append(data.get("perspective")[0][0])
                no_perspective_pre.append(data.get("noperspective")[0][0])
                pers_vs_nopers_pre.append(data.get("perspective_vs_noperspective")[0][0])

            elif file[-5] == "2":
                perspective_post.append(data.get("perspective")[0][0])
                no_perspective_post.append(data.get("noperspective")[0][0])
                pers_vs_nopers_post.append(data.get("perspective_vs_noperspective")[0][0])

                if file[:3] in down_reg:
                    regulation.append(0)
                else:
                    regulation.append(1)

                if file[:3] in male:
                    gender.append("m")
                else:
                    gender.append("w")

        output = {"Gender": gender,
                "Regulation": regulation,
                "Proband": proband,
                "perspective_pre": perspective_pre,
                "perspective_post": perspective_post,
                "no_perspective_pre": no_perspective_pre,
                "no_perspective_post": no_perspective_post,
                "perspective_vs_noperspective_pre": pers_vs_nopers_pre,
                "perspective_vs_noperspective_post": pers_vs_nopers_post,
                }

        df = get_dataframes(output)

        return finalize(df)



    elif type == "posner_online":
        os.chdir(PATH_POSNER_ONLINE)

        proband = []
        valid_pre = []
        invalid_pre = []
        inval_vs_val_pre = []
        valid_post = []
        invalid_post = []
        inval_vs_val_post = []
        regulation = []
        gender = []

        for file in os.listdir():
            data = sio.loadmat(file)

            if file[-5] == "1":
                proband.append(file[0:3])
                valid_pre.append(data.get("valid")[0][0])
                invalid_pre.append(data.get("invalid")[0][0])
                inval_vs_val_pre.append(data.get("invalid_vs_valid")[0][0])

            elif file[-5] == "2":
                valid_post.append(data.get("valid")[0][0])
                invalid_post.append(data.get("invalid")[0][0])
                inval_vs_val_post.append(data.get("invalid_vs_valid")[0][0])

                if file[:3] in down_reg:
                    regulation.append(0)
                else:
                    regulation.append(1)

                if file[:3] in male:
                    gender.append("m")
                else:
                    gender.append("w")

        output = {"Sex": gender,
                "Regulation": regulation,
                "Proband": proband,
                "valid_pre": valid_pre,
                "valid_post": valid_post,
                "invalid_pre": invalid_pre,
                "invalid_post": invalid_post,
                "invalid_vs_valid_pre": inval_vs_val_pre,
                "invalid_vs_valid_post": inval_vs_val_post,
                }

        df = get_dataframes(output)

        return finalize(df)
