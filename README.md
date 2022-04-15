# The tools-python project
## What does it contain ?
A collection of scripts written in python that can be run from the command line
## What does it solve ?
A lot of time consuming tasks that need to be done through UI, can be invoked as
a simple command from one's laptop.
<br>
For e.g to deploy a latest master PE-PC through rdm UI, it takes at least 2-3 mins:
<br>With tools-python, just run the command: `rdmdeploy.py --nocmsp --duration 4`
<br> taking just 5 secs.
<br> The same goes for extending the expiry of deployment, checking deployment status,
creating an active directory, crud operations<br>
on users, roles, permissions, acps etc (especially useful in rbac context)

## Download and install
### Pre-requisites
Python 3 is needed. The code may not work on python 2.
### General steps:
Clone the directory into some place and from inside the project directory,
<br> run pip install. All your scripts are available in system path itself, and<br>
can be invoked from anywhere in the system.

### Example on mac:
```
~/coding$ git clone https://${GIT_TOKEN}@github.com/sidharthr8/tools-python
~/coding$ cd tools-python
~/coding/tools-python$ python3 -m pip install .
```
## Project structure
`{project_root}/tools-python/` <br> The top level package of the codebase.<br><br>
`{project_root}/tools-python/{component}/` <br> code belonging to the particular component<br>
resides in this package or the sub-packages, if any.<br><br>
`{project_root}/tools-python/{component}/bin/` <br>
The scripts directly callable from anywhere in the system, reside here.
