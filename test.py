import json
import sqlite3

content_json = '''{
  "full_name": "Donald John Trump",
  "maiden_name": "Unknown",
  "born_date": "1946-06-14",
  "death_date": null,
  "father": "Fred Trump",
  "mother": "Mary Anne MacLeod Trump",
  "children": ["Ivanka Trump", "Donald Trump Jr.", "Eric Trump", "Tiffany Trump", "Barron Trump"],
  "source_link": "https://en.wikipedia.org/wiki/Donald_Trump"
}'''
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

  ## ADD main person
  #
  #query_add_main_person = f"""
  #INSERT INTO tree (full_name, maiden_name, born_date, death_date, source_link)
  #VALUES (?, ?, ?, ?, ?);
  #"""
  #c.execute(query_add_main_person, (full_name, maiden_name, born_date, death_date, source_link))
  #conn.commit()

  # ID main person

  query_ask_id_person = "SELECT id FROM tree WHERE full_name = ?"
  c.execute(query_ask_id_person, (full_name,))
  conn.commit()
  id_main_person = c.fetchone()
  id_main_person = id_main_person[0]

  ## ADD father main person
  #
  #query_add_father_main_person = f"""
  #  INSERT INTO tree (full_name, children) VALUES (?, ?);
  #  """
  #c.execute(query_add_father_main_person, (father, id_main_person))
  #conn.commit()
  #
  ## ADD mather main person
  #
  #query_add_father_main_person = f"""
  #    INSERT INTO tree (full_name, children) VALUES (?, ?);
  #    """
  #c.execute(query_add_father_main_person, (mother, id_main_person))
  #conn.commit()

  # ADD children main person
  #for child in children:
  #  child
#
  #  query_add_father_main_person = f"""
  #        INSERT INTO tree (full_name, father) VALUES (?, ?);
  #        """
  #  c.execute(query_add_father_main_person, (child, id_main_person))
  #  conn.commit()

  # Ask BD, id father, mother, children(s)

  c.execute(query_ask_id_person, (father,))
  conn.commit()
  id_father = c.fetchone()
  id_father = id_father[0]


  c.execute(query_ask_id_person, (mother,))
  conn.commit()
  id_mother = c.fetchone()
  id_mother= id_mother[0]


  id_childrens = []
  for child in children:
    child
    c.execute(query_ask_id_person, (child,))
    conn.commit()
    id_child = c.fetchone()
    id_child = id_child[0]
    id_childrens.append(id_child)




  ## Update  main person

  query_update_main_person = """
  UPDATE tree
  SET father = ?, mother = ?
  WHERE id = ?;
  """
  c.execute(query_update_main_person, (id_father, id_mother,  id_main_person))
  conn.commit()

  for child_id in id_childrens:
    query_add_relationship = """
      INSERT INTO relationships (parent_id, child_id)
      VALUES (?, ?);
      """
    c.execute(query_add_relationship, (id_main_person, child_id))
    conn.commit()

  # work but not good

  #query_update_main_person_children = "UPDATE tree SET children = ?, father = ?, mother = ? WHERE id = ?;"
  #c.execute(query_update_main_person_children, (','.join(map(str, id_childrens)), id_father, id_mother, id_main_person))
  #conn.commit()
  #conn.close()

main_person()


"""SELECT t.id, t.full_name,
       (SELECT ct.full_name
        FROM tree AS ct
        WHERE ct.id = r.child_id) AS children
FROM tree AS t
LEFT JOIN relationships AS r ON t.id = r.parent_id"""