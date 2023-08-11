import json
import sqlite3
from bardapi import Bard
from bard_token import token
import os


os.environ["_BARD_API_KEY"] = token

# Connect to DB
conn = sqlite3.connect("treeDB.db")
c = conn.cursor()


# QUERY
query_ask_id_person = "SELECT id FROM tree WHERE full_name = ?"
query_add_family_main_person = f"""INSERT INTO tree (full_name) VALUES (?);"""
child_relationship = """INSERT INTO relationships (parent_id, child_id) VALUES (?, ?);"""


def check_in_db(name):
    try:
        # check person id in DB
        c.execute(query_ask_id_person, (name,))
        conn.commit()
        search_person_id = c.fetchone()
        search_person_id = search_person_id[0]
    except TypeError:
    #if search_person_id is None:
        # JSON
        message = "In JSON (full_name, maiden_name, born_date, depth_date, father, mother, childrens, source_link)  " \
                  "format explain. If some information is unknown leave empty(null)." \
                  "Father, mother, children just a full name. For the person {}?".format(name)
        bard_search_engine(message)
    else:
        # check validation data
        query_ask_source_link = "SELECT source_link FROM tree WHERE id = ?"
        c.execute(query_ask_source_link, (search_person_id,))
        conn.commit()
        link = c.fetchone()
        link = link[0]

        if link is not None:
            print("Person already in database")
        if link is None:
            update_person_info(search_person_id)


def update_person_info(search_person_id):
    try:
        parent_search_person = """SELECT t.full_name AS parent_name
                        FROM tree AS t
                        WHERE t.id IN (
                            SELECT parent_id
                            FROM relationships
                            WHERE child_id = ?
                        );
                        """
        c.execute(parent_search_person, (search_person_id,))
        conn.commit()
        parent = c.fetchall()
        parent = parent
        # JSON
        message = (
            "In JSON (full_name, maiden_name, born_date, death_date, father, mother, childrens, source_link) format explain. "
            "If some information is unknown, leave empty (null)."
            "Father, mother, children just a full name."
            "For the person: {}, parent(s): {}"
                .format(name, parent, "parent" if " and " not in parent else "parents"))
        bard_search_engine(message)
    except IndexError:
        children_search_person = """SELECT t.id, t.full_name AS parent,
        (SELECT ct.full_name
        FROM tree AS ct
        WHERE ct.id = r.child_id) AS children
        FROM tree AS t
        LEFT JOIN relationships AS r ON t.id = r.parent_id
        WHERE t.id = ?; """
        c.execute(children_search_person, (search_person_id,))
        conn.commit()
        childrens = c.fetchall()
        child_names = [children[2] for children in childrens]
        # JSON
        message = (
            "In JSON (full_name, maiden_name, born_date, death_date, father, mother, childrens, source_link) format explain. "
            "If some information is unknown, leave empty (null). "
            "Father, mother, children just a full name."
            "For the person: {} is a parent for: {}"
                .format(name, child_names, "parent" if " and " not in child_names else "parents")
        )

        bard_search_engine(message)


def bard_search_engine(message):
    content = Bard().get_answer(str(message))['content']
    print(content)
    start_pos = content.find("{")
    end_pos = content.find("}")
    content_json = content[start_pos:end_pos + 1].strip()
    data_dict = json.loads(content_json)
    json_to_sql(data_dict)

def json_to_sql(data_dict):
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

    # ADD main person

    try:
        # check person id in DB
        c.execute(query_ask_id_person, (full_name,))
        conn.commit()
        search_person_id = c.fetchone()
        search_person_id = search_person_id[0]
        query_update_main_person = """
            UPDATE tree
            SET full_name = ?, maiden_name = ?, born_date = ?, death_date = ?, source_link = ?
            WHERE id = ?;
        """
        c.execute(query_update_main_person,
                  (full_name, maiden_name, born_date, death_date, source_link, search_person_id))
        conn.commit()
    except TypeError:
        query_add_main_person = f"""
                INSERT INTO tree (full_name, maiden_name, born_date, death_date, source_link)
                VALUES (?, ?, ?, ?, ?);
                """
        c.execute(query_add_main_person, (full_name, maiden_name, born_date, death_date, source_link))
        conn.commit()

    # ID main person

    c.execute(query_ask_id_person, (full_name,))
    conn.commit()
    id_main_person = c.fetchone()
    id_main_person = id_main_person[0]

    # ADD father main person

    try:
        # check person id in DB
        c.execute(query_ask_id_person, (father,))
        conn.commit()
        search_person_id = c.fetchone()
        search_person_id = search_person_id[0]
    except TypeError:
        c.execute(query_add_family_main_person, (father,))
        conn.commit()
        c.execute(query_ask_id_person, (father,))
        conn.commit()
        id_father = c.fetchone()
        id_father = id_father[0]
        c.execute(child_relationship, (id_father, id_main_person))
        conn.commit()

    # ADD mother main person

    try:
        # check person id in DB
        c.execute(query_ask_id_person, (mother,))
        conn.commit()
        search_person_id = c.fetchone()
        search_person_id = search_person_id[0]
    except TypeError:
        c.execute(query_add_family_main_person, (mother,))
        conn.commit()
        c.execute(query_ask_id_person, (mother,))
        conn.commit()
        id_mother = c.fetchone()
        id_mother = id_mother[0]
        c.execute(child_relationship, (id_mother, id_main_person))
        conn.commit()


    # ADD children main person
    # Loop through each child and add them to the main person's family
    for child in children:
        c.execute(query_ask_id_person, (child,))
        search_person_id = c.fetchone()

        if search_person_id:
            # Person already exists in the DB
            search_person_id = search_person_id[0]
        else:
            # Add the child to the tree table
            c.execute(query_add_family_main_person, (child,))
            conn.commit()
            search_person_id = c.lastrowid  # Get the last inserted ID

        # Create the relationship between the main person and the child
        c.execute(child_relationship, (id_main_person, search_person_id))
        conn.commit()


if __name__ == "__main__":
    name = input("Enter the name: ")
    check_in_db(name)
