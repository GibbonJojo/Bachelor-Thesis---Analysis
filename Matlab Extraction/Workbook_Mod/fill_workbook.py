from openpyxl.utils.dataframe import dataframe_to_rows


def fill_sheet(df, sheet):
    """Fill the excel sheet with the data"""
    for row in dataframe_to_rows(df, index=True, header=True):
        sheet.append(row)
