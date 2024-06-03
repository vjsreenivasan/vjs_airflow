from airflow.models import Connection
from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError


def get_connection_info(airflow_conn_id: str):
    """
    This function get connection info from airflow

    Parameters:

    airflow_conn_id (str): db_funnow_v2 | db_data_warehouse | db_elasticsearch
    """

    conn_info = Connection.get_connection_from_secrets(airflow_conn_id)

    conn_info_dict = {
        "conn_type": conn_info.conn_type,
        "host": conn_info.host,
        "user": conn_info.login,
        "passwd": conn_info.password,
        "db": conn_info.schema,
        "port": conn_info.port,
    }

    return conn_info_dict


def create_sql_engine(conn_info_dict: dict):
    if conn_info_dict["conn_type"] == "mysql":
        engine = create_engine(
            f"{conn_info_dict['conn_type']}+pymysql://{conn_info_dict['user']}:{conn_info_dict['passwd']}@{conn_info_dict['host']}:{conn_info_dict['port']}/{conn_info_dict['db']}"
        )
    elif conn_info_dict["conn_type"] == "postgres":
        url = f"{conn_info_dict['conn_type']}ql://{conn_info_dict['user']}:{conn_info_dict['passwd']}@{conn_info_dict['host']}:{conn_info_dict['port']}/{conn_info_dict['db']}"
        engine = create_engine(
            url,
            connect_args={"options": "-csearch_path={}".format(None)},
        )

    # test connection
    try:
        engine.connect()
        print("connection success")
    except SQLAlchemyError as err:
        print("error", err.__cause__)
        print(engine.connect())
    return engine
