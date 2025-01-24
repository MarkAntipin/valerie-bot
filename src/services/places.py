import asyncpg

from src.mappers.places import map_place_from_pg_row
from src.models.places import Place, RecommendPlacesResponseFormat
from src.repositories.open_ai import OpenAIClient
from src.repositories.postgres.places import PlacesRepo
from src.texts import AUGMENTED_PROMPT


class PlacesService:
    def __init__(self, pg_pool: asyncpg.Pool) -> None:
        self.places_repo = PlacesRepo(pg_pool=pg_pool)
        self.open_ai_client = OpenAIClient()

    async def find_places(self, query: str) -> str | None:
        # TODO: preprocess query? with GPT?
        embeddings = self.open_ai_client.get_embeddings(texts=[query])
        if not embeddings:
            return

        rows = await self.places_repo.find_simular(embedding=embeddings[0])
        if not rows:
            return

        simular_places: list[Place] = [map_place_from_pg_row(row) for row in rows]

        retrieved_context: str = _places_to_prompt(places=simular_places)

        # TODO: handle errors
        resp: RecommendPlacesResponseFormat = self.recommend_places(query=query, retrieved_context=retrieved_context)

        place = next((place for place in simular_places if place.place_id == resp.place_id), None)
        if not place:
            return

        return (
            f'{_escape_symbols(resp.message)}'
            f'\n\n[{_escape_symbols(place.metadata.name)}]({_escape_symbols(place.metadata.link)})'
        )

    def recommend_places(self, query: str, retrieved_context: str) -> RecommendPlacesResponseFormat:
        augmented_prompt = AUGMENTED_PROMPT.format(
            query=query,
            retrieved_context=retrieved_context
        )
        res = self.open_ai_client.get_response(prompt=augmented_prompt, response_format=RecommendPlacesResponseFormat)
        return res


def _escape_symbols(text: str) -> str:
    special_symbols = r"_*[]()~`>#+-=|{}.!"
    escaped_text = ""

    for char in text:
        if char in special_symbols:
            escaped_text += f"\\{char}"
        else:
            escaped_text += char

    return escaped_text


# TODO: places to prompt refactor + rewrite
def _places_to_prompt(places: list[Place]) -> str:
    places_prompts = [_place_to_prompt(place=p) for p in places]
    return '\n'.join(places_prompts)


def _place_to_prompt(place: Place) -> str:
    metadata = place.metadata

    prompt: str = f'Place id: {place.place_id}.'
    prompt += f'Place name: {metadata.name}.'

    if metadata.description:
        prompt += f'Description: {metadata.description}'

    if metadata.categories:
        categories_str = ', '.join(metadata.categories)
        prompt += f'Categories: {categories_str}.'

    return prompt
