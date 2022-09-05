"""
Script to turn yaml into a schedule
"""
from datetime import datetime, timedelta
from colored import fg, bg, attr

import yaml

with open('Eos314_2022.yml') as f:
    data = yaml.safe_load(f)
    print(data)
    for subject in data['subjects']:
        print(subject)

subject_num = 0
subjects = data['subjects']
for subject in subjects:
    subject['assigned'] = 0
    subject['classes'] = subject.get('classes', 3)
    subject['type'] = subject.get('type', 'lecture')

assignments = []
# print out the schedule.

date = data['first-day']
print(date)
html = '<table>\n'
html += '<tr><th>Date</th> <th>Type</th> <th>Activity</th> <th>Reading due</th> <th>Assignment Due</th>\n'
while (data['last-day'] - date).total_seconds() >= 0:
    datestr = date.strftime('%a %d %b')

    title = None
    for special in data['special-days']:
        if date == special['date']:
            title = special['title']
            type = special['type'].upper()
            if type == 'CANCELLED':
                thecolor = 'sandy_brown'
                csscolor = 'sandybrown'
            elif type == 'QUIZ':
                thecolor = 'orange_4a'
                csscolor = 'lightsalmon'
            elif type == 'HOLIDAY':
                thecolor = 'pale_green_1b'
                csscolor = 'lightgreen'
            elif type == 'FIELD':
                thecolor = 'cornflower_blue'
                csscolor = 'cornflowerblue'
            emp = ''
            print(f'{bg(thecolor)} {datestr}  {type.upper():10}    {title:40} {emp:18} {bg("white")}')
            html += f'<tr bgcolor={csscolor}> <td>{datestr}</td>  <td>{type.upper()}</td>  <td>{title}</td> <td></td> <td></td> </tr>\n'
            break

    # not a special day?  slot in next class.
    if not title:
        if date.weekday() in [1, 2, 4]:
            for subject_num, subject in enumerate(subjects):
                if subject['assigned'] < subject['classes']:
                    title = subject['title']
                    type = subject['type']
                    reading = subject.get('reading', '')
                    if subject['assigned'] == reading:
                        reading = f'Read {subject_num:02d}'
                    else:
                        reading = ''

                    # check if there is an assignment for today
                    assign = ''
                    for assi in assignments:
                        if (assi['due'] - date).total_seconds() <= 0:
                            assign = assi['str']
                            assignments.remove(assi)

                    if type == 'lecture':
                        type = ''

                    thecolor = 'white' if subject_num % 2 else 'grey_82'
                    print(f'{bg(thecolor)} {datestr}  {type:10} {subject_num:02d} {title:40} {reading:11} {assign:6} {bg("white")} ')
                    thecolor = 'white' if subject_num % 2 else 'lightgrey'
                    html += f'<tr bgcolor={thecolor}> <td> {datestr}</td> <td>{type:10}</td> <td>{subject_num:02d} {title:40}</td> <td> {reading:11}</td> <td> {assign:6}</td> </tr>\n'
                    # create an entry to assignments to track when this one is due.
                    assign = subject.get('assign', None)
                    if assign and subject['assigned']+1 == subject['classes']:

                        new = {'assign': assign,
                               'str': f'Ex {subject_num:02d}',
                               'due': date + timedelta(days=assign)}
                        assignments += [new]
                    subject['assigned'] += 1
                    break

    date = date + timedelta(days=1)

html += '</table>\n'

print('Left over assignments:')
for assignment in assignments:
    print(assignment)
print()

print('Left over classes:')
for subject_num, subject in enumerate(subjects):
    if subject['assigned'] < subject['classes']:
        print(subject)

print()

with open('example.html', 'w') as f:
    f.write(html)