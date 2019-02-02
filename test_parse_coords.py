import unittest
import cadastron


class TestParseCoords(unittest.TestCase):
    """
    Тест функции parse_coords(text)
    """

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


if __name__ == '__main__':
    unittest.main()
