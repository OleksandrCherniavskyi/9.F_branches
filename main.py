import json

from bardapi import Bard
from bard_token import token
import os
import pandas as pd

os.environ["_BARD_API_KEY"] = token

def get_family_tree(name):
    """Gets the family tree of the given name."""
    # JSON
    #message = "In JSON ( First Name, Last Name, Family Name, Born Date, Depth Date, Father, Mother, Children, Source Link)  format explain, Who is the family tree of {}?".format(name)

    # Table
    #message = "Create table ( First Name, Last Name, Family Name, Born Date, Depth Date, Father, Mother, Children, Source Link)  format explain, Fill it the table for  {}?".format(
    #  name)

    # SQL
    message = "Create a query to insert INTO tree (first_name, last_name, family_name, born_date, depth_date, father, mother, children, source_link) VALUES, Where value is data you can find in internet for the person {}".format(
     name)

    content = Bard().get_answer(str(message))['content']
    print(content)
    start_pos = content.find("INSERT")
    end_pos = content.find(";")
    sql_query = content[start_pos:end_pos + 1].strip()

    print(sql_query)


    import sqlite3
##
    conn = sqlite3.connect("tree.db")
##
    c = conn.cursor()
##
    c.execute(sql_query)
##
    conn.commit()
##
    conn.close()
#
#
#
    #print(content)
    #with open('family_tree.json', 'w') as f:
    #    json.dump(content, f, indent=4)
#
    ## Create a Pandas DataFrame from the content
#



if __name__ == "__main__":
    name = input("Enter the name: ")
    get_family_tree(name)