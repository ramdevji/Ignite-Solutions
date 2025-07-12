import os

class Config:
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'DATABASE_URL',
        'postgresql://ramdev:ramdev@localhost:5432/ignite_solutions'
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = True
