import unittest
from app import get_message

class TestApp(unittest.TestCase):
    def test_message(self):
        self.assertEqual(get_message(), "Hello from Jenkins CI/CD Pipeline!")

if __name__ == '__main__':
    unittest.main()
