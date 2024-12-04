from fastapi import Depends, HTTPException, APIRouter, Header
from sqlalchemy.orm import Session

from company.models import Company, CompanyName, MultiLanguageTagName, CompanyTag, Tag
from company.schema import CompanyFullInfo, CompanyCreate

from config.database import get_db

router = APIRouter()


def require_name(obj: dict, language: str = "ko"):
    return obj.get(language) or list(obj.values())[0]


@router.post(
    "/companies",
    status_code=200,
    summary="기업(태그) 생성",
    response_model=CompanyFullInfo,
)
def add_company(
    body: CompanyCreate,
    x_wanted_language: str = Header(...),
    db: Session = Depends(get_db),
):
    new_company = Company(main_name=require_name(body.company_name))
    db.add(new_company)
    db.flush()

    for lang_code, name in body.company_name.items():
        db.add(
            CompanyName(company_id=new_company.id, language_code=lang_code, name=name)
        )

    for tag_data in body.tags:
        new_tag = Tag(main_name=require_name(tag_data.tag_name))
        db.add(new_tag)
        db.flush()

        for lang_code, tag_name in tag_data.tag_name.items():
            db.add(
                MultiLanguageTagName(
                    tag_id=new_tag.id, language_code=lang_code, name=tag_name
                )
            )

        db.add(CompanyTag(company_id=new_company.id, tag_id=new_tag.id))

    db.commit()

    return {
        "company_name": require_name(body.company_name, x_wanted_language),
        "tags": [
            tag.tag_name[x_wanted_language]
            for tag in body.tags
            if x_wanted_language in tag.tag_name
        ],
    }
