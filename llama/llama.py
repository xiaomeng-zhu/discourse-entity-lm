# adapted from https://github.com/EleutherAI/lm-evaluation-harness/issues/539
import json, csv
from tqdm import tqdm
import torch
import torch.nn.functional as F
from transformers import AutoTokenizer, AutoModelForCausalLM
import numpy as np

# ======= load in data ======
print("Loading data...")
stimuli_dir = "llama/"
# single_noun_data_fname = "full_sentence_hand_written_stimuli.jsonl"
double_noun_data_fname = "extended_stimuli_complete.jsonl"

def load_single_noun_data(fname):
    single_noun_data = []
    with open(stimuli_dir + fname, "r") as jsonl_f:
            for line in jsonl_f:
                ex = json.loads(line)
                ex1 = {
                    "id": ex["id"],
                    "sentence": ex["i_sentence"],
                    "type": ex["type"],
                    "pronoun": "it"
                }
                ex2 = {
                    "id": ex["id"],
                    "sentence": ex["s_sentence"],
                    "type": ex["type"],
                    "pronoun": "subj"
                }
                single_noun_data.append(ex1)
                single_noun_data.append(ex2)
    # print(single_noun_data)
    print("Finished loading data.")
    return single_noun_data
# single_noun_data = load_single_noun_data(single_noun_data_fname)

def load_double_noun_data(fname):
    double_noun_data = []
    with open(stimuli_dir + fname, "r") as jsonl_f:
        for line in jsonl_f:
            ex = json.loads(line)
            ex1 = {
                "id": ex["id"],
                "sentence": ex["exp_sentence"],
                "type": ex["type"],
                "expected": 1,
                "order": ex["order"]
            }
            ex2 = {
                "id": ex["id"],
                "sentence": ex["unexp_sentence"],
                "type": ex["type"],
                "expected": 0,
                "order": ex["order"]
            }
            double_noun_data.append(ex1)
            double_noun_data.append(ex2)
    # print(double_noun_data)
    return double_noun_data

double_noun_data = load_double_noun_data(double_noun_data_fname)
print(len(double_noun_data))
# print(len(single_noun_data), len(double_noun_data))

# ======= load in tokenizer and model ======
print("Loading tokenizer...")
tokenizer = AutoTokenizer.from_pretrained('meta-llama/Llama-2-7b-hf')
print("Finished loading tokenizer")
print("Loading llama...")
# # model = AutoModelForCausalLM.from_pretrained('huggyllama/llama-7b', device_map='auto', load_in_8bit=True)
model = AutoModelForCausalLM.from_pretrained('meta-llama/Llama-2-7b-hf', device_map='auto')
print("Finished loading llama")

# ======= experiments ========
def exp1(tokenizer, model, single_noun_data):
    for example in single_noun_data:
        # clean up data to remove punctuations and expand contractions
        sentence = example['sentence'].strip()
        # print(sentence)
        tokens = tokenizer.tokenize(sentence)
        # print(tokens)
        # feed sentence to llama
        batched_ids = tokenizer.batch_encode_plus([sentence], add_special_tokens=False, return_tensors='pt')['input_ids']
        # print(batched_ids, len(batched_ids[0]))

        # run the model on full sentences and get the log probabilities
        batched_logprobs = F.log_softmax(model(batched_ids)['logits'], dim=-1)

        # iterate to get the log prob for each word
        next_word_logs = []
        for i, distr in enumerate(batched_logprobs[0]):
            if i == batched_logprobs.size()[1]-1:
                continue
            logprob = distr[batched_ids[0][i+1]]
            # print(tokens[i+1], batched_ids[0][i+1], logprob)
            next_word_logs.append(logprob.item())
        example["logprobs"] = next_word_logs

        # decide critical token index
        critical_token_idx = -1
        for i, token in enumerate(tokens):
            if (token == "▁it" or token == "▁It" or token == "▁they" or token == "▁They") and i > 0 and ("▁and" in tokens[i-1] or tokens[i-1] == "."):
                # critical_token_idx = i
                critical_token_idx = i-1
                break

        if critical_token_idx < 0:
            print("ERROR: critical token idx is 0!!!")
        # print(critical_token_idx)
        # print(next_word_logs[critical_token_idx:-1], len(next_word_logs[critical_token_idx:-1]))
        
        # take into account the log prob of the period
        # continuation_log_prob = sum(next_word_logs[critical_token_idx:-1])
        continuation_log_prob = sum(next_word_logs[critical_token_idx:])
        # print(continuation_log_prob)

        example["continuation_log_prob"] = continuation_log_prob
        example["id_num"] = example["id"].split("_")[0]
        example["tokens"] = "|".join(tokens)
    return single_noun_data

def exp2(tokenizer, model, double_noun_data):
    for example in tqdm(double_noun_data, desc="Processing items", unit="item"):
        sentence = example['sentence'].strip()
        tokens = tokenizer.tokenize(sentence)

        batched_ids = tokenizer.batch_encode_plus([sentence], add_special_tokens=False, return_tensors='pt')['input_ids']
        batched_logprobs = F.log_softmax(model(batched_ids)['logits'], dim=-1)

        next_word_logs = []
        for i, distr in enumerate(batched_logprobs[0]):
            if i == batched_logprobs.size()[1]-1:
                continue
            logprob = distr[batched_ids[0][i+1]]
            # print(tokens[i+1], batched_ids[0][i+1], logprob)
            next_word_logs.append(logprob.item())
        example["logprobs"] = next_word_logs
        
        critical_token_idx = -1

        # every input has a period in exp2
        for i, token in enumerate(tokens):
              if token == ".":
                critical_token_idx = i
                break
              
        if critical_token_idx < 0:
            print("ERROR: critical token idx is 0!!!")
        # print(critical_token_idx)

        continuation_log_prob = sum(next_word_logs[critical_token_idx:])
        # print(continuation_log_prob, next_word_logs[critical_token_idx:])
        example["continuation_log_prob"] = continuation_log_prob
        example["critical_token_idx"] = critical_token_idx
        example["id_num"] = example["id"].split("_")[0]
        example["tokens"] = "|".join(tokens)
        # print(example)
    return double_noun_data
              
# single_noun_res = exp1(tokenizer, model, single_noun_data)
double_noun_res = exp2(tokenizer, model, double_noun_data)

def res_to_csv(out_fname, data):
    with open("llama/"+out_fname, "w") as out_f:
        writer = csv.DictWriter(out_f, data[0].keys())
        writer.writeheader()
        writer.writerows(data)

# res_to_csv("llama2_entity_single_res.csv", single_noun_res)
res_to_csv("llama2_extended.csv", double_noun_res)