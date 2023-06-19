from llama_cpp import Llama


class LlamaModel_llama_cpp:
    def __init__(self, model_path):
        self.llm = Llama(model_path)

    def compute_text(self, input_str):
        output = self.llm.create_completion(
            prompt=input_str,
            suffix=None,
            max_tokens=30,
            temperature=0.8,
            top_p=0.95,
            logprobs=None,
            echo=False,
            stop=["Player"],
            frequency_penalty=0.0,
            presence_penalty=0.0,
            repeat_penalty=1.1,
            top_k=40,
            stream=False,
            tfs_z=1.0,
            mirostat_mode=0,
            mirostat_tau=5.0,
            mirostat_eta=0.1,
            model=None,
            stopping_criteria=None,
            logits_processor=None,
        )
        text = output.get("choices")[0].get("text")[:-2]
        return text.split(".")[0]
