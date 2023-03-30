import json

with open('me.json') as f:
  info = json.load(f)

print('Name:',info['name'])
print('\nschool:')

for schools in info['school']:
    print("%s "%schools)

print('\ngrade:')

for grades in info['grade']:
    print("%d "%grades)
print('\nteacher:',info['teacher'])
print('\nclassmate:')

for classmates in info['classmate']:
    print("%s "%classmates)

print('\nsport:')

for sports in info['sport']:
    print("%s "%sports)
