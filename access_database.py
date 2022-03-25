import sshtunnel
from sqlalchemy import create_engine

DB_ADDRESS = "127.0.0.1"
DB_ADDRESS_PORT = None
DB_NAME = "database"
DB_USER_NAME = "user"
DB_PASSWORD = "password"

SSH_ENABLE = True
SSH_ADDRESS = "127.0.0.1"
SSH_ADDRESS_PORT = 22
SSH_USER_NAME = "user"
SSH_PKEY = "./.ssh/id_rsa"
SSH_REMOTE_BIND_ADDRESS = "127.0.0.1"
SSH_REMOTE_BIND_ADDRESS_PORT = 3306

def db_engine(server):
    db_address = DB_ADDRESS
    db_address_port = DB_ADDRESS_PORT
    db_name = DB_NAME
    db_user_name = DB_USER_NAME
    db_password = DB_PASSWORD

    if server is not None:
        db_address_port = server.local_bind_port
    
    if db_address_port is None:
        return create_engine(
            f"mysql+pymysql://{db_user_name}:{db_password}@{db_address}/{db_name}"
        )
    else:
        return create_engine(
            f"mysql+pymysql://{db_user_name}:{db_password}@{db_address}:{db_address_port}/{db_name}"
        )

def jump_server():
    if SSH_ENABLE:
        return sshtunnel.SSHTunnelForwarder(
            (SSH_ADDRESS, SSH_ADDRESS_PORT),
            ssh_username=SSH_USER_NAME,
            ssh_pkey=SSH_PKEY,
            remote_bind_address=(SSH_REMOTE_BIND_ADDRESS, SSH_REMOTE_BIND_ADDRESS_PORT)
        )

def select_table(engine):
    sql = f"""
        SELECT column1, column2 FROM table LIMIT 1;
    """

    with engine.connect() as conn:
        result = conn.execute(sql)
        for row in result:
            if row["column1"] is not None:
                print("column1: ", row["column1"])
            if row["column1"] is not None:
                print("column2: ", row["column2"])

if __name__ == "__main__":
    server = jump_server()
    if server is not None:
        server.start()

    engine = db_engine(server)

    select_table(engine)

    if server is not None:
        server.close()
