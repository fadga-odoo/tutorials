from odoo.tests.common import TransactionCase
from odoo.exceptions import UserError
from odoo.tests import tagged

'''

----------------------------
--- How CI works in Odoo ---
----------------------------

CI will run the tests after ALL modules are installed, not right after installing the one defining it.
For example: the following tests won't run after `estate` module is installed, but soon after all modules are installed.

'''

@tagged("post_install", "-at_install")
class EstateTestCase(TransactionCase):
    @classmethod
    def setUpClass(cls):
        # Run setUpClass of the parent/base class, which is TransactionCase
        super(EstateTestCase, cls).setUpClass()

        # Initialize dummy data
        cls.properties = cls.env['estate.property'].create([
            {'name': 'property_a', 'expected_price': 19},
            {'name': 'property_b', 'expected_price': 19}
        ])
    
    def test_creation_area(self):
        '''Test that the total_area_is computed like it should.'''
        self.properties.living_area = 30
        self.properties[0].living_area = 15
        self.assertRecordValues(self.properties, [
            {'name': 'property_a', 'total_area': 15, 'expected_price': 19},
            {'name': 'property_b', 'total_area': 30, 'expected_price': 19}
        ])