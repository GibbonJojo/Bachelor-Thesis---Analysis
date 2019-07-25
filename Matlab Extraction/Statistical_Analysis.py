import scipy.stats as stats

def kruskal(*args):
    stat, p = stats.kruskal(*args)

    return p


def analysis_init(pos, direc, type="None"):

    if type == "posner":
        rt_valid = kruskal(pos[0], pos[1])
        rt_invalid = kruskal(pos[2], pos[3])
        correct_valid = kruskal(pos[4], pos[5])
        correct_invalid = kruskal(pos[6], pos[7])
        pos_misses = kruskal(pos[8], pos[9])

        return ["", rt_valid, "", rt_invalid, "", correct_valid, "", correct_invalid, "", pos_misses]

    elif type == "director":
        rt_npt = kruskal(direc[0], direc[1])
        rt_pt = kruskal(direc[2], direc[3])
        rt_total = kruskal(direc[4], direc[5])
        acc_npt = kruskal(direc[6], direc[7])
        acc_pt = kruskal(direc[8], direc[9])
        acc_total = kruskal(direc[10], direc[11])
        dir_misses = kruskal(direc[12], direc[13])

        return ["", rt_npt, "", rt_pt, "", rt_total, "", acc_npt, "", acc_pt, "", acc_total, "", dir_misses]

    else:
        raise NameError("Function needs posner or director as type")

if __name__ == "__main__":
    analysis_init()
    print(analysis_init("posner"))
    print(analysis_init("director"))
