def isLeapYear(y):
	# Every year divisible by 4 is a leap year.
	# However, every year divisible by 100 is not a leap year.
	# However, every year divisible by 400 is a leap year after all.
	return (y % 4 != 0 or (y % 100 == 0 and y % 400 != 0)) == False

def GetMonths(y):
	return [31, 29 if isLeapYear(y) else 28,
			31, 30, 31,
			30, 31, 31,
			30, 31, 30,
			31]

def GetTotalDays(y, m, d):
	year = y - 1
	# get all days plus all leap years, minus non-leap years
	days = year * 365 + year / 4 - year / 100 + year / 400
	# the years before 1582 were all leap if divisible by 4
	if year > 1582:
		days += 12
	else:
		days += year / 100
		days -= year / 400
	# validate month
	if m > 12:
		m = 12
	# get the days for the month up to the current one
	months = GetMonths(y)
	for i in range(m - 1):
		days += months[i]
	# validate day
	if months[m - 1] < d:
		d = months[m - 1]
	# now add the current days of the month
	days += d
	# now adjust for the 10 missing days (Oct 4 - Oct 15, 1582)
	if days > 577737:
		days -= 10
	return days

def GetDate(totaldays):
	# method by Branislav L. Slantchev
	if totaldays > 577737:  # ReformDayNumber
		totaldays += 10
	y = int(totaldays / 365)
	d = int(totaldays % 365)
	if y < 1700:
		d -= y / 4
	else:
		d -= y / 4
		d += y / 100
		d -= y / 400
		d -= 12
	while d <= 0:
		d += 366 if isLeapYear(y) else 365
		y -= 1
	# y is the number of elapsed years, add 1 to get current
	y += 1
	# figure out the month and current day too
	months = GetMonths(y)
	for m in range(12):
		days = months[m]
		if d > days:
			d -= days
		else:
			break
	m += 1
	return [y, m, d]

if __name__ == "__main__":  # run tests
	assert GetDate(GetTotalDays(2008, 2, 29)) == [2008, 2, 29]
	assert GetDate(GetTotalDays(2009, 2, 29)) == [2009, 2, 28]
	assert GetDate(GetTotalDays(2008, 2, 28) + 1) == [2008, 2, 29]
	assert GetDate(GetTotalDays(2009, 2, 28) + 1) == [2009, 3, 1]
	assert GetDate(GetTotalDays(2008, 2, 20) + 10) == [2008, 3, 1]
	assert GetDate(GetTotalDays(2009, 2, 20) + 10) == [2009, 3, 2]
