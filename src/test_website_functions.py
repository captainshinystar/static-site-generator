from website_functions import extract_title
import unittest

class Test_website_functions(unittest.TestCase):
    def test_extract_title(self):
        md = """
# Pokemon is the best

pokemon is the best game series ever!
here is why:
-it is fun
-it is awesome
"""
        title = extract_title(md)
        self.assertEqual(title, "Pokemon is the best")
    
    def test_no_title(self):
        md = """
Pokemon is the best
"""
        
        with self.assertRaises(Exception) as context:
            title = extract_title(md)
        self.assertEqual(str(context.exception), "No title found")

    def test_extract_title_with_whitespace(self):
        md = "# Title with   extra   spaces   "
        title = extract_title(md)
        self.assertEqual(title, "Title with   extra   spaces")

    def test_extract_title_multiple_headers(self):
        md = "# First Title\n## Second Title\n# Another First Title"
        title = extract_title(md)
        self.assertEqual(title, "First Title")

    if __name__ == "__main__":
        unittest.main()