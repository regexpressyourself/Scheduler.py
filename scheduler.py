'''
------------
TO DO
------------
    [x]random assignment of shifts to employees
    [x]does not go over hours alloted for each TM
    [x]does not interfere with TM day off requests
    [ ]does not interfere with TM shift off requests
    [ ]if possible, avoid clopens
    [ ]change inputs for day off inputs
    [ ]comment out code
    [ ]refine excel worksheet- colors, bold, data manipulation, etc
    [ ]add shift preference
    [ ]get off cli
    [x]fix day off user input
    [ ]
    [ ]
    [ ]
    [ ]
    [ ]
    [ ]
    [ ]
    [ ]

'''
import random
import xlwt

def CheckTime(time):
    '''
    checks that time is entered in the format "hh:mma" or "hh:mmp"
    '''
    while True:
        try:
            float(time.split(':')[0])
            if len(((time.split(':')[0])))==2:
                try:
                    float((time.split(':')[1][:2]))
                    if len(((time.split(':')[1][:2])))==2:
                        if str((time.split(':')[1][2]))=='a':
                            break
                        elif str((time.split(':')[1][2]))=='p':
                            break
                        else:
                            print 'Please enter time in hh:mma or hh:mmp format'
                            time=raw_input('Please re-enter time: ')
                    else:
                        print 'Please enter time in hh:mma or hh:mmp format'
                        time=raw_input('Please re-enter time: ')
                except ValueError:
                    print 'Please enter time in hh:mma or hh:mmp format'
                    time=raw_input('Please re-enter time: ')
            else:
                print 'Please enter time in hh:mma or hh:mmp format'
                time=raw_input('Please re-enter time: ')
        except ValueError:
            print 'Please enter time in hh:mma or hh:mmp format'
            time=raw_input('Please re-enter time: ')
    return time

def CheckInt(num):
    '''
    Checks that number is integer
    '''
    while True:
        try: 
            int(num)
            return int(num)
            break
        except ValueError:
            num = raw_input('Please enter an integer: ')

def TimetoDec(time):
    '''
    time is entered in the format "hh:mma" or "hh:mmp" and returned in a 
    decimal form from 00.00 up to 23.99
    '''
    hour = float(time.split(':')[0])
    minute = float(time.split(':')[1][:2])
    ampm = str(time.split(':')[1][2])

    if ampm == 'p':
        if hour != 12:
            hour += 12.0

    minute = minute/60.0

    return hour+minute


def DectoTime(dec):
    '''
    time is entered in the decimal form (see TimetoDec) and
    returned in the hh:mma or hh:mmp form
    '''
    dec = str(dec)
    time = dec.split('.')
    minute = int(int(time[1])*.6)
    if int(time[0])>12:
        hour = int(time[0])-12
        ampm = 'p'
    else:
        hour = int(time[0])
        ampm = 'a'
    hour = str(hour)
    minute = str(minute)
    if len(minute)<2:
        if minute == '0':
            minute = '0' + minute
        else:
            minute = minute + '0'
    return hour + ':' + minute + ampm


class Day:
    '''
    The Day class keeps a dictionary consisting of the 
    start and stop times of each shift in the form
    {start:stop, start:stop}.
    Times are maintained in both decimal and regular form.
    '''
    def __init__(self):
        self.shiftRegDict = {}
        self.shiftRegList = []
        self.shiftDecDict = {}
        self.shiftDecList = []
    def addShift(self, start, end):
        self.shiftRegList.append((start,end))
        self.shiftRegDict = dict(self.shiftRegList)
        self.shiftDecList.append((TimetoDec(start),TimetoDec(end)))
        self.shiftDecDict = dict(self.shiftDecList)
#    def editShift(self):
         
    def viewShift(self):
        return self.shiftRegDict

class TM:
    '''
    Maintains a class for each employee (TM). Keeps track of 
    maximum hours, a blacklist for days they can't work, and functions
    to add a shift
    '''
    def __init__(self, maxHours):
        self.maxHours = maxHours
        self.totalTime = 0
        self.blackList = {}
        self.shiftDict = {}
        self.printShiftDict = {}
    def canWork(self, day, strDay, start, end):
        shiftTime = end-start
        if self.totalTime + shiftTime <= self.maxHours:
            if day in self.shiftDict:
                return False
            elif strDay.lower() in self.blackList:
                return False
            else:
                return True
        else:
            return False
    def addShift(self, day, stringday, start, stop):
        shiftTime = stop-start
        try: 
            self.shiftDict[day]    
            self.shiftDict[day][start] = stop
        except:
            self.shiftDict[day] = {start:stop}
        try:
            self.printShiftDict[day]
            self.printShiftDict[day][DectoTime(start)] = DectoTime(stop)
        except:
            self.printShiftDict[day] = {DectoTime(start):DectoTime(stop)}
        self.totalTime += shiftTime
    def maxHours(self, newShift):
        if self.totalTime + newShift > self.maxHours:
            return False
        elif self.totalTime + newShift <= self.maxHours:
            return True
    def blacklist(self, day, dayClass):
        self.blackList[day] = dayClass

'''
classify all the days
'''
Monday = Day()
Tuesday = Day()
Wednesday = Day()
Thursday = Day()
Friday = Day()
Saturday = Day()
Sunday = Day()

# dayList is used mostly for indexing purposes, as dictionaries have no index
dayList = [Monday,Tuesday,Wednesday,Thursday,Friday,Saturday,Sunday]

#dayPrintDict is for error checking the days off entries
dayPrintDict = {'monday':Monday,'tuesday':Tuesday,'wednesday':Wednesday,'thursday':Thursday,'friday':Friday,'saturday':Saturday,'sunday':Sunday}

'''
 dayDict allows the class name to correlate with a string of the name for
 printing purposes
'''
dayDict = {Monday:'Monday', Tuesday:'Tuesday', Wednesday:'Wednesday', Thursday:'Thursday', Friday:'Friday', Saturday:'Saturday',Sunday:'Sunday'}

#testing data
Monday.addShift('07:00a','03:30p')
Monday.addShift('02:00p','10:30p')
Monday.addShift('11:00a','06:30p')

Tuesday.addShift('07:00a','03:30p')
Tuesday.addShift('02:00p','10:30p')
Tuesday.addShift('11:00a','06:30p')

Wednesday.addShift('07:00a','03:30p')
Wednesday.addShift('02:00p','10:30p')
Wednesday.addShift('11:00a','06:30p')

Thursday.addShift('07:00a','03:30p')
Thursday.addShift('02:00p','10:30p')
Thursday.addShift('11:00a','06:30p')

Friday.addShift('07:00a','03:30p')
Friday.addShift('02:00p','10:30p')
Friday.addShift('11:00a','06:30p')

Saturday.addShift('07:00a','03:30p')
Saturday.addShift('02:00p','10:30p')
Saturday.addShift('11:00a','06:30p')

Sunday.addShift('07:00a','03:30p')
Sunday.addShift('02:00p','10:30p')
Sunday.addShift('11:00a','06:30p')
''' ------------------------------------------------------------------------
#get shift data for each day
for day in dayList:
    shiftNum = CheckInt(raw_input('How many shifts for ' + str(dayDict[day]) + '? '))
    x = 0
    while x < shiftNum:
        start = CheckTime(raw_input('Enter the start time of the shift: '))
        end = CheckTime(raw_input('Enter the end time of the shift: '))
        day.addShift(start, end)
        day.viewShift()
        x+=1
'''
'''
tmDict and tmList work simlarly to dayDict and dayList to store classes and
printable names for all the employees
'''
tmDict = {}
tmList = []
tmNum = CheckInt(raw_input('How many employees are you staffing? '))

#make a class for each tm and a add a corresponding name
x = 0
while x < tmNum:
    name = raw_input('What is the name of employee number %i? '%(x+1))
    tmHours = CheckInt(raw_input('How many hours can %s work? '%name))
    classname = name
    classname = TM(tmHours)
    tmList.append(classname)
    tmDict[classname] = name
    x += 1

# add days off to tm.blackList
for tm in tmList:
    while True:
        blacklist = raw_input("What days can't %s work? (press enter to skip ) "%tmDict[tm]).lower()
        if blacklist in dayPrintDict:
            tm.blacklist(blacklist, dayPrintDict[blacklist])
        elif blacklist == '':
            break
        else:
            print "Please enter a day, or press enter to finish "

#unassigned stores all the extra shifts (hence the huge "maxhour" number)
unassigned = TM(999999999999999999999999999999999)

'''
OK this is the convuluted part. Here goes:
- For every shift, a string of random integers (which reperesent the index
numbers of tmList) is generated.
- Using these random integers, a tm is selcted at random. If they pass the
"caWork" test, the shift is assigned to them. Otherwise, we just continue down
the list.
- If every TM fails the "canWork" test, the shift is assigned to "unassigned" and
an error message is printed. 
'''

for day in dayDict:
    for shift in day.shiftDecDict:
        numList = []
        for num in range(0,len(tmList)):
            numList.append(num)
        random.shuffle(numList)
        x=0
        while True:
            if x >= len(numList):
                print 'Following shift could not be assigned:'
                print dayDict[day],
                print str(DectoTime(shift)) + '-' + str(DectoTime(day.shiftDecDict[shift]))
                unassigned.addShift(day, dayDict[day], shift, day.shiftDecDict[shift])
                break
            else:
                shiftTM = tmList[numList[x]]
            if shiftTM.canWork(day, dayDict[day], shift, day.shiftDecDict[shift]):
                shiftTM.addShift(day, dayDict[day], shift, day.shiftDecDict[shift])
                break
            else:
                x+=1

#Excel printing

workbook = xlwt.Workbook()
sheet = workbook.add_sheet('Schedule')

grey = xlwt.easyxf('pattern: pattern solid;')
grey.pattern.pattern_fore_colour = 22

bold_string = "font: bold on"
bold = xlwt.easyxf(bold_string)

x=0
while x<len(dayList):
    sheet.write(0,x+1,dayDict[dayList[x]], bold)
    x += 1

x=1
tmList.append(unassigned)
tmDict[unassigned] = 'unassigned'
sheet.write(0,8,"Total Hours", bold)
for tm in tmList:
    sheet.write(x,0,tmDict[tm], bold)
    for day in tm.printShiftDict:
        y = 0
        for shift in tm.printShiftDict[day]:
            time = shift + ' - ' +  tm.printShiftDict[day][shift]
            sheet.write(x+y, dayList.index(day)+1, time)
            y += 1
    y = 0
    for day in tm.blackList:
        sheet.write(x+y, dayList.index(tm.blackList[day])+1, 'Not Available',grey)
        y += 1
    sheet.write(x,8,tm.totalTime)
    x += 1

x = 1
while x <= len(tmList)-1:
    y = 1
    while y <= len(dayList):
        try:
            sheet.write(x, y, '', grey)
        except:
            pass
        y += 1
    x += 1


workbook.save('schedule.xls')
