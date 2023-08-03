import json

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



