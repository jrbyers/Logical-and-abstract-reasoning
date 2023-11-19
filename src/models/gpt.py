
from .base import Model

import openai
import backoff
from retrying import retry
import time

class GPTModel(Model):

    def __init__(self, model_name, api_key, model_type=None, temperature=0.5, max_tokens=4097, **kwargs):
        self.model_name = model_name
        self.model_type = model_type
        self.api_key = api_key
        self.temperature = temperature
        self.max_tokens = max_tokens
        openai.api_key = self.api_key

    def load(self):
        pass # no load required as calls are made to API

    def format_data(self, data: dict) -> tuple:
        return data["input"], data["ideal"]

    def answer_query(self, prompt):
        if self.model_type == "completion":
            return self._prompt_completion(prompt)
            #return backoff(self._prompt_completion,
             #              args = [prompt],
              #             max_delay = 10)


        elif self.model_type == "chat":   #GPT-3.5 is chat
            #return self._prompt_chat(prompt)
        
            timeout = 5
            start_time = time.time()
            try:
                result = self._prompt_chat(prompt)
            except Exception as e:
                print("Error: " + e)

            end_time = time.time()
            elapsed_time = end_time - start_time

            if elapsed_time < timeout:
                return result  # Exit the loop if the function executed within the timeout
            else:
                print("Function execution took longer than " + str(timeout) + " seconds. Moving to next test...")
                return


            #return backoff(self._prompt_chat,
             #              args = [prompt],
              #             max_delay = 10)
        else:
            raise ValueError(f"Model type {self.model_type} not found.")
        
    @retry(stop_max_delay=5000, wait_fixed=1000)   # functionality to retry if api hangs
    def _prompt_completion(self, prompt):
        print("line1")
        prompt = self.convert_input_list_to_text(prompt)
        
        print("line2")
        # legacy code was openai.Completion.create
        response = openai.chat.completions.create(
            engine=self.model_name,
            prompt=prompt,
            max_tokens=self.max_tokens,
            n=1,
            stop=None,
            temperature=self.temperature,
            request_timeout=1)  #request_timeout = 10
        print("line3")
        return [self._postprocess(choice.text) for choice in response.choices]
    
    @retry(stop_max_delay=5000, wait_fixed=1000)   # functionality to retry if api hangs
    def _prompt_chat(self, prompt):
        responses = []
        for i in range(len(prompt[0]["content"])):
            prompt_i = self._get_prompt_i(prompt, i)

            # legacy code was openai.Completion.create
            response = openai.chat.completions.create(
                model=self.model_name,
                messages=prompt_i,
                max_tokens=self.max_tokens,
                n=1,
                stop=None,
                temperature=self.temperature,
                request_timeout=10)
            responses.append(self._postprocess(response.choices[0].message.content))
        return responses
    
    def _get_prompt_i(self, prompt, i):
        prompt_i = []
        for p in prompt:
            p_i = {}
            for k, v in p.items():
                p_i[k] = v[i]
            prompt_i.append(p_i)
        return prompt_i

    def _postprocess(self, text):
        if len(text) == 0:
            return "<|endoftext|>"
        else:
            return text
        
    

class GPTModelCompletion(GPTModel):
    def __init__(self, model_name, api_key, model_type=None, temperature=0.5, max_tokens=4097, **kwargs):
        super().__init__(model_name, api_key, model_type, temperature, max_tokens, **kwargs)
        self.model_type = "completion"

    def answer_query(self, prompt):
        return self._prompt_completion(prompt)
    
class GPTModelChat(GPTModel):
    def __init__(self, model_name, api_key, model_type=None, temperature=0.5, max_tokens=4097, **kwargs):
        super().__init__(model_name, api_key, model_type, temperature, max_tokens, **kwargs)
        self.model_type = "chat"

    def answer_query(self, prompt):
        return self._prompt_chat(prompt)
