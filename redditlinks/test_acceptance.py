from selenium import webdriver
import unittest


class AcceptanceTest(unittest.TestCase):
    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    def test_example_email(self):
        self.browser.get('http://localhost:8001/example-mail/')
        self.assertEquals(u'Example Reddit.cool Email', self.browser.title)

if __name__ == '__main__':
    unittest.main(warnings='ignore')
