import pandas as pd
from Archive.Get_Data_Pandas2 import get_data


def get_all_data():
    posner_data = get_data("posner")  # extract the data from posner test
    director_data = get_data("director")  # extract the data from director test
    posner_data_online = get_data("posner_online")  # extract the online posner data
    director_data_online = get_data("director_online")  # extract the online director data

    for key in posner_data:
        print(len(posner_data.get(key)))

    df_posner = pd.DataFrame(posner_data)
    df_director = pd.DataFrame(director_data)
    df_posner_online = pd.DataFrame(posner_data_online)
    df_director_online = pd.DataFrame(director_data_online)


    print(df_posner)


if __name__ == "__main__":
    get_all_data()
