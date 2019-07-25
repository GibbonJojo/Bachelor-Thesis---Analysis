import pandas as pd


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

