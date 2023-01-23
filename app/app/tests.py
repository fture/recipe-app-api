"""
sample tests
"""

from django.test import SimpleTestCase

from . import calc


class CalaTest(SimpleTestCase) :
    """Test the calc module"""

    def test_add_numbers(self):
        """test adding number"""
        res = calc.add(5, 6)

        self.assertEqual(res, 11)
    
    def test_substract_numbers(self):
        
        res = calc.substract(6,5)

        self.assertEqual(res,1)