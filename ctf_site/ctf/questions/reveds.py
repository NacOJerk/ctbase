from ..question import question

@question("resistor_question.html", "Resistance", 100, "Reved's")
def resistors(answer):
    if answer == "hello":
        return 1
    return 2
