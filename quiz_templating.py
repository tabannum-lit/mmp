import os
class QuizTemplate:
    """
    Manages HTML templates in a template directory.

    Attributes:
        filename (str): filename of the template

    Methods:
        format(substitute_dict) - substitute the placeholders in the template with the values in the dictionary

    """
    def __init__(self, name):
        self.filename = os.path.join("templates", name)
        fd = open(self.filename)
        self.template_string=fd.read()
        fd.close()

    def format(self, substitutions):
        if "answers" in substitutions:
            answer_count = len(substitutions['answers'])
            substitutions['answers'].extend(['Not Available'] * (10 - answer_count))
            substitutions['hidden'] = [""] * answer_count
            substitutions['hidden'].extend(["hidden"] * (10 - answer_count))
        return self.template_string.format(**substitutions)


