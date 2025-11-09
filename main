import pandas as pd
import usecase.df_extension as df_extension
import usecase.staff_extension as staff_extension
import pyperclip
import datetime
from model.ConfigHelper import ConfigHelper

configHelper = ConfigHelper('config.ini')
config_data = configHelper.config
excel_file = config_data['base']['excelFile']
sheetIndex = int(config_data['base']['sheetIndex'])

df = pd.read_excel(excel_file, sheet_name=sheetIndex)
clean_df = df_extension.clean_data(df)
staffs = staff_extension.create_staffs(clean_df)
scheduleList = staff_extension.get_schedule_list(staffs)

# print(df_extension.clean_data(df))
# print(scheduleList)
# for s in staffs:
# 	print(s.__dict__)

year = int(config_data['base']['year'])
month = int(config_data['base']['month'])

for index, staff in enumerate(staffs):
    print(f"[{index}] {staff.name} {staff.staffNo}")

selected_index = input("Copy [X] schedule: ")

selected_staff = staffs[int(selected_index)]


result = []
for scheduleKeys in selected_staff.schedule.keys():
    schedule_date = datetime.datetime(year, month, int(scheduleKeys))
    # print(schedule_date)
    # print(selected_staff.schedule[scheduleKeys])
    # print(config_data['Schedule'][selected_staff.schedule[scheduleKeys]])
    row = f'{schedule_date.day}/{schedule_date.month} ({schedule_date.strftime("%a")}) {config_data["Schedule"][selected_staff.schedule[scheduleKeys]]}'
    result.append(row)


pyperclip.copy("\n".join(result))
print("----------------")
print("Copied to clipboard:")
print("\n".join(result))
