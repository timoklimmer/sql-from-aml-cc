import os
import struct

import pyodbc
from azure.core.credentials import TokenCredential
from azure.identity import (
    AzureCliCredential,
    AzurePowerShellCredential,
    ChainedTokenCredential,
    ManagedIdentityCredential,
)

server = os.environ.get("SQL_SERVER", "fidge-aml-sql-spike-server.database.windows.net")
database = os.environ.get("SQL_DATABASE", "AdventureWorksLT")

print(f"Server: {server}")
print(f"Database: {database}")
print(f"")


def pyodbc_azure_sql_connection(server, database):
    """Return a connected PyODBC connection to an Azure SQL instance."""
    SQL_COPT_SS_ACCESS_TOKEN = 1256
    credential: TokenCredential = ChainedTokenCredential(
        ManagedIdentityCredential(), AzureCliCredential(), AzurePowerShellCredential()
    )
    token = credential.get_token("https://database.windows.net/.default").token.encode("UTF-16-LE")
    token_struct = struct.pack(f"<I{len(token)}s", len(token), token)
    connString = f"Driver={{ODBC Driver 17 for SQL Server}};Server={server};Database={database}"
    return pyodbc.connect(connString, attrs_before={SQL_COPT_SS_ACCESS_TOKEN: token_struct})


with pyodbc_azure_sql_connection(server, database) as sql_conn:
    cursor = sql_conn.cursor()
    user_name = cursor.execute("SELECT ORIGINAL_LOGIN()").fetchone()[0]


print(f"Hello {user_name}!")
