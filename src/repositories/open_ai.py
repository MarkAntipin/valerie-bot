from langchain_openai import OpenAIEmbeddings
from openai import OpenAI
from pydantic import BaseModel

from settings import bot_settings


class OpenAIClient:
    def __init__(self) -> None:
        self.client = OpenAI(api_key=bot_settings.OPENAI_KEY)

    def get_response(
        self,
        prompt: str,
        model: str = 'gpt-4o',
        response_format: type[BaseModel] = None,
    ) -> str | BaseModel:
        response = self.client.beta.chat.completions.parse(
            model=model,
            messages=[
                {'role': 'user', 'content': prompt}
            ],
            response_format=response_format
        )
        answer = response.choices[0].message.parsed
        return answer

    @staticmethod
    def get_embeddings(
        texts: list[str],
        model: str = 'text-embedding-3-large'
    ) -> list[list[float]]:
        # TODO: can pass self.client as class init argument?
        embeddings = OpenAIEmbeddings(model=model, api_key=bot_settings.OPENAI_KEY)
        r = embeddings.embed_documents(texts)
        return r
