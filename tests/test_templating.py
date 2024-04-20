from unittest import TestCase
from quiz_templating import QuizTemplate


class TestQuizTemplates(TestCase):
    def setUp(self):
        self.tpl = QuizTemplate("testPage.tpl")

    def test_format_ok(self):
        subs = {
            'number': 5,
            'score': 10,
            'length': 20,
            'question': "Where do lonely hearts go?",
            'answers': ["Home","Nowhere","First star to the left","Heaven"],
        }

        htmlpage = self.tpl.format(subs)
        for ans in subs['answers']:
            self.assertIn(ans, htmlpage, "Wrong HTML generated")
        self.assertIn("5 out of 20", htmlpage, "Wrong HTML generated")

