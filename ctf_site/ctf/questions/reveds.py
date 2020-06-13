from ..question import question


@question("resistor_question.html", "Resistance", 100, "Reveds")
def resistors(answer):
    if answer == "hello":
        return 1
    return 2
