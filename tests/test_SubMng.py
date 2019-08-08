import unittest

from TMLib import SubMng as Sub
from TMLib import Definitions as TMdef

class TMReWrapper(unittest.TestCase):
    
    def test_add_transformation_protocol(self):
        Sub.subsribed_functions = {}
        entry = {
            Sub.PROCESSING : (lambda x, y : 0)
            , Sub.PREPROCESSING : (lambda x, y : 1)
            , Sub.VALIDATION : (lambda x, y : 2)
        }

        Sub.subscribe_protocol_transformation({'test' : entry})

        self.assertTrue(len(Sub.subsribed_functions.keys()) == 1)
        self.assertTrue(list(Sub.subsribed_functions.values())[0] is entry)
        self.assertTrue(entry[Sub.PROCESSING](None, None) == 0 )
        self.assertTrue(entry[Sub.PREPROCESSING](None, None) == 1 )
        self.assertTrue(entry[Sub.VALIDATION](None, None) == 2 )


