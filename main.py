from src.utils import create_database, create_table, insert_tables


name_db = "test_course"
create_database(name_db)
create_table(name_db)
insert_tables(name_db)
