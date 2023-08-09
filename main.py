import json

from bardapi import Bard
from bard_token import token
import os
import pandas as pd

os.environ["_BARD_API_KEY"] = token

def get_family_tree(name):
    """Gets the family tree of the given name."""
    # JSON
    message = "In JSON (full_name, maiden_name, born_date, depth_date, father, mother, childrens, source_link)  format explain. If some information is unknown leave empty(null). For the person {}?".format(name)

    # Table
    #message = "Create table ( First Name, Last Name, Family Name, Born Date, Depth Date, Father, Mother, Children, Source Link)  format explain, Fill it the table for  {}?".format(
    #  name)

    # SQL
    #message = "Create a query to insert INTO tree (first_name, last_name, family_name, born_date, depth_date, father, mother, children, source_link) VALUES, Where value is data you can find in internet for the person {}".format(
    # name)

    content = Bard().get_answer(str(message))['content']
    print(content)
    start_pos = content.find("{")
    end_pos = content.find("}")
    content_json = content[start_pos:end_pos + 1].strip()


    print(content_json)
    data_dict = json.loads(content_json)

    full_name = data_dict["full_name"]
    maiden_name = data_dict["maiden_name"]
    born_date = data_dict["born_date"]
    death_date = data_dict["death_date"]
    father = data_dict["father"]
    mother = data_dict["mother"]
    children = data_dict["children"]
    for child in children:
        child
    source_link = data_dict["source_link"]

    sql_query = f"""
    INSERT INTO tree (full_name, maiden_name, born_date, death_date, source_link)
    VALUES (?, ?, ?, ?, ?);
    """

    import sqlite3

    conn = sqlite3.connect("treeDB.db")
    c = conn.cursor()
    c.execute(sql_query, (full_name, maiden_name, born_date, death_date, source_link))
    conn.commit()
    conn.close()



if __name__ == "__main__":
    name = input("Enter the name: ")
    get_family_tree(name)