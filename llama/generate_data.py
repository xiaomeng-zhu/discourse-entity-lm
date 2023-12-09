def generate_example_affirmative_negation(name, pronoun, verb_pres, verb_pst, indef_1, noun_1, indef_2, noun_2):
    negation_affirmative_1 = "{} didn't {} {} {} but {} {} {} {}.".format(name, verb_pres, indef_1, noun_1, pronoun, verb_pst, indef_2, noun_2)
    negation_affirmative_2 = "{} didn't {} {} {} but {} {} {} {}.".format(name, verb_pres, indef_2, noun_2, pronoun, verb_pst, indef_1, noun_1)
    affirmative_negation_1 = "{} {} {} {} but {} didn't {} {} {}.".format(name, verb_pst, indef_1, noun_1, pronoun, verb_pres, indef_2, noun_2)
    affirmative_negation_2 = "{} {} {} {} but {} didn't {} {} {}.".format(name, verb_pst, indef_2, noun_2, pronoun, verb_pres, indef_1, noun_1)
    return [negation_affirmative_1, negation_affirmative_2, affirmative_negation_1, affirmative_negation_2]


def generate_example_affirmative_modal(name, pronoun, verb_pres, verb_pst, indef_1, noun_1, indef_2, noun_2):
    modal_affirmative_1 = "{} wanted to {} {} {} but {} {} {} {}.".format(name, verb_pres, indef_1, noun_1, pronoun, verb_pst, indef_2, noun_2)
    modal_affirmative_2 = "{} wanted to {} {} {} but {} {} {} {}.".format(name, verb_pres, indef_2, noun_2, pronoun, verb_pst, indef_1, noun_1)
    affirmative_modal_1 = "{} {} {} {} but {} wanted to {} {} {}.".format(name, verb_pst, indef_1, noun_1, pronoun, verb_pres, indef_2, noun_2)
    affirmative_modal_2 = "{} {} {} {} but {} wanted to {} {} {}.".format(name, verb_pst, indef_2, noun_2, pronoun, verb_pres, indef_1, noun_1)
    return [modal_affirmative_1, modal_affirmative_2, affirmative_modal_1, affirmative_modal_2]


def generate_example_managed_failed(name, pronoun, verb_pres, verb_pst, indef_1, noun_1, indef_2, noun_2):
    managed_failed_1 = "{} managed to {} {} {} but {} failed to {} {} {}.".format(name, verb_pres, indef_1, noun_1, pronoun, verb_pres, indef_2, noun_2)
    managed_failed_2 = "{} managed to {} {} {} but {} failed to {} {} {}.".format(name, verb_pres, indef_2, noun_2, pronoun, verb_pres, indef_1, noun_1)
    failed_managed_1 = "{} failed to {} {} {} but {} managed to {} {} {}.".format(name, verb_pres, indef_1, noun_1, pronoun, verb_pres, indef_2, noun_2)
    failed_managed_2 = "{} failed to {} {} {} but {} managed to {} {} {}.".format(name, verb_pres, indef_2, noun_2, pronoun, verb_pres, indef_1, noun_1)
    return [managed_failed_1, managed_failed_2, failed_managed_1, failed_managed_2]

def generate_example_managed_failed(name, pronoun, verb_pres, verb_pst, indef_1, noun_1, indef_2, noun_2):
    know_doubt_1 = "I know that {} {} {} {} but I doubt that {} {} {} {}.".format(name, verb_pst, indef_1, noun_1, pronoun, verb_pst, indef_2, noun_2)
    know_doubt_2 = "I know that {} {} {} {} but I doubt that {} {} {} {}.".format(name, verb_pst, indef_2, noun_2, pronoun, verb_pst, indef_1, noun_1)
    doubt_know_1 = "I doubt that {} {} {} {} but I know that {} {} {} {}.".format(name, verb_pst, indef_1, noun_1, pronoun, verb_pst, indef_2, noun_2)
    doubt_know_2 = "I doubt that {} {} {} {} but I know that {} {} {} {}.".format(name, verb_pst, indef_2, noun_2, pronoun, verb_pst, indef_1, noun_1)
    return [know_doubt_1, know_doubt_2, doubt_know_1, doubt_know_2]

def generate_examples(items):
    examples = []
    for item in items:
        pass
        

def main():
    print(generate_example_affirmative_negation("Mandy", "she", "complete", "completed", "a", "project", "an", "assignment"))
    print(generate_example_affirmative_modal("Mandy", "she", "complete", "completed", "a", "project", "an", "assignment"))
    print(generate_example_managed_failed("Mandy", "she", "complete", "completed", "a", "project", "an", "assignment"))
    print(generate_example_managed_failed("Mandy", "she", "complete", "completed", "a", "project", "an", "assignment"))
main()