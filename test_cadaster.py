import unittest

import cadastron


class TestParseCadaster(unittest.TestCase):
    """
    Тест функции parse_cadaster(text)
    """
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_parse_cadaster(self):
        text = '66:25:1001001:0023'
        cadaster_no = cadastron.parse_cadaster(text)
        self.assertEqual(cadaster_no, '66:25:1001001:0023')

    def test_parse_cadaster_spaces_delimiter(self):
        text = '66 25 1001001 0023'
        cadaster_no = cadastron.parse_cadaster(text)
        self.assertEqual(cadaster_no, '66:25:1001001:0023')

    def test_parse_cadaster_without_delimiter(self):
        text = '662510010010023'
        cadaster_no = cadastron.parse_cadaster(text)
        self.assertEqual(cadaster_no, '66:25:1001001:0023')
