"""Script used to test conditional formating capabilities of the pandas library.
"""

# Python import
import pandas as pd

# Only run if run as main script
if __name__ == "__main__":

    # Create some Pandas dataframes from some data.
    start_row = 2  # Row on which we start displaying the data analysis
    start_column = 0  # Column on which we start displaying the data analysis
    df1 = pd.DataFrame([1, 3, 1, 0, 4, 2])
    df2 = pd.DataFrame([1, 3, 1, 0, 4, 2])
    df3 = pd.DataFrame(["a", "d", "b", "b", "a", "a"])
    df4 = pd.DataFrame(["d", "a", "b", "a", "d", "a"])

    # Create a Pandas Excel writer using XlsxWriter as the engine.
    writer = pd.ExcelWriter("pandas_xlsxwriter.xlsx", engine="xlsxwriter")

    # Write each dataframe to a different worksheet.
    df1.to_excel(
        writer, sheet_name="Sheet1", header=False, index=False, startrow=start_row
    )
    df2.to_excel(
        writer, sheet_name="Sheet3", header=False, index=False, startrow=start_row
    )
    df3.to_excel(writer, sheet_name="Sheet2", header=False, index=False)
    df4.to_excel(writer, sheet_name="Sheet2", header=False, index=False, startcol=1)

    # Get the xlsxwriter workbook and worksheet objects.
    workbook = writer.book
    worksheet_1 = writer.sheets["Sheet1"]
    worksheet_2 = writer.sheets["Sheet2"]
    worksheet_2.hide()
    worksheet_3 = writer.sheets["Sheet3"]

    # Create a format for the conditional format.
    end_row = df1.shape[0] - 1 + start_row
    end_col = df2.shape[1] - 1 + start_column
    condition_format = workbook.add_format(
        {"bg_color": "#C6EFCE", "font_color": "#006100"}
    )

    # Write a conditional format over a range.
    worksheet_1.conditional_format(
        start_row,
        start_column,
        end_row,
        end_col,
        {"type": "formula", "criteria": '=Sheet2!A1="a"', "format": condition_format},
    )
    worksheet_3.conditional_format(
        start_row,
        start_column,
        end_row,
        end_col,
        {"type": "formula", "criteria": '=Sheet2!B1="a"', "format": condition_format},
    )

    # Close the Pandas Excel writer and output the Excel file.
    writer.save()
