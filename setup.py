from distutils.core import setup

setup(
    name='vvbasicfile',
    version='0.0.1b1',
    packages=['vvbasicfile'],
    url='https://github.com/verum-visu-toolkit/basicfile',
    license='MIT',
    author='Jacob Zimmerman (jczimm)',
    author_email='jczimm@jczimm.com',
    description='',
    install_requires=[
        # 'schema==0.6.6', # only necessary for vvbasicfile.static.*; these are not required
        'ijson==2.3',
        'ujson==1.35'
    ]
)
