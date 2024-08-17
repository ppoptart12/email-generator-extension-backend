from langchain_core.pydantic_v1 import BaseModel, Field


class email_schema(BaseModel):
    email_body: str = Field(description="The body of the email")
    email_subject: str = Field(description="The subject line of the email")
