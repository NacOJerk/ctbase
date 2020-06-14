from ..question import question


@question("resistor_question.html", "Resistance", 100, "Reveds")
def resistors(answer):
    if answer.lower() == "hello":
        return 1
    return 2


@question("pnp_question.html", "PNP", 1000, "Computers")
def resistors(answer):
    if answer.lower() == "no":
        return 1
    return 2