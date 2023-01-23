import os
import snowflake.connector
from dotenv import dotenv_values, load_dotenv


load_dotenv()

config = dotenv_values(".env")


# Gets the version
ctx = snowflake.connector.connect(
    user='mvmtaylor',
    password='T@sk12!$',
    account='aha32444.us-east-1'
    )
cs = ctx.cursor()
try:
    cs.execute("SELECT current_version()")
    one_row = cs.fetchone()
    print(one_row[0])
finally:
    cs.close()
ctx.close()