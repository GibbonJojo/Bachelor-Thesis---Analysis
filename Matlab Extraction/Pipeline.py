#!/usr/bin/env python
# coding: utf-8

# First import the necessary modules
from GetData import Behavioral, NF
from Workbook_Mod import fill_workbook, format_workbook, init_workbook

# Define the path to the output Excel sheet
PATH_EXCEL = r"C:\Users\jojou\OneDrive\Dokumente\Uni\BACHELORARBEIT\Analysis\Data_Complete.xlsx"


def main():
    # create the excel workbook
    workbook = init_workbook.init_workbook()

    # get the behavioral data
    behavioral_df = Behavioral.get_behavioral()

    # get the NF data
    nf_df = NF.get_NF()

    fill_workbook.fill_sheet(behavioral_df, workbook.worksheets[0])

    # fill the excel sheet
    for sheet, data in zip(workbook.worksheets[1:], nf_df):
        fill_workbook.fill_sheet(data, sheet)

    # format the sheet for better readability
    for sheet in workbook.worksheets:
        format_workbook.format_sheet(sheet)

    # save the workbook
    workbook.save(PATH_EXCEL)

### TODO: Currently not working: Threshold Source, Fit column width to text


if __name__ == "__main__":
    main()
