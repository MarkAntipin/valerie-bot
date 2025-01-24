from pydantic import BaseModel, Field


class ReviewKeyword(BaseModel):
    keyword: str
    count: int


class Coordinates(BaseModel):
    latitude: float
    longitude: float


class AboutOption(BaseModel):
    name: str
    enabled: bool


class About(BaseModel):
    id: str
    name: str
    options: list[AboutOption]


class Review(BaseModel):
    review_id: str
    rating: int | None
    review_text: str | None
    published_at: str
    published_at_date: str
    response_from_owner_text: str | None
    response_from_owner_ago: str | None
    response_from_owner_date: str | None
    review_likes_count: int
    total_number_of_reviews_by_reviewer: int | None
    total_number_of_photos_by_reviewer: int | None
    is_local_guide: bool
    review_translated_text: str | None
    response_from_owner_translated_text: str | None


class PlaceMetadata(BaseModel):
    place_id: str
    name: str
    reviews: int
    address: str
    description: str | None = None
    main_category: str
    categories: list[str]
    rating: float
    review_keywords: list[ReviewKeyword] | None = None
    link: str
    reviews_per_rating: dict[str, int | None] | None = None
    coordinates: dict[str, float]
    cid: str
    about: list[About]
    featured_reviews: list[Review]


class Place(BaseModel):
    place_id: int
    metadata: PlaceMetadata


class RecommendPlacesResponseFormat(BaseModel):
    message: str = Field(description="Response on user prompt")
    place_id: int = Field(description="Place ID")
