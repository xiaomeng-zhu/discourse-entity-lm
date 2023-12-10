import csv, itertools
COL_NAMES = ["negation_affirmative1",
             "negation_affirmative2",
             "affirmative_negation1",
             "affirmative_negation2",
             "modal_affirmative1",
             "modal_affirmative2",
             "affirmative_modal1",
             "affirmative_modal2",
             "managed_failed1",
             "managed_failed2",
             "failed_managed1",
             "failed_managed2",
             "know_doubt1",
             "know_doubt2",
             "doubt_know1",
             "doubt_know2"]

def read_names():
    with open("llama/boy_names.txt") as f:
        boys = [name.strip() for name in f.readlines()]
    with open("llama/girl_names.txt") as f:
        girls = [name.strip() for name in f.readlines()]
    # make sure that there are 80 unique names in each gender
    assert(len(set(boys))==80)
    assert(len(set(girls))==80)
    return boys + girls

def read_extended_items():
    rows = []
    with open("llama/extended_stimuli.csv") as f:
        reader = csv.DictReader(f)
        for row in reader:
            rows.append(row)
    return rows

def generate_examples(items, boy_names, girl_names):
    examples = []
    boy_idx = 0
    girl_idx = 0
    total_idx = 1
    for idx, row in enumerate(items):
        pronoun = row["pronoun"]
        verb_pres = row["verb_pres"]
        verb_mf = row["verb_mf"]
        verb_alt = row["verb_altt"]
        optional_PP = row["PP_1"] + " " if row["PP_1"] != "" else ""
        nouns = row["nouns"].split("/")
        old_ref_continuation_1, old_nonref_continuation_1, old_noun_1, old_ref_continuation_2, old_nonref_continuation_2, old_noun_2 = row["continuation_ref_1"], row["continuation_nonref_1"], row["noun_1"], row["continuation_ref_2"], row["continuation_nonref_2"], row["noun_2"]

        nouns_pair = [tuple(phrase.split(" ")) for phrase in nouns]
        print(nouns_pair)
        noun_pair_combinations = list(itertools.combinations(nouns_pair, 2))
        for pair in noun_pair_combinations:
            print(pair)
        

        for phrase_1, phrase_2 in noun_pair_combinations:
            example = {}
            if len(phrase_1) != 3 and len(phrase_2) != 3: # normal case
                det_1, noun_1 = phrase_1
                det_2, noun_2 = phrase_2
            elif len(phrase_1) == 3 and len(phrase_2) == 2:
                det_1, noun_11, noun_12 = phrase_1
                noun_1 = noun_11 + " " + noun_12
                det_2, noun_2 = phrase_2
            elif len(phrase_2) == 3 and len(phrase_1) == 2:
                det_2, noun_21, noun_22 = phrase_2
                noun_2 = noun_21 + " " + noun_22
                det_1, noun_1 = phrase_1
            else: # both are 3
                det_1, noun_11, noun_12 = phrase_1
                noun_1 = noun_11 + " " + noun_12
                det_2, noun_21, noun_22 = phrase_2
                noun_2 = noun_21 + " " + noun_22
                

            example["id"] = "{}_{}_{}".format(str(total_idx), noun_1, noun_2)

            if pronoun == "he":
                name = boy_names[boy_idx] 
                boy_idx += 1
            else:
                name = girl_names[girl_idx]
                girl_idx += 1

            if idx in [0,1]: # the first two sentences are in present tense
                an = generate_example_affirmative_negation_pres(name, pronoun, verb_pres, verb_alt, det_1, noun_1, det_2, noun_2, optional_PP)
                am = generate_example_affirmative_modal_pres(name, pronoun, verb_pres, verb_alt, det_1, noun_1, det_2, noun_2, optional_PP)
            else:
                an = generate_example_affirmative_negation_pst(name, pronoun, verb_pres, verb_alt, det_1, noun_1, det_2, noun_2, optional_PP)
                am = generate_example_affirmative_modal_pst(name, pronoun, verb_pres, verb_alt, det_1, noun_1, det_2, noun_2, optional_PP)
            
            if verb_mf != "":
                # a different verb for the managed failed case
                mf = generate_example_managed_failed(name, pronoun, verb_mf, verb_alt, det_1, noun_1, det_2, noun_2, optional_PP)
            else:
                mf = generate_example_managed_failed(name, pronoun, verb_pres, verb_alt, det_1, noun_1, det_2, noun_2, optional_PP)
            
            kd = generate_example_know_doubt(name, pronoun, verb_pres, verb_alt, det_1, noun_1, det_2, noun_2, optional_PP)

            all_sents = an+am+mf+kd
            for col_name, sent in list(zip(COL_NAMES, all_sents)):
                example[col_name] = sent

            new_ref_continuation_1 = old_ref_continuation_1.replace(f" {old_noun_1} ", f" {noun_1} ")
            new_ref_continuation_2 = old_ref_continuation_2.replace(f" {old_noun_2} ", f" {noun_2} ")
            new_nonref_continuation_1 = old_nonref_continuation_1.replace(f" {old_noun_1} ", f" {noun_1} ")
            new_nonref_continuation_2 = old_nonref_continuation_2.replace(f" {old_noun_2} ", f" {noun_2} ")
            example["continuation_ref_1"] = new_ref_continuation_1
            example["continuation_ref_2"] = new_ref_continuation_2
            example["continuation_nonref_1"] = new_nonref_continuation_1
            example["continuation_nonref_2"] = new_nonref_continuation_2
 
            examples.append(example) # should be of len 160
            total_idx += 1
            
    return examples


def generate_example_affirmative_negation_pst(name, pronoun, verb_pres, verb_pst, indef_1, noun_1, indef_2, noun_2, optional_PP):
    negation_affirmative_1 = "{} didn't {} {} {} {}but {} {} {} {}.".format(name, verb_pres, indef_1, noun_1, optional_PP, pronoun, verb_pst, indef_2, noun_2)
    negation_affirmative_2 = "{} didn't {} {} {} {}but {} {} {} {}.".format(name, verb_pres, indef_2, noun_2, optional_PP, pronoun, verb_pst, indef_1, noun_1)
    affirmative_negation_1 = "{} {} {} {} {}but {} didn't {} {} {}.".format(name, verb_pst, indef_1, noun_1, optional_PP, pronoun, verb_pres, indef_2, noun_2)
    affirmative_negation_2 = "{} {} {} {} {}but {} didn't {} {} {}.".format(name, verb_pst, indef_2, noun_2, optional_PP, pronoun, verb_pres, indef_1, noun_1)
    return [negation_affirmative_1, negation_affirmative_2, affirmative_negation_1, affirmative_negation_2]

def generate_example_affirmative_negation_pres(name, pronoun, verb_pres, verb_pres_s, indef_1, noun_1, indef_2, noun_2, optional_PP):
    negation_affirmative_1 = "{} doesn't {} {} {} {}but {} {} {} {}.".format(name, verb_pres, indef_1, noun_1, optional_PP, pronoun, verb_pres_s, indef_2, noun_2)
    negation_affirmative_2 = "{} doesn't {} {} {} {}but {} {} {} {}.".format(name, verb_pres, indef_2, noun_2, optional_PP, pronoun, verb_pres_s, indef_1, noun_1)
    affirmative_negation_1 = "{} {} {} {} {}but {} doesn't {} {} {}.".format(name, verb_pres_s, indef_1, noun_1, optional_PP, pronoun, verb_pres, indef_2, noun_2)
    affirmative_negation_2 = "{} {} {} {} {}but {} doesn't {} {} {}.".format(name, verb_pres_s, indef_2, noun_2, optional_PP, pronoun, verb_pres, indef_1, noun_1)
    return [negation_affirmative_1, negation_affirmative_2, affirmative_negation_1, affirmative_negation_2]


def generate_example_affirmative_modal_pst(name, pronoun, verb_pres, verb_pst, indef_1, noun_1, indef_2, noun_2, optional_PP):
    modal_affirmative_1 = "{} wanted to {} {} {} {}but {} {} {} {}.".format(name, verb_pres, indef_1, noun_1, optional_PP, pronoun, verb_pst, indef_2, noun_2)
    modal_affirmative_2 = "{} wanted to {} {} {} {}but {} {} {} {}.".format(name, verb_pres, indef_2, noun_2, optional_PP, pronoun, verb_pst, indef_1, noun_1)
    affirmative_modal_1 = "{} {} {} {} {}but {} wanted to {} {} {}.".format(name, verb_pst, indef_1, noun_1, optional_PP, pronoun, verb_pres, indef_2, noun_2)
    affirmative_modal_2 = "{} {} {} {} {}but {} wanted to {} {} {}.".format(name, verb_pst, indef_2, noun_2, optional_PP, pronoun, verb_pres, indef_1, noun_1)
    return [modal_affirmative_1, modal_affirmative_2, affirmative_modal_1, affirmative_modal_2]

def generate_example_affirmative_modal_pres(name, pronoun, verb_pres, verb_pres_s, indef_1, noun_1, indef_2, noun_2, optional_PP):
    modal_affirmative_1 = "{} wants to {} {} {} {}but {} {} {} {}.".format(name, verb_pres, indef_1, noun_1, optional_PP, pronoun, verb_pres_s, indef_2, noun_2)
    modal_affirmative_2 = "{} wants to {} {} {} {}but {} {} {} {}.".format(name, verb_pres, indef_2, noun_2, optional_PP, pronoun, verb_pres_s, indef_1, noun_1)
    affirmative_modal_1 = "{} {} {} {} {}but {} wants to {} {} {}.".format(name, verb_pres_s, indef_1, noun_1, optional_PP, pronoun, verb_pres, indef_2, noun_2)
    affirmative_modal_2 = "{} {} {} {} {}but {} wants to {} {} {}.".format(name, verb_pres_s, indef_2, noun_2, optional_PP, pronoun, verb_pres, indef_1, noun_1)
    return [modal_affirmative_1, modal_affirmative_2, affirmative_modal_1, affirmative_modal_2]


def generate_example_managed_failed(name, pronoun, verb_pres, verb_pst, indef_1, noun_1, indef_2, noun_2, optional_PP):
    managed_failed_1 = "{} managed to {} {} {} {}but {} failed to {} {} {}.".format(name, verb_pres, indef_1, noun_1, optional_PP, pronoun, verb_pres, indef_2, noun_2)
    managed_failed_2 = "{} managed to {} {} {} {}but {} failed to {} {} {}.".format(name, verb_pres, indef_2, noun_2, optional_PP, pronoun, verb_pres, indef_1, noun_1)
    failed_managed_1 = "{} failed to {} {} {} {}but {} managed to {} {} {}.".format(name, verb_pres, indef_1, noun_1, optional_PP, pronoun, verb_pres, indef_2, noun_2)
    failed_managed_2 = "{} failed to {} {} {} {}but {} managed to {} {} {}.".format(name, verb_pres, indef_2, noun_2, optional_PP, pronoun, verb_pres, indef_1, noun_1)
    return [managed_failed_1, managed_failed_2, failed_managed_1, failed_managed_2]

def generate_example_know_doubt(name, pronoun, verb_pres, verb_altt, indef_1, noun_1, indef_2, noun_2, optional_PP):
    know_doubt_1 = "I know that {} {} {} {} {}but I doubt that {} {} {} {}.".format(name, verb_altt, indef_1, noun_1, optional_PP, pronoun, verb_altt, indef_2, noun_2)
    know_doubt_2 = "I know that {} {} {} {} {}but I doubt that {} {} {} {}.".format(name, verb_altt, indef_2, noun_2, optional_PP, pronoun, verb_altt, indef_1, noun_1)
    doubt_know_1 = "I doubt that {} {} {} {} {}but I know that {} {} {} {}.".format(name, verb_altt, indef_1, noun_1, optional_PP, pronoun, verb_altt, indef_2, noun_2)
    doubt_know_2 = "I doubt that {} {} {} {} {}but I know that {} {} {} {}.".format(name, verb_altt, indef_2, noun_2, optional_PP, pronoun, verb_altt, indef_1, noun_1)
    return [know_doubt_1, know_doubt_2, doubt_know_1, doubt_know_2]

def write_to_csv(examples):
    with open("llama/extended_stimuli_complete.csv", "w") as f:
        writer = csv.DictWriter(f, fieldnames=examples[0].keys())
        writer.writeheader()
        writer.writerows(examples)


def main():
    names = read_names()
    boy_names = names[:80]
    girl_names = names[80:]
    items = read_extended_items()
    examples = generate_examples(items, boy_names, girl_names)
    write_to_csv(examples)
main()