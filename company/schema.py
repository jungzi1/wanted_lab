from pydantic import BaseModel, field_validator, ValidationError


class CompanyNameInfo(BaseModel):
    company_name: str


class CompanyFullInfo(CompanyNameInfo):
    tags: list[str]


class TagCreate(BaseModel):
    tag_name: dict[str, str]


class CompanyCreate(BaseModel):
    company_name: dict[str, str]
    tags: list[TagCreate]

    @field_validator("company_name")
    def check_non_empty_company_name(cls, company_name):
        if not company_name or len(company_name) == 0:
            raise ValueError("company_name must not be an empty dictionary.")
        return company_name
