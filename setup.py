from setuptools import setup, find_packages
import os

def getscripts():
    scripts = []
    code_path = 'pythontools'
    for path in ['common', 'rdm', 'iam']:
        path = os.path.join(code_path, path)
        if os.path.isdir(path):
            binpath = os.path.join(path, 'bin')
            for p in os.listdir(binpath):
                p = os.path.join(binpath, p)
                if not os.path.isdir(p):
                    scripts.append(p)
    return scripts

# print(f'SUPER:{getscripts()}')
# exit()

setup(
    name='pythontools',
    version='0.0.1',
    author='Sidharth R',
    author_email='sidharth.r@nutanix.com',
    description='developer focussed commandline tools and libraries in python',
    long_description=open('README.md').read(),
    packages=find_packages(),
    install_requires=[
        'click==8.0.4',
        'requests==2.27.1'
    ],
    scripts=getscripts()
)
