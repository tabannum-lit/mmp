"""
Multiple choice quiz implementation including persistent storage solution.

Classes:
    Quiz - the quiz object
    QuizItem - an individual Quiz element/question with possible answers.
"""

import os

import persist_ptext as qpersist


class Quiz:
    """Quiz consisting of quiz items and related methods

    Persistent store methods should be under the SRP principle.

    Attributes:
        name (str): storage name and ID of the Quiz
    """

    def __init__(self, name):
        self.name = name
        self._items = []

    def load(self):
        """Load a quiz from persistent store

        THIS IS A STUB

        Returns:
            a new Quiz object with items of a previously stored quiz

        Raises:
            Standard IO Errors

        """
        return qpersist.load(self)  # delegating this call to persistence module

    def save(self):
        """Save quiz to persistent store its current name

        Args:

        Raises:
            Standard IO Errors

        """
        qpersist.store(self)  # delegate the call to persist module

    def __len__(self):
        return len(self._items)

    def __iter__(self):
        return iter(self._items)

    def add_item(self, new_item):
        """Add a quiz item to the quiz

        Args:
            new_item: item to be added to the quiz

        Returns:

        Raises:
            TypeError is parameter is not a QuizItem

        """

        if not isinstance(new_item, QuizItem):
            raise TypeError("parameter to Quiz.add must be QuizItem")
        self._items.append(new_item)

    def add(self, question, correct_answer, incorrect_answers):
        """Add a quiz item to the quiz

            Args:
                 question (str): The multiple choice question
                 correct_answer (str): The correct answer
                 incorrect_answers (list of str): List of incorrect answers
            Returns:
                The added QuizItem or None
            Raises:
                TypeError is parameter is not a QuizItem

            THIS IS A STUB IMPLEMENTATION
        else:   """
        new_item = QuizItem(question, correct_answer, incorrect_answers)
        if isinstance(new_item, QuizItem):

            self.add_item (new_item)
            return new_item

    def match(self, question):
        """Return the matching quiz item

        Args:
            question: question to match

        Returns:
            The quiz item or None if the item is not found
        """
        # Check for exact match first
        for item in self:
            if item.question.strip() == question.strip():
                return item

        # If exact match not found, check for matching with leading blanks
        for item in self:
            if item.question.strip().startswith(question.strip()):
                return item

        # If no match found
        return None

    def remove(self, old_item):
        """Remove an item from the quiz

        Args:
            old_item: quiz item to be removed

        Raises:
            a TypeError if the item is not in the quiz

        """
        pass

    def destroy(self):
        """Erase the quiz from the persistent store

            Raises:
                IOError: if quiz name is not found in storage or cannot be destroyed
        """
        qpersist.destroy(self)  # delegated


class QuizItem:
    """Individual items for the Quiz object

    Attributes:
         question (str): The multiple choice question
         correct_answer (str): The correct answer
         incorrect_answers (list of str): List of incorrect answers

    Special Methods:
        __iter__ : the iterator returns the answers in sequence, starting with the correct answer

    """

    def __init__(self, question, correct_answer, incorrect_answers):
        self.question = question
        self.correct_answer = correct_answer
        self.incorrect_answers = incorrect_answers
        self._iter_delegate = None

    def __len__(self):
        return len(self.incorrect_answers) + 1

    def __getattr__(self, attr):
        if attr == 'answers':
            return [self.correct_answer] + self.incorrect_answers
        else:
            raise AttributeError

    def __getitem__(self, item):
        if item == 0:
            return self.correct_answer
        else:
            return self.incorrect_answers[item + 1]

    def __iter__(self):
        return self

    def __next__(self):
        if not self._iter_delegate:
            self._iter_delegate = iter(self.incorrect_answers)
            return self.correct_answer
        else:
            try:
                next_one = next(self._iter_delegate)
            except StopIteration:
                self._iter_delegate = None
                raise
            return next_one
