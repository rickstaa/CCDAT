### Import python modules ###
import pandas as pd
import numpy as np
import os
import xlsxwriter

### Needed Variables ###
timestep = 0.166667/100  # 100 samples is 0.166667
player_name = " "

### Get current path ###
dirname = os.path.dirname(__file__)

### import the csv data and time sections file ###
df_data = pd.read_csv(r"C:\Users\ricks\OneDrive\Development\Tools\CGDAT\input_data\input_data.csv", header=0, encoding='utf-8')
df_data.columns = df_data.columns.str.title()         # Capitalize columns to prohibit key errors
df_data_time = pd.read_csv(r"C:\Users\ricks\OneDrive\Development\Tools\CGDAT\input_data\time_data.csv", header=0, encoding="utf-8", sep=';')
df_data_time.columns = df_data_time.columns.str.title()

### Create extra time column ###
df_data['Time'] = df_data['Timestamp']*timestep
df_data.index = pd.to_datetime(df_data['Time'], unit='s')

### Convert begin and start times to datetime format ###
begin_times = pd.to_datetime(df_data_time['Start Time'], format='%H:%M:%S.%f').dt.time
end_times = pd.to_datetime(df_data_time['End Time'], format='%H:%M:%S.%f').dt.time

### Get data within specific time ranges ###
# Begin time: List containing begin times [00:02:30, 00:07:30, ...]
# End times: List containing end times [00:05:00, 00:10:00, ...]
df_sections = [df_data.between_time(i, j) for (i,j) in zip(begin_times, end_times)]
df_result = pd.concat(df_sections) # Add all the df sections together

### Specify Conditions ###"
condition1 = ((df_data['Speed'] > 10) & (df_data['Acceleration'] > 0.69) & (df_data['Name'] == player_name))
condition2 = ((df_data['Speed'] > 10) & (df_data['Acceleration'] > 1.30) & (df_data['Name'] == player_name))
condition3 = ((df_data['Speed'] > 7.5) & (df_data['Acceleration'] > 1.30) & (df_data['Name'] == player_name))
condition4 = ((df_data['Speed'] > 7.5) & (df_data['Acceleration'] < (-1.30)) & (df_data['Name'] == player_name))

### Test conditions ###
df_data_sub_1 = df_data[condition1]
df_data_sub_2 = df_data[condition2]
df_data_sub_3 = df_data[condition3]
df_data_sub_4 = df_data[condition4]

### Only get collumns you want ###
df_data_sub_1 = df_data_sub_1[['Speed','Acceleration']]
df_data_sub_2 = df_data_sub_2[['Speed','Acceleration']]
df_data_sub_3 = df_data_sub_3[['Speed','Acceleration']]
df_data_sub_4 = df_data_sub_4[['Speed','Acceleration']]

### Save in excel file ###
# Each condition on one sheet

# Create a Pandas Excel writer using XlsxWriter as the engine.
filename = os.path.join(dirname, 'data_analyse_result.xlsx')
writer = pd.ExcelWriter(filename, engine='xlsxwriter')

# df_data.to_excel(writer, sheet_name='Sheet1')
df_data_sub_1.to_excel(writer, sheet_name='Condition1')
df_data_sub_2.to_excel(writer, sheet_name='Condition2')
df_data_sub_3.to_excel(writer, sheet_name='Condition3')
df_data_sub_4.to_excel(writer, sheet_name='Condition4')
writer.save()


# def game_analyse(input_file, output_path, output_name, condition_list):
print("done")