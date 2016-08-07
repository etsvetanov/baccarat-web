from selenium import webdriver
import unittest


class NewVisitorTest(unittest.TestCase):
    def setUp(self):
        self.browser = webdriver.Chrome()

    def tearDown(self):
        self.browser.quit()

    def test_can_open_page(self):
        self.browser.get('http://localhost:8000')

        self.assertIn('Baccarat', self.browser.title)

if __name__ == '__main__':
    unittest.main()
