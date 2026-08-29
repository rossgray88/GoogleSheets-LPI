from shotsheet import shotsheet

s = shotsheet()
values = s.googlesheetsloader(
    id='YOUR_SPREADSHEET_ID',
    tokenloc='token.pickle',
    sheetname='Sheet1!A1:Z100'
)
print(values)