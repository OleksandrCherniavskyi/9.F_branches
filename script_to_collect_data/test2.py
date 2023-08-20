import psycopg2
from bard_token import db_name, db_user, db_pass, db_host, db_port

conn = psycopg2.connect(
    database=db_name,
    user=db_user,
    password=db_pass,
    host=db_host,
    port=db_port
)
conn.autocommit = True

c = conn.cursor()



#table_1 = """CREATE TABLE IF NOT EXISTS branch (
#    id SERIAL PRIMARY KEY,
#    full_name VARCHAR(255),
#    born_date DATE,
#    death_date DATE,
#    source_link VARCHAR(255)
#);"""
#table_2 = """CREATE TABLE IF NOT EXISTS relationships (
#    id SERIAL PRIMARY KEY,
#    parent_id INT,
#    child_id INT,
#    FOREIGN KEY(parent_id) REFERENCES branch(id),
#    FOREIGN KEY(child_id) REFERENCES branch(id)
#);"""
#c.execute(table_1)
#c.execute(table_2)


#drop_relativ = '''ALTER TABLE relationships DROP CONSTRAINT relationships_parent_id_fkey, DROP CONSTRAINT relationships_child_id_fkey;'''
#c.execute(drop_relativ)

#drop_table_1 = """DROP TABLE IF EXISTS relationships ;"""
drop_table_2 = """DROP TABLE IF EXISTS branch ;"""
#c.execute(drop_table_1)
c.execute(drop_table_2)


#delete_data_in_table = """DELETE FROM branch;"""
#c.execute(delete_data_in_table)


c.close()