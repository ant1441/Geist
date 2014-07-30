import unittest
from geist.repo import DirectoryRepo


class TestDirectoryRepo(unittest.TestCase):
    def setUp(self):
        self.repo = DirectoryRepo('.')

    def test_valid_name(self):
        self.assertTrue(self.repo._valid_name('valid'))

    def test_invalid_name(self):
        self.assertFalse(self.repo._valid_name('1valid'))

    def test_keyword(self):
        self.assertFalse(self.repo._valid_name('pass'))


directory_repo_suite = unittest.TestLoader().loadTestsFromTestCase(
    TestDirectoryRepo)
all_tests = unittest.TestSuite([directory_repo_suite])
if __name__ == "__main__":
    runner = unittest.TextTestRunner(verbosity=1)
    runner.run(all_tests)
