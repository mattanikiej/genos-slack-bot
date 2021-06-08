import random


class Trivia:
    """
    This class stores all questions and answers for the /trivia command.
    It also stores if a question has been answered, or needs to be answered.
    This is to make sure it only collects the first response to the question.
    Feel free to add as many questions and answers as you'd like!
    """
    def __init__(self):
        self.questions = ["What is my name?",
                          "What show does my name come from?",
                          "What is the best droid in Star Wars",  # This is a fun one whose answer can be changed
                          "Eggs of what sturgeon are the preferred form of caviar?",
                          "Which of Jupiter's moons is the most volcanically active body in the solar system?"]

        self.answers = ["Genos",
                        "One Punch Man",
                        "Gonk Droid",  # The Gonk Droid is easily the best, anyone who says otherwise is wrong
                        "Beluga",
                        "Io"]

        self.was_asked = False

        self.question_number = 0

    def ask_random_question(self):
        """
        Finds a random integer for the index of the question
        :return: question that corresponds to the random index
        """
        # sets asked flag for bot
        self.was_asked = True
        self.question_number = random.randint(0, len(self.questions) - 1)
        return self.questions[self.question_number]

    def is_correct(self, answer):
        """
        checks if answer is correct
        :param answer: string representing answer
        :return: True if correct, False otherwise
        """
        # resets asked flag
        self.was_asked = False
        if self.answers[self.question_number].lower() == answer.lower():
            return True
        return False
