from pydantic import BaseModel


class SummaryResponseSchema(BaseModel):
    summary_text: str
    context_text: str
