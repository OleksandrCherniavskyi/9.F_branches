#import sqlite3
#
#conn = sqlite3.connect("tree.db")
#
#c = conn.cursor()
#
#c.execute("""CREATE TABLE tree (
#    id INTEGER PRIMARY KEY,
#    first_name TEXT,
#    last_name TEXT,
#    family_name TEXT,
#    born_date DATE,
#    depth_date INTEGER,
#    father TEXT,
#    mother TEXT,
#    children TEXT,
#    source_link TEXT
#)""")
#
#conn.commit()
#
#conn.close()

#import sqlite3
#
#conn = sqlite3.connect("tree.db")
#
#c = conn.cursor()
#
#c.execute(
#INSERT INTO tree (first_name, last_name, family_name, born_date, depth_date, father, mother, children, source_link)
#VALUES ('George', 'H.W.', 'Bush', '1924-06-12', '0', 'Prescott Bush', 'Dorothy Walker Bush',
#        'Neil Bush', 'George W. Bush', 'https://en.wikipedia.org/wiki/George_H._W._Bush');
#```)
#
#conn.commit()
#
#conn.close()

content = """

```sql
INSERT INTO tree (first_name, last_name, family_name, born_date, depth_date, father, mother, children, source_link)
VALUES ('Tim', 'Kuk', 'Kuk', '2023-08-01', 0, NULL, NULL, NULL, NULL);
```

This query will insert a new row into the `tree` table with the following values:
"""


start_pos = content.find("INSERT")

end_pos = content.find(";")
sql_query = content[start_pos:end_pos + 1].strip()
print(sql_query)