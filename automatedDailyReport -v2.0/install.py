import os
import pip

print('Installing required dependencies for Automatic Daily Manual Reports script')
os.chdir('/Users/noah.p/PycharmProjects/autoReports')
print('Reading dependencies file `requirements.txt`:')
dependencies = []

with open('the_requirements.txt') as requirements:
    for line in requirements:
        print('   > Found `%s`' % line.strip())
        dependencies.append(line.strip())
print('Installing dependencies to `dependencies` folder:')

for dependency in dependencies:
    pip.main(['install', '--target', 'dependencies', dependency])
    print('   > `%s` done!' % dependency)

print('Packing the dependencies directory...')
os.chdir('dependencies')
open('__init__.py', 'w').close()

print('All done and ready to go: run `AutoManualDailyReports`')
