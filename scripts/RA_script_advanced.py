# -*- coding: utf-8 -*-

### Import modules ###
import pandas as pd
import numpy as np
import os
import xlsxwriter

### Get information from the user ###
print "\n=== Welcome to the game analyser tool ==="
print "Please put the data file you want to analyse in the data folder.\n"
input_file_name = raw_input("What is the name of the data file: ")
output_file_name = raw_input("How do you want to name the output file: ")
print "\n What conditions do you want to analyse. Put empty line when done.ty line when your done."
input_conditions = []
line = raw_input("Condition 1: ")
counter = 1
while line != "\r":
    input_conditions.append(line)
    counter += 1
    line = raw_input("Condition " + str(counter)+ ": ")

### Get the conditions out of the answers in the right answers ###
conditions = []
for item in input_conditions:
    condition_split = item.split()
    conditions.append(item.split())
    string_length = len()

print conditions
# ]
# ### Get current path ###
# dirname = os.path.dirname(__file__)

# ### import the csv file, note that the encoding has been set to ANSI###
# filename = os.path.join(dirname, 'test.csv')
# df = pd.read_csv(filename, header=0, low_memory=False) #, encoding = "ANSI")

# ### Specify Conditions ###
# condition1 = ((df['Speed'] > 10) & (df['Acceleration'] > 0.69))
# condition2 = ((df['Speed'] > 10) & (df['Acceleration'] > 1.30))
# condition3 = ((df['Speed'] > 7.5) & (df['Acceleration'] > 1.30))
# condition4 = ((df['Speed'] > 7.5) & (df['Acceleration'] < (-1.30)))

# ### Test conditions ###
# df_sub_1 = df[condition1]
# df_sub_2 = df[condition2]
# df_sub_3 = df[condition3]
# df_sub_4 = df[condition4]

# ### Only get collumns you want ###
# df_sub_1 = df_sub_1[['Speed','Acceleration']]
# df_sub_2 = df_sub_2[['Speed','Acceleration']]
# df_sub_3 = df_sub_3[['Speed','Acceleration']]
# df_sub_4 = df_sub_4[['Speed','Acceleration']]

# ### Get data around found times ###

# ### Save in excel file ###
# # Each condition on one sheet

# # Create a Pandas Excel writer using XlsxWriter as the engine.
# filename = os.path.join(dirname, 'data_analyse_result.xlsx')
# writer = pd.ExcelWriter(filename, engine='xlsxwriter')

# # df.to_excel(writer, sheet_name='Sheet1')
# df_sub_1.to_excel(writer, sheet_name='Condition1')
# df_sub_2.to_excel(writer, sheet_name='Condition2')
# df_sub_3.to_excel(writer, sheet_name='Condition3')
# df_sub_4.to_excel(writer, sheet_name='Condition4')
# writer.save()


# def game_analyse(input_file, output_path, output_name, condition_list):
