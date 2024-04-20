
import os

def load(qobject):
    """Load the named quiz from persistence storage - previously stored

        Args:
            qname: name of quiz to load

        Returns:
            the number of items

        Rasises:
            Standard IO errors if quiz cannot be loaded properly.

    """

    if not os.path.isfile(qobject.name):
        raise IOError("quiz not available")

    with open(qobject.name) as f:
        for line in f:
            if len(line) < 2: continue
            markup=line[0]
            qstring=line[1:-1]
            if markup == 'Q':
                question=qstring
                incorrect=[]
            if markup == 'C':
                correct=qstring
            if markup == 'I':
                incorrect.append(qstring)
            if markup == 'E':
                qobject.add(question,correct,incorrect)
                incorrect=[]

    return len(qobject)

def store(quiz, name=None):
    """Store the quiz object in the persistence storage.
        Args:
            quiz: quiz object to save
            name (optional): name to store the quiz under. Defaults to name of the quiz if none provided.

        Returns:

        Rasises:
            Standard IO errors if quiz cannot be stored properly

    """
    with open(quiz.name, mode="x") as f:
        for qi in quiz:
            print("Q"+qi.question,file=f)
            print("C" + qi.correct_answer, file=f)
            for wrongi in qi.incorrect_answers:
                print("I" + wrongi, file=f)
            print("End",file=f)


def destroy(quiz):
    """Erase the quiz from the persistent store

        Raises:
            IOError: if quiz name is not found in storage or cannot be destroyed

        Note this is a stub implementation and is incorrect unless you decide to
         store each quiz in a separate file under its own name.
    """
    if os.path.isfile(quiz.name):
        os.remove(quiz.name)
    else:
        raise IOError(f"quiz {quiz.name} was never saved")