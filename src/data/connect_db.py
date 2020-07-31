import os
import dotenv
from sqlalchemy import create_engine
from sqlalchemy.engine.url import URL

def create_engine_to_rds(db_name, echo=True, db_params=None):
    """
    Connect to RDS database instance described by `db_params` or environment variables or variables in .env
    """

    dotenv.load_dotenv()

    db_params = db_params or {}
    
    db_params['drivername'] = db_params.get('drivername', os.getenv('RDS_DRIVER', 'postgres'))
    db_params['username'] = db_params.get('username', os.getenv('RDS_USER', 'postgres'))
    db_params['password'] = db_params.get('password', os.getenv('RDS_PASS', 'password'))
    db_params['host'] = db_params.get('host', os.getenv('RDS_HOST', '0.0.0.0'))
    db_params['port'] = db_params.get('port', os.getenv('RDS_PORT', 5432))

    db_uri = f'{URL(**db_params)}/{db_name}'

    engine = create_engine(db_uri, executemany_mode="batch", echo=echo)

    return engine


if __name__ == "__main__":

    engine = create_engine_to_rds("postgres")
