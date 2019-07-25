import pandas as pd
import numpy as np
from GetData.Finalize_DF import finalize


def to_trial(data, sub, template):
    output = []

    for n in range(72):
        ind = [n + (72 * i) for i in range(len(sub))]
        output.append([data[i] for i in ind])

    output_dict = {str(x): y for x, y in enumerate(output, 1)}

    output_df = finalize(pd.DataFrame({**template, **output_dict}))

    return output_df


def to_run(data, sub, template):
    output = []

    for n in range(12):
        ind = [(n * 6) + (72 * i) for i in range(len(sub))]
        output.append([np.mean(data[i:i + 6]) for i in ind])

    output_dict = {str(x): y for x, y in enumerate(output, 1)}

    output_df = finalize(pd.DataFrame({**template, **output_dict}))

    return output_df


def to_sess(data, sub, template):
    output = []

    for n in range(6):
        ind = [(n * 12) + (72 * i) for i in range(len(sub))]
        output.append([np.mean(data[i:i + 12]) for i in ind])

    output2 = [output[0], [(x+y)*0.5 for x, y in zip(output[1], output[2])],
               [(x+y)*0.5 for x, y in zip(output[3], output[4])], output[5]]

    output_dict = {str(x): y for x, y in enumerate(output2, 1)}

    output_df = finalize(pd.DataFrame({**template, **output_dict}))

    return output_df
