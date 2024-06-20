import os
import openai
import re
from dotenv import load_dotenv

load_dotenv()


def get_json(text):
    json_match = re.search(r"```json\n(.*)\n```", text, re.DOTALL)
    return json_match.group(1) if json_match else None


class OpenaiAPI:
    import os

    # Set your OpenAI API key
    openai.api_key = os.getenv("OPENAI_APIKEY")

    def __int__(self):
        pass

    def get_completion(self, model="gpt-4o",
                       prompt="",
                       temperature=0.2,
                       max_tokens=1000,
                       top_p=1,
                       frequency_penalty=0,
                       presence_penalty=0,
                       stop=["###"],
                       system_prompt="You are a helpful assistant for teachers and students.",
                       chat_gpt=True):
        try:
            result = ""
            if chat_gpt:
                response = openai.ChatCompletion.create(
                    model="gpt-4o",
                    messages=[
                        # {"role": "system", "content": system_prompt},
                        {"role": "user", "content": prompt},
                    ],
                    stop=stop,
                    seed=123456,
                    temperature=temperature
                )
                result = str(response['choices'][0]
                             ['message']["content"]).strip()
            else:
                response = openai.Completion.create(
                    model=model,
                    prompt=f"{system_prompt}\n{prompt}",
                    temperature=temperature,
                    max_tokens=max_tokens,
                    top_p=top_p,
                    frequency_penalty=frequency_penalty,
                    presence_penalty=presence_penalty,
                    stop=stop,
                    seed=123456
                )
                result = str(response['choices'][0]['text']).strip()

            return result

        except Exception as e:
            return f"Error: {str(e)}"

    def get_moderation(self, text):
        try:
            response = openai.Moderation.create(
                input=str(text)
            )

            return response["results"][0]["flagged"], response["results"][0]
        except Exception as e:
            return f"Error: {str(e)}"
