import unittest

import cadastron


class TestGetObjId(unittest.TestCase):

    def test_get_obj_id(self):
        cadaster = '66:25:1100101:45'
        obj_id = cadastron.get_obj_id(cadaster)
        self.assertEqual(obj_id, '66:25:1100101:45')

    def test_get_obj_id_lead_zero(self):
        cadaster = '66:01:0100101:045'
        obj_id = cadastron.get_obj_id(cadaster)
        self.assertEqual(obj_id, '66:1:100101:45')
