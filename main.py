import json
import sqlite3
from bardapi import Bard
from bard_token import token
import os

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
table_1 = """CREATE TABLE IF NOT EXISTS branch (
    id SERIAL PRIMARY KEY,
    full_name VARCHAR(255),
    born_date DATE,
    death_date DATE,
    source_link VARCHAR(255)
);"""
table_2 = """CREATE TABLE IF NOT EXISTS relationships (
    id SERIAL PRIMARY KEY,
    parent_id INT,
    child_id INT,
    FOREIGN KEY(parent_id) REFERENCES branch(id),
    FOREIGN KEY(child_id) REFERENCES branch(id)
);"""
c.execute(table_1)
c.execute(table_2)



os.environ["_BARD_API_KEY"] = token


# QUERY
query_ask_id_person = "SELECT id FROM branch WHERE full_name = %s;"
query_add_family_main_person = "INSERT INTO branch (full_name) VALUES (%s) RETURNING id;"
child_relationship = "INSERT INTO relationships (parent_id, child_id) VALUES (%s, %s);"



def check_in_db(name):
    try:
        # check person id in DB
        c.execute(query_ask_id_person, (name,))
        #conn.commit()
        search_person_id = c.fetchone()
        search_person_id = search_person_id[0]
    except TypeError:
    #if search_person_id is None:
        # JSON
        message = "In JSON (full_name, born_date, depth_date, father, mother, children, source_link)  " \
                  "format explain. If some information is unknown leave empty(null)." \
                  "Father, mother, children just a full name. For the person {}?".format(name)
        bard_search_engine(message)
    else:
        # check validation data
        query_ask_source_link = "SELECT source_link FROM branch WHERE id = %s;"
        c.execute(query_ask_source_link, (search_person_id,))
        #conn.commit()
        link = c.fetchone()
        link = link[0]

        if link is not None:
            print("Person already in database")
        if link is None:
            update_person_info(search_person_id)


def update_person_info(search_person_id):
    try:
        parent_search_person = """SELECT t.full_name AS parent_name
                                FROM branch AS t
                                WHERE t.id IN (
                                    SELECT parent_id
                                    FROM relationships
                                    WHERE child_id = %s
                                );
                                """
        c.execute(parent_search_person, (search_person_id,))
        #conn.commit()
        parent = c.fetchall()
        parent = parent
        # JSON
        message = (
            "In JSON (full_name, born_date, death_date, father, mother, children, source_link) format explain. "
            "If some information is unknown, leave empty (null)."
            "Father, mother, children just a full name."
            "For the person: {}, parent(s): {}"
                .format(name, parent, "parent" if " and " not in parent else "parents"))
        bard_search_engine(message)
    except IndexError:
        children_search_person = """SELECT t.id, t.full_name AS parent,
                (SELECT ct.full_name
                FROM branch AS ct
                WHERE ct.id = r.child_id) AS children
                FROM branch AS t
                LEFT JOIN relationships AS r ON t.id = r.parent_id
                WHERE t.id = %s;"""

        c.execute(children_search_person, (search_person_id,))
        #conn.commit()
        childrens = c.fetchall()
        child_names = [children[2] for children in childrens]
        # JSON
        message = (
            "In JSON (full_name, born_date, death_date, father, mother, children, source_link) format explain. "
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
    data_dict = json.loads(content_json,  strict=False)
    json_to_sql(data_dict)

def json_to_sql(data_dict):
    try:
        full_name = data_dict["full_name"]
        full_name = full_name.replace(" Jr.", "").replace(" Sr.", "")
        split_full_name = full_name.split()
        if len(split_full_name) > 2:
            first_name = split_full_name[0]
            last_name = split_full_name[-1]
            full_name = f"{first_name} {last_name}"
        else:
            full_name = full_name

        born_date = data_dict["born_date"]

        death_date = data_dict["death_date"]

        father = data_dict["father"]
        if father is None:
            pass
        else:
            father = father.replace(" Jr.", "").replace(" Sr.", "")
            split_father = father.split()
            if len(split_father) > 2:
                first_name = split_father[0]
                last_name = split_father[-1]
                father = f"{first_name} {last_name}"
            else:
                father = father

        mother = data_dict["mother"]
        if mother is None:
            pass
        else:
            mother = mother.replace(" Jr.", "").replace(" Sr.", "")
            split_mother = mother.split()
            if len(mother) > 2:
                first_name = split_mother[0]
                last_name = split_mother[-1]
                mother = f"{first_name} {last_name}"
            else:
                mother = mother

        children = data_dict["children"]
        childrens = []
        if children is None:
            pass
        else:
            for child in children:
                child = child.replace(" Jr.", "").replace(" Sr.", "")
                split_child = child.split()
                if len(child) > 2:
                    first_name = split_child[0]
                    last_name = split_child[-1]
                    child = f"{first_name} {last_name}"
                    childrens.append(child)
                else:
                    child = child
                    childrens.append(child)

        source_link = data_dict["source_link"]

        # ADD main person

        try:
            # check person id in DB
            c.execute(query_ask_id_person, (full_name,))
            #conn.commit()
            search_person_id = c.fetchone()
            search_person_id = search_person_id[0]
            query_update_main_person = """
                UPDATE branch
                SET full_name = %s, born_date = %s, death_date = %s, source_link = %s
                WHERE id = %s;
            """

            c.execute(query_update_main_person,
                      (full_name, born_date, death_date, source_link, search_person_id))
            #conn.commit()
        except TypeError:
            query_add_main_person = """
                INSERT INTO branch (full_name, born_date, death_date, source_link)
                VALUES (%s, %s, %s, %s)
                RETURNING id;
            """

            c.execute(query_add_main_person, (full_name, born_date, death_date, source_link))
            #conn.commit()

        # ID main person

        c.execute(query_ask_id_person, (full_name,))
        #conn.commit()
        id_main_person = c.fetchone()
        id_main_person = id_main_person[0]

        # ADD father main person

        if father is None:
            pass
        else:
            try:
                # check person id in DB
                c.execute(query_ask_id_person, (father,))
                #conn.commit()
                search_person_id = c.fetchone()
                search_person_id = search_person_id[0]
            except TypeError:
                c.execute(query_add_family_main_person, (father,))
                #conn.commit()
                c.execute(query_ask_id_person, (father,))
                #conn.commit()
                id_father = c.fetchone()
                id_father = id_father[0]
                c.execute(child_relationship, (id_father, id_main_person))
                #conn.commit()

        if mother is None:
            pass
        else:
            try:
                # check person id in DB
                c.execute(query_ask_id_person, (mother,))
                #conn.commit()
                search_person_id = c.fetchone()
                search_person_id = search_person_id[0]
            except TypeError:
                c.execute(query_add_family_main_person, (mother,))
                #conn.commit()
                c.execute(query_ask_id_person, (mother,))
                #conn.commit()
                id_mother = c.fetchone()
                id_mother = id_mother[0]
                c.execute(child_relationship, (id_mother, id_main_person))
                #conn.commit()


        # ADD children main person
        # Loop through each child and add them to the main person's family
        if children is None:
            pass
        else:
            for child in childrens:
                c.execute(query_ask_id_person, (child,))
                search_person_id = c.fetchone()

                if search_person_id:
                    # Person already exists in the DB
                    search_person_id = search_person_id[0]
                else:
                    # Add the child to the branch table
                    c.execute(query_add_family_main_person, (child,))
                    c.execute(query_ask_id_person, (child,))
                    search_person_id = c.fetchone()
                    search_person_id = search_person_id[0]

                # Create the relationship between the main person and the child
                c.execute(child_relationship, (id_main_person, search_person_id))
    finally:
        c.close()


if __name__ == "__main__":
    name = input("Enter the name: ")
    name = name.title()
    check_in_db(name)
