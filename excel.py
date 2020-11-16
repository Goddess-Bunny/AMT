import xlwings as xw

places = {} # place:{date:[info]}
names = []

wb = xw.Book('excel.xlsx')

for sheet in wb.sheets: # getting places
	names = sheet.range('E2:H2').value

	i = 1
	
	while sheet.range(f'A{i}').value != 'Подразделение':
		i += 1
	
	i += 2
	
	while sheet.range(f'A{i}').value is not None:
		if not sheet.range(f'A{i}').value in places.keys():
			places[sheet.range(f'A{i}').value] = {sheet.name:sheet.range(f'E{i}:H{i}').value}
		else:
			places[sheet.range(f'A{i}').value][sheet.name] = sheet.range(f'E{i}:H{i}').value
		
		i += 1
		
wb_output = xw.Book()
sheet = wb_output.sheets[0]

sheet.range('A1').value = 'Подразделение'

sheet.range('B1').value = 'Дата'
sheet.range('C1:F1').value = names

wb_output.sheets[0].activate()

rng = xw.Range('A1:F1')

for col in rng.columns:
	col.autofit()

cur_row = 2

for place in places.keys():
	sheet.range(f'A{cur_row}').value = place
	
	for date in places[place].keys():
		sheet.range(f'B{cur_row}').value = date
		sheet.range(f'C{cur_row}:F{cur_row}').value = places[place][date]
		cur_row += 1
			