from distutils.core import setup

setup(
    name='cherryBGP',
    version='0.0.1',
    author='Michal Grzedzicki',
    author_email='lazy@iq.pl',
    packages=['cherryBGP'],
    scripts=['bin/cherryBGP',],
    description='Web frontend for exabgp blackholing',
    requires=["Cherrypy", "ipaddr",],
)