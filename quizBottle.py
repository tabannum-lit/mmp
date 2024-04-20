# Python 3 server example
import random

from bottle import Bottle, request
from quiz_templating import QuizTemplate

import quiz
import random

host = "localhost"
# host = '0.0.0.0'
serverPort = 8080

html_template = """
<!DOCTYPE HTML>
<html>

<head>
    <meta name="author" content="Ed Brown">
    <title>Quiz from 2005</title>
</head>

<body>
    <h1>Magic Online Quiz</h1>
 <div>
    <p>Question no {number} out of {length}</p>
    <p>Your Score: {score} out of {length}</p>
    <p><bold>{question}</bold>
    <form action="/answer" method="POST">
        <p>
        <button type="submit" name="but" value="0" id="0" {hidden[0]}>{answers[0]}</button>
        <button type="submit" name="but" value="1" id="1" {hidden[1]}>{answers[1]}</button>
        <button type="submit" name="but" value="2" id="2" {hidden[2]}>{answers[2]}</button>
        <button type="submit" name="but" value="3" id="3" {hidden[3]}>{answers[3]}</button>
        <button type="submit" name="but" value="4" id="4" {hidden[4]}>{answers[4]}</button>
        <button type="submit" name="but" value="5" id="5" {hidden[5]}>{answers[5]}</button>
        <button type="submit" name="but" value="6" id="6" {hidden[6]}>{answers[6]}</button>
        <button type="submit" name="but" value="7" id="7" {hidden[7]}>{answers[7]}</button>
        <button type="submit" name="but" value="8" id="8" {hidden[8]}>{answers[8]}</button>
        <button type="submit" name="but" value="9" id="9" {hidden[9]}>{answers[9]}</button>
        </p>
    </form>
 </div>
</body>
</html>
"""


class QuizBottle(Bottle):
    one_quiz = quiz.Quiz("data/quiz2.txt")
    one_quiz.load()
    quiz_iterator = iter(one_quiz)
    quiz_item = None
    quiz_item_answers = None
    quiz_score = 0
    quiz_count = 0

    normal_template = QuizTemplate("normalPage.tpl")
    last_template = QuizTemplate("lastPage.tpl")


    @classmethod
    def quiz_name(cls):
        return cls.one_quiz.name

    def __init__(self):
        super(QuizBottle, self).__init__()
        self.route("/", callback=self.quizzing)
        self.route("/answer", callback=self.answering, method="POST")
        self.route("/name", callback=self.quiz_name_handler)

    def quiz_name_handler(self):
        return self.quiz_name()

    @classmethod
    def nextPage(cls):
        cls.quiz_item = next(cls.quiz_iterator)
        cls.quiz_count += 1
        cls.quiz_item_answers = list(cls.quiz_item)
        random.shuffle(cls.quiz_item_answers)

        template_substitutions = {
            'number': cls.quiz_count,
            'score': cls.quiz_score,
            'length': len(cls.one_quiz),
            'question': cls.quiz_item.question,
            'answers': cls.quiz_item_answers,
        }

        return cls.normal_template.format(template_substitutions)

    @classmethod
    def lastPage(cls):
        template_substitutions = {
            'score': cls.quiz_score,
            'length': len(cls.one_quiz),
        }
        return cls.last_template.format(template_substitutions)

    @classmethod
    def increment_score(cls):
        cls.quiz_score += 1

    def quizzing(self):
        return self.nextPage()

    def answering(self):

        # is answer correct? Refactor this to app logic!
        quiz_item_answers = self.quiz_item
        if quiz_item_answers.correct_answer == quiz_item_answers.answers[int(request.forms['but'])]:
            self.increment_score();
        try:
            response = self.nextPage()
        except StopIteration:
            response = self.lastPage()
        return response


if __name__ == "__main__":
    qs = QuizBottle()
    qs.run(host=host, port=serverPort, debug=True)
