# Python 3 server example

from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs

import quiz
import random
from quiz_templating import QuizTemplate

hostName = "localhost"
serverPort = 8080


class QuizRequestHandler(BaseHTTPRequestHandler):

    one_quiz = quiz.Quiz("data/quiz2.txt")
    one_quiz.load()
    quiz_iterator = iter(one_quiz)
    quiz_item = None
    quiz_item_answers = None
    quiz_score = 0
    quiz_count = 0

    normal_template = QuizTemplate("normalPage.tpl")
    last_template = QuizTemplate("lastPage.tpl")


    def do_GET(self):
        if self.path == "/name":
            self.send_response(200)
            self.send_header("Content-type", "text/plain")
            self.end_headers()
            self.wfile.write(bytes(self.one_quiz.name, "utf-8"))
        elif self.path in ["/", "/start"]:
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(bytes(self.nextPage(), "utf-8"))

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

    def do_GET(self):
        if self.path in ["/", "/start"]:
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(bytes(self.nextPage(), "utf-8"))

    def do_POST(self):


        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()

        if self.path == "/answer":
            data_string = self.rfile.read(int(self.headers['Content-Length'])).decode('utf-8')
            data = parse_qs(data_string, keep_blank_values=True)
            user_selection = self.quiz_item_answers[int(data['but'][0])]
            if user_selection == self.quiz_item.correct_answer:
                self.increment_score()
            try:
                self.wfile.write(bytes(self.nextPage(), "utf-8"))
            except StopIteration:
                self.wfile.write(bytes(self.lastPage(), "utf-8"))

if __name__ == "__main__":
    webServer = HTTPServer((hostName, serverPort), QuizRequestHandler)
    print("Server started http://%s:%s" % (hostName, serverPort))

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")
