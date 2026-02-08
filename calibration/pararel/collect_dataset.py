from transformers import AutoTokenizer,AutoModelForCausalLM
import torch
import json
from tqdm.auto import tqdm
import random
from argparse import ArgumentParser
from scipy.stats import entropy
import math
import os


import torch.nn as nn

def inference(input_text, model):
    device = next(model.parameters()).device
    full_input = "Question:" + input_text + " Answer:"
    inputs = tokenizer(full_input,return_tensors="pt").to(device)
    ids = inputs['input_ids']
    length = len(ids[0])     
    outputs = model.generate(
            ids,
            max_new_tokens = 15,
        )
    output_text = tokenizer.decode(outputs[0][length:])
    idx = output_text.find('.')
    output_text = output_text[:idx]
    return output_text

if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument('--dataset', type=str, default="training_data")
    parser.add_argument('--model', type=str, required=True)
    parser.add_argument('--result',type=str, default="pararel")
    
    args = parser.parse_args()

    model_name = args.model.split('/')[-1]
    cache_dir = None  # Use default cache directory
    tokenizer = AutoTokenizer.from_pretrained(args.model,use_fast=True,unk_token="<unk>",bos_token="<s>",eos_token="</s>",add_bos_token=False,cache_dir=cache_dir)
    
    # Use single GPU that has most free memory for stability
    model = AutoModelForCausalLM.from_pretrained(
        args.model,
        dtype=torch.float32,  # Use float32 for stability
        device_map={'': 1},   # Use GPU 1 which has the most free memory
        low_cpu_mem_usage=True
    )

    data = []
    with open(f"../../dataset/pararel/{args.dataset}.json",'r') as f:
        data = json.load(f)

    certain_data = []
    uncertain_data = []

    # Process samples individually for stability (proven to work)
    print(f"Processing {len(data)} samples individually")
    
    for sample in tqdm(data):
        try:
            output = inference(sample[0], model)
            if sample[1] in output:
                certain_data.append(sample)
            else:
                uncertain_data.append(sample)
        except Exception as e:
            print(f"Error processing sample: {e}")
            continue

    random.shuffle(certain_data)
    random.shuffle(uncertain_data)

    os.makedirs("../training_data",exist_ok=True)
    with open(f"../training_data/{args.result}_{model_name}_certain.json",'w') as f:
        json.dump(certain_data,f)
    with open(f"../training_data/{args.result}_{model_name}_uncertain.json",'w') as f:
        json.dump(uncertain_data,f)
