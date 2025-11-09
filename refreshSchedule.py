import pandas as pd
import usecase.df_extension as df_extension
import usecase.staff_extension as staff_extension
from model.ConfigHelper import ConfigHelper

configHelper = ConfigHelper('config.ini')
config_data = configHelper.config

excel_file = config_data['base']['excelFile']
sheetIndex = int(config_data['base']['sheetIndex'])

df = pd.read_excel(excel_file, sheet_name=sheetIndex)
clen_df = df_extension.clean_data(df)
staffs = staff_extension.create_staffs(clen_df)
scheduleList = staff_extension.get_schedule_list(staffs)

# configHelper.create_schedule_list_txt()
configHelper.refreshSchedule(scheduleList)

