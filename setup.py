from setuptools import setup

requires = [
    'pyramid', # the framework
    'waitress', # the pyramid production ready server
    'pytest', # unit test framework
    'psycopg2', # postgresql driver
    'pyramid_tm', # database transaction manager
    'zope.sqlalchemy', # integrate transaction manager into pyramid
    'bcrypt', # encrypt auth
    'alembic',  # migration runner
    'webtest', # View Tests requirement
]

setup(
    name='user_management',
    install_requires=requires,
    entry_points={
        'paste.app_factory': [
            'main = user_management:main'
        ],
    },
)
