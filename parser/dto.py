from pydantic import BaseModel, ConfigDict


class ItemCard(BaseModel):
    model_config = ConfigDict(extra="ignore")

    nm_id: int
    imt_name: str
    subj_name: str
    subj_root_name: str
    description: str


class KeyRequest(BaseModel):
    source: str
    key_words: str


class WBItem:
    def __init__(self, page_url: str) -> None:
        self.page_url = page_url
        self.paths = self.parse_paths()
    
    def parse_paths(self):
        pass