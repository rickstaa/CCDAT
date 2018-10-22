
# -*- coding: utf-8 -*-

### Import GUI modules ###
import 

### Import python modules ###
import pandas as pd
import numpy as np
import os
import xlsxwriter












conditions = ["Speed > 10 & Acceleration > 0.69",
              "Speed > 10 & Acceleration > 1.30",
              "Speed > 7.5 & Acceleration > 1.30",
              "Speed > 7.5 & Acceleration < (-1.30)",
              "Acceleration > 7.50 & Acceleration < -1.30",
              "Speed => Acceleration"
             ]

### Get current path ###
dirname = os.path.dirname(__file__)

### import the csv file, note that the encoding has been set to ANSI###
filename = os.path.join(dirname, r'data\test.csv')
df = pd.read_csv(filename, header=0, low_memory=False) #, encoding = "ANSI")

### Specify Conditions ###
condition1 = ((df['Speed'] > 10) & (df['Acceleration'] > 0.69))
condition2 = ((df['Speed'] > 10) & (df['Acceleration'] > 1.30))
condition3 = ((df['Speed'] > 7.5) & (df['Acceleration'] > 1.30))
condition4 = ((df['Speed'] > 7.5) & (df['Acceleration'] < (-1.30)))

### Test conditions ###
df_sub_1 = df[condition1]
df_sub_2 = df[condition2]
df_sub_3 = df[condition3]
df_sub_4 = df[condition4]

idx = np.where(condition3.values == True)[0]
for item2 in idx:
    condition1[item2-2]

### Only get collumns you want ###
df_sub_1 = df_sub_1[['Speed','Acceleration']]
df_sub_2 = df_sub_2[['Speed','Acceleration']]
df_sub_3 = df_sub_3[['Speed','Acceleration']]
df_sub_4 = df_sub_4[['Speed','Acceleration']]


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
