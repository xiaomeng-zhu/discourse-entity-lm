# adapted from https://github.com/EleutherAI/lm-evaluation-harness/issues/539
import json, csv, tqdm
import torch
import torch.nn.functional as F
from transformers import AutoTokenizer, AutoModelForCausalLM

# load in data
print("Loading data...")
stimuli_dir = "stimuli/"
single_noun_data_fname = "full_sentence_hand_written_stimuli.jsonl"

single_noun_data = []
with open(stimuli_dir + single_noun_data_fname, "r") as jsonl_f:
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
print(single_noun_data)
print("Finished loading data.")

print("Loading tokenizer...")
tokenizer = AutoTokenizer.from_pretrained('huggyllama/llama2-7b')
print("Finished loading tokenizer")
print("Loading llama...")
# model = AutoModelForCausalLM.from_pretrained('huggyllama/llama-7b', device_map='auto', load_in_8bit=True)
model = AutoModelForCausalLM.from_pretrained('huggyllama/llama-7b', device_map='auto')
print("Finished loading llama")

for example in single_noun_data:
    # clean up data to remove punctuations and expand contractions
    sentence = example['sentence'].strip()
    print(sentence)
    tokens = tokenizer.tokenize(sentence)

    # feed sentence to llama
    batched_sentences = tokenizer.batch_encode_plus([sentence], add_special_tokens=False, return_tensors='pt')['input_ids']
    # run the model on full sentences and get the log probabilities
    batched_logprobs = F.log_softmax(model(batched_sentences)['logits'], dim=-1)
    # print(batched_logprobs, batched_logprobs.size())
    next_word_logs = []
    for i, distr in enumerate(batched_logprobs[0]):
        if i == batched_logprobs.size()[1]-1:
            continue
        logprob = distr[batched_sentences[0][i+1]]
        next_word_logs.append(logprob.item())
    example["logprobs"] = next_word_logs

    # decide critical token index
    critical_token_idx = -1
    for i, token in enumerate(tokens):
        if (token == "▁it" or token == "▁It" or token == "▁they" or token == "▁They") and i > 0 and ("▁and" == tokens[i-1] or tokens[i-1] == "."):
            critical_token_idx = i-1
            break

    if critical_token_idx < 0:
        print("ERROR: critical token idx is 0!!!")
    # print(critical_token_idx)
    continuation_log_prob = sum(next_word_logs[critical_token_idx: -1])
    example["continuation_log_prob"] = continuation_log_prob
    example["id_num"] = example["id"].split("_")[0]
    example["tokens"] = "|".join(tokens)
    # print(example)
    # break

with open("llama/entity_single_res.csv", "w") as out_f:
      writer = csv.DictWriter(out_f, single_noun_data[0].keys())
      writer.writeheader()
      writer.writerows(single_noun_data)