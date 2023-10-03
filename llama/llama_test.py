# adapted from https://github.com/EleutherAI/lm-evaluation-harness/issues/539
import json
import torch
import torch.nn.functional as F
from transformers import AutoTokenizer, AutoModelForCausalLM


tokenizer = AutoTokenizer.from_pretrained('huggyllama/llama-7b')
model = AutoModelForCausalLM.from_pretrained('huggyllama/llama-7b', device_map='auto', load_in_8bit=True)

eg_sentence = "John owns a dog and it follows him everywhere he goes."

# encode full sentences, questions, and answers, no padding for simplicity
batched_sentences = tokenizer.batch_encode_plus([eg_sentence], add_special_tokens=False, return_tensors='pt')['input_ids']

# run the model on full sentences and get the log probabilities
batched_logprobs = F.log_softmax(model(batched_sentences.cuda())['logits'], dim=-1).cpu()
print(batched_logprobs)