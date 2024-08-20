import unittest

from parser import parse
from scaner import scan
from tree import display


class TestParseSchema(unittest.TestCase):

    def test_create_schema_simple(self):
        query = "CREATE SCHEMA my_schema;"
        self._test_query(query)

    def test_create_schema_with_authorization(self):
        query = "CREATE SCHEMA AUTHORIZATION user1;"
        self._test_query(query)

    def test_create_schema_with_name_and_authorization(self):
        query = "CREATE SCHEMA my_schema AUTHORIZATION user1;"
        self._test_query(query)

    def test_create_schema_with_charset(self):
        query = "CREATE SCHEMA my_schema DEFAULT CHARACTER SET utf8mb4;"
        self._test_query(query)

    def test_create_schema_with_path(self):
        query = "CREATE SCHEMA my_schema PATH '/usr/local/share';"
        self._test_query(query)

    def test_create_schema_with_charset_and_path(self):
        query = "CREATE SCHEMA my_schema DEFAULT CHARACTER SET utf8mb4 PATH '/usr/local/share';"
        self._test_query(query)

    def test_create_schema_with_path_and_charset(self):
        query = "CREATE SCHEMA my_schema PATH '/usr/local/share' DEFAULT CHARACTER SET utf8mb4;"
        self._test_query(query)

    def test_create_schema_with_table_definition(self):
        query = "CREATE SCHEMA my_schema; CREATE TABLE my_schema.my_table (id INT PRIMARY KEY, name VARCHAR(100));"
        self._test_query(query)

    def test_create_schema_with_view_definition(self):
        query = "CREATE SCHEMA my_schema; CREATE VIEW my_schema.my_view AS SELECT id, name FROM my_schema.my_table;"
        self._test_query(query)

    def test_create_schema_with_domain_definition(self):
        query = "CREATE SCHEMA my_schema; CREATE DOMAIN my_schema.my_domain AS VARCHAR(255) CHECK (VALUE <> '');"
        self._test_query(query)

    def test_create_schema_with_charset_definition(self):
        query = "CREATE SCHEMA my_schema; CREATE CHARACTER SET my_schema.my_charset AS utf8mb4;"
        self._test_query(query)

    def test_create_schema_with_collation_definition(self):
        query = "CREATE SCHEMA my_schema; CREATE COLLATION my_schema.my_collation FOR utf8mb4 FROM 'utf8mb4_bin';"
        self._test_query(query)

    def test_create_schema_with_trigger_definition(self):
        query = """CREATE SCHEMA my_schema;
                   CREATE TABLE my_schema.my_table (id INT PRIMARY KEY, name VARCHAR(100));
                   CREATE TRIGGER my_schema.my_trigger BEFORE INSERT ON my_schema.my_table
                   FOR EACH ROW SET NEW.name = UPPER(NEW.name);"""
        self._test_query(query)

    def test_create_schema_with_sequence_definition(self):
        query = "CREATE SCHEMA my_schema; CREATE SEQUENCE my_schema.my_sequence START WITH 1 INCREMENT BY 1;"
        self._test_query(query)

    def test_create_schema_with_grant_statement(self):
        query = "CREATE SCHEMA my_schema; GRANT SELECT ON my_schema.my_table TO user1;"
        self._test_query(query)

    def test_create_schema_with_role_definition(self):
        query = "CREATE SCHEMA my_schema; CREATE ROLE my_schema.my_role;"
        self._test_query(query)

    def _test_query(self, query):
        tokens = scan(query)
        ast_head = parse(tokens)
        display(ast_head)
        self.assertTrue(True)


if __name__ == '__main__':
    unittest.main()
