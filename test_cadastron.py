import unittest
import cadastron


class TestParseCadaster(unittest.TestCase):
    """
    Тест функции parse_cadaster(text)
    """
    def setUp(self):
        self.inp_strings = ['66:25:1001001:0023',
                            '66 25 1001001 0023',
                            '662510010010023']

    def tearDown(self):
        pass

    def test_parse_cadaster(self):
        for inp_str in self.inp_strings:
            self.assertEqual(cadastron.parse_cadaster(inp_str), '66:25:1001001:0023')


class TestParseCoords(unittest.TestCase):
    """
    Тест функции parse_coords(text)
    """
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_parse_coords_whitespace_dot(self):
        coords_txt = '55.455555 61.25847'
        coords = cadastron.parse_coords(coords_txt)
        self.assertTupleEqual(coords, ('55.455555', '61.25847'))

    def test_parse_coords_whitespace_comma(self):
        coords_txt = '55,455555 61,25847'
        coords = cadastron.parse_coords(coords_txt)
        self.assertTupleEqual(coords, ('55.455555', '61.25847'))

    def test_parse_coords_yandex(self):
        coords_txt = '55.455555, 61.25847'
        coords = cadastron.parse_coords(coords_txt)
        self.assertTupleEqual(coords, ('55.455555', '61.25847'))


class TestGetObjId(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_get_obj_id(self):
        cadaster = '66:25:1100101:45'
        obj_id = cadastron.get_obj_id(cadaster)
        self.assertEqual(obj_id, '66:25:1100101:45')

    def test_get_obj_id_lead_zero(self):
        cadaster = '66:01:0100101:045'
        obj_id = cadastron.get_obj_id(cadaster)
        self.assertEqual(obj_id, '66:1:100101:45')


if __name__ == '__main__':
    unittest.main()
