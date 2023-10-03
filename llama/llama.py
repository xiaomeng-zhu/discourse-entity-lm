import csv, sys, tqdm, json, os
import numpy
import torch
import torch.nn.functional as F
from transformers import AutoTokenizer, AutoModelForCausalLM

with open(sys.argv[1], "r") as config_f:
  config = json.load(config_f)

input_fname = config["input"]
output_fname = config["output"]

examples = []


if ".csv" in input_fname:
    with open(input_fname, "r") as csv_f:
      reader = csv.DictReader(csv_f)
      for line in reader:
        examples.append(line)
else:
    with open(input_fname, "r") as jsonl_f:
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
            examples.append(ex1)
            examples.append(ex2)

tokenizer = AutoTokenizer.from_pretrained('huggyllama/llama-7b')
model = AutoModelForCausalLM.from_pretrained('huggyllama/llama-7b', device_map='auto', load_in_8bit=True)

for idx in tqdm.tqdm(range(int(len(examples)/16))):
    
    sentences = []
    for i in range(16):
      full_sentence = examples[idx*16 + i]["sentence"].replace(" ||| ", "").strip()
      sentences.append(full_sentence)

    batched_sentences = tokenizer.batch_encode_plus(sentences, add_special_tokens=False, return_tensors='pt')['input_ids']
    batched_logprobs = F.log_softmax(model(batched_sentences.cuda())['logits'], dim=-1).cpu()

    for i in range(16):
      examples[idx*16 + i]["tokens"] = "|".join(response["choices"][i]["logprobs"]["tokens"])
      examples[idx*16 + i]["log_probs"] = "|".join([str(p) for p in batched_logprobs])

with open(output_fname, "w") as csv_f:
  writer = csv.DictWriter(csv_f, fieldnames=examples[0].keys())
  writer.writeheader()
  writer.writerows(examples)

