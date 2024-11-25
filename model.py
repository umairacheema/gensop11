from transformers import AutoTokenizer, AutoModelForCausalLM
import torch
from gensop_config import GenSOPConfig


class GenSOPModel:
    def __init__(self):
        self.config = GenSOPConfig(file_path='./gensop.yaml').read()
        self.model_name = self.config['model_name']
        self.model_path = self.config['model_path']
        self.device = self.config['device']
        self.model = None
        self.system_prompt = self.config['system_prompt']
        self.tokenizer = None
        self.terminators = None

    def load_model(self):

        self.tokenizer = AutoTokenizer.from_pretrained(self.model_path)
        self.model = AutoModelForCausalLM.from_pretrained(
                   self.model_path,
                   torch_dtype=torch.bfloat16,
                   device_map=self.device,
            )

     
    def generate_response(self, user_prompt):

        messages = [
        {"role": "system", "content": self.system_prompt},
        {"role": "user", "content": user_prompt},
         ]
        
        input_ids = self.tokenizer.apply_chat_template(
            messages,
            add_generation_prompt=True,
            return_tensors="pt"
        ).to(self.model.device)

        self.terminators = [
            self.tokenizer.eos_token_id,
            self.tokenizer.convert_tokens_to_ids("<|eot_id|>")
        ]

        outputs = self.model.generate(
            input_ids,
            max_new_tokens=2000,
            eos_token_id=self.terminators,
            do_sample=True,
            temperature=0.6,
            top_p=0.9,
        )
        
        response = outputs[0][input_ids.shape[-1]:]
        return self.tokenizer.decode(response, skip_special_tokens=True)
