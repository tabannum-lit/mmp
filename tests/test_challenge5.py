from unittest import TestCase
from quiz import Quiz, QuizItem

_test_data = [{"question": "What is considered the rarist form of color blindness?", "correct_answer": "Blue",
               "incorrect_answers": ["Red", "Green", "Purple"]},
              {"question": "The humerus, paired radius, and ulna come together to form what joint?",
               "correct_answer": "Elbow", "incorrect_answers": ["Knee", "Sholder", "Ankle"]},
              {"question": "All of the following human genetic haplogroup names are shared between Y-chromosome and mitochondrial DNA haplogroups EXCEPT:",
               "correct_answer": "Haplogroup U", "incorrect_answers": ["Haplogroup L", "Haplogroup T", "Haplogroup J"]},
              {"question": "71% of the Earth&#039;s surface is made up of", "correct_answer": "Water",
               "incorrect_answers": ["Deserts", "Continents", "Forests"]},
              {"question": "Muscle fiber is constructed of bundles small long organelles called what?",
               "correct_answer": "Myofibrils", "incorrect_answers": ["Epimysium", "Myofiaments", "Myocardium"]},
              {"question": "What are human nails made of?", "correct_answer": "Keratin",
               "incorrect_answers": ["Bone", "Chitin", "Calcium"]},
              {"question": "How long is a light-year?", "correct_answer": "9.461 Trillion Kilometres",
               "incorrect_answers": ["1 AU", "105.40 Earth-years", "501.2 Million Miles"]},
              {"question": "On which mission did the Space Shuttle Columbia break up upon re-entry?",
               "correct_answer": "STS-107", "incorrect_answers": ["STS-51-L", "STS-61-C", "STS-109"]},
              {"question": "In human biology, a circadium rhythm relates to a period of roughly how many hours?",
               "correct_answer": "24", "incorrect_answers": ["8", "16", "32"]},
              {"question": "What is the official name of the star located closest to the North Celestial Pole?",
               "correct_answer": "Polaris", "incorrect_answers": ["Eridanus", "Gamma Cephei", "Iota Cephei"]}]

class TestQuizPersist(TestCase):
    def setUp(self):
        self.q = Quiz("temp.quiz")
        for item_data in _test_data:
            self.q.add_item(QuizItem(item_data["question"], item_data["correct_answer"], item_data["incorrect_answers"]))

    def test_save_load_destroy(self):
        self.q.save()
        newq = Quiz("temp.quiz")
        newq.load()
        for (item_data, quiz_item) in zip(_test_data,self.q):
            self.assertEqual(item_data["question"], quiz_item.question)
            self.assertEqual(item_data["correct_answer"], quiz_item.correct_answer)
            self.assertListEqual(item_data["incorrect_answers"], quiz_item.incorrect_answers)
        newq.destroy()
        testq = Quiz("temp.quiz")
        self.assertRaises(IOError, testq.load )  # Loading a destroyed quiz should raise an error"

    def test_save_destroy(self):
        self.q.save()
        self.assertRaises(IOError, self.q.save ) # "Saving an exiting quiz should raise an error"
        self.q.destroy()
        testq = Quiz("temp.quiz")
        self.assertRaises(IOError, testq.load )  # Loading a destroyed quiz should raise an error"

class TestQuizOps(TestCase):
    def setUp(self):
        self.quiz = Quiz("testquiz");

    def test_quizAddItem(self):
        self.assertEqual(0, len(self.quiz), "Empty quiz length should be zero")
        for item_data in  _test_data:
            qi = QuizItem(item_data["question"], item_data["correct_answer"], item_data["incorrect_answers"])
            icount = len(self.quiz)
            self.quiz.add_item(qi)
            self.assertEqual(icount+1, len(self.quiz), "Quiz length should increase on add")

    def test_quizAdd(self):
        self.assertEqual(0, len(self.quiz), "Empty quiz length should be zero")
        for item_data in  _test_data:
            icount = len(self.quiz)
            self.quiz.add(item_data["question"], item_data["correct_answer"], item_data["incorrect_answers"])
            self.assertEqual(icount+1, len(self.quiz), "Quiz length should increase on add")

    def test_quizAdd_Iter(self):
        for item_data in _test_data:
            self.quiz.add(item_data["question"], item_data["correct_answer"], item_data["incorrect_answers"])
        for (item_data, quiz_item) in zip(_test_data,self.quiz):
            self.assertEqual(item_data["question"], quiz_item.question)
            self.assertEqual(item_data["correct_answer"], quiz_item.correct_answer)
            self.assertListEqual(item_data["incorrect_answers"], quiz_item.incorrect_answers)

    def test_quizAdd_Match_Iter(self):
        for item_data in _test_data:
            self.quiz.add(item_data["question"], item_data["correct_answer"], item_data["incorrect_answers"])
        for (item_data, quiz_item) in zip(_test_data, self.quiz):
            item = self.quiz.match(item_data['question'])
            self.assertIsNotNone(item, "Match did not find added item")
            self.assertEqual(quiz_item, item, "Match did not find added item")

    def test_quizAdd_Match_Remove(self):
        for item_data in _test_data:
            self.quiz.add(item_data["question"], item_data["correct_answer"], item_data["incorrect_answers"])
        for (item_data, quiz_item) in zip(_test_data, list(self.quiz)):
            item = self.quiz.match(item_data['question'])
            self.assertIsNotNone(item, "Match did not find added item")
            self.assertEqual(quiz_item, item, "Match did not find added item")
            old_len = len(self.quiz)
            self.quiz.remove(item)
            self.assertEqual(len(self.quiz), old_len-1, "Remove should shorten quiz")
            self.assertIsNone(self.quiz.match(item_data['question']), "Item not removed")


class TestQuizItemOps(TestCase):

    def test_nest_Iter(self):
        for item_data in _test_data:
            qi = QuizItem(item_data["question"], item_data["correct_answer"], item_data["incorrect_answers"])

            for ans1 in qi:
                found = False
                for ans2 in qi:
                    if(ans1 == ans2):
                        found = True;
                        break;
                self.assertTrue(found, "Nested iteration does not work")



