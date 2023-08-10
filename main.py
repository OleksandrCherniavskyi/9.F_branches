import json
import sqlite3
from bardapi import Bard
from bard_token import token
import os
import pandas as pd

os.environ["_BARD_API_KEY"] = token

def get_family_tree(name):
    """Gets the family tree of the given name."""
    # JSON
    message = "In JSON (full_name, maiden_name, born_date, depth_date, father, mother, childrens, source_link)  format explain. If some information is unknown leave empty(null). For the person {}?".format(name)



    content = Bard().get_answer(str(message))['content']
    print(content)
    start_pos = content.find("{")
    end_pos = content.find("}")
    content_json = content[start_pos:end_pos + 1].strip()

    def main_person():

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

        # Connect to DB

        conn = sqlite3.connect("treeDB.db")
        c = conn.cursor()

        # ADD main person

        query_add_main_person = f"""
      INSERT INTO tree (full_name, maiden_name, born_date, death_date, source_link)
      VALUES (?, ?, ?, ?, ?);
      """
        c.execute(query_add_main_person, (full_name, maiden_name, born_date, death_date, source_link))
        conn.commit()

        # ID main person

        query_ask_id_person = "SELECT id FROM tree WHERE full_name = ?"
        c.execute(query_ask_id_person, (full_name,))
        conn.commit()
        id_main_person = c.fetchone()
        id_main_person = id_main_person[0]

        # ADD father main person

        query_add_father_main_person = f"""
        INSERT INTO tree (full_name) VALUES (?);
        """
        c.execute(query_add_father_main_person, (father,))
        conn.commit()

        # ADD mather main person

        query_add_father_main_person = f"""
          INSERT INTO tree (full_name) VALUES (?);
          """
        c.execute(query_add_father_main_person, (mother,))
        conn.commit()

        # ADD children main person
        for child in children:
            child

            query_add_father_main_person = f"""
              INSERT INTO tree (full_name) VALUES (?);
              """
            c.execute(query_add_father_main_person, (child,))
            conn.commit()

        # Ask BD, id father, mother, children(s)

        c.execute(query_ask_id_person, (father,))
        conn.commit()
        id_father = c.fetchone()
        id_father = id_father[0]

        c.execute(query_ask_id_person, (mother,))
        conn.commit()
        id_mother = c.fetchone()
        id_mother = id_mother[0]

        id_childrens = []
        for child in children:
            child
            c.execute(query_ask_id_person, (child,))
            conn.commit()
            id_child = c.fetchone()
            id_child = id_child[0]
            id_childrens.append(id_child)

        # add relationships for parents

        child_relationship = """
            INSERT INTO relationships (parent_id, child_id)
            VALUES (?, ?);
            """
        c.execute(child_relationship, (id_father, id_main_person))
        c.execute(child_relationship, (id_mother, id_main_person))
        conn.commit()

        # add relationships for children's

        for child_id in id_childrens:
            c.execute(child_relationship, (id_main_person, child_id))
            conn.commit()

    main_person()



if __name__ == "__main__":
    name = input("Enter the name: ")
    get_family_tree(name)