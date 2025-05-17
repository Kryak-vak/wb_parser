from pydantic import BaseModel, ConfigDict, model_validator
from httpx import URL


class ItemCard(BaseModel):
    model_config = ConfigDict(
        extra="ignore",
        arbitrary_types_allowed=True,
        json_encoders={URL: lambda u: str(u)},
    )

    nm_id: int
    imt_name: str
    subj_name: str
    subj_root_name: str
    description: str
    item_url: URL

    key_requests: dict[str, int] = dict()
    
    brand_name: str | None = None

    @model_validator(mode="before")
    @classmethod
    def extract_brand_name(cls, data: dict):
        selling = data.get("selling", {})
        if "brand_name" in selling:
            data["brand_name"] = selling["brand_name"]
        return data