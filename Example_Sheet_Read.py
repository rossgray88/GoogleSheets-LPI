from shotsheet import shotsheet

s = shotsheet()
values = s.googlesheetsloader(
    id='1RpeozLpwos29tEZN1ynouHcuUb1cWiPaNxnXMCTLlIE',
    tokenloc='token.pickle',
    sheetname='Sheet1!A1:Z100'
)
print(values)