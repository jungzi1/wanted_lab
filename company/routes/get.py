from fastapi import FastAPI, Depends, HTTPException, APIRouter, Header
from sqlalchemy.orm import Session
from company.schema import CompanyNameInfo, CompanyFullInfo
from fastapi import HTTPException
from sqlalchemy import and_, or_, func
from sqlalchemy.orm import Session
from company.models import Company, CompanyTag, Tag, CompanyName, MultiLanguageTagName


from config.database import get_db

router = APIRouter()


@router.get(
    "/search",
    status_code=200,
    summary="기업 이름 자동완성(partial matching) 검색",
    response_model=list[CompanyNameInfo],
)
def search_companies_by_name_auto_finished(
    query: str,
    x_wanted_language: str = Header(...),
    db: Session = Depends(get_db),
    offset: int = 0,
    limit: int = 50,
):
    subquery = (
        db.query(CompanyName.company_id)
        .filter(func.lower(CompanyName.name).contains(func.lower(query)))
        .subquery()
    )

    return [
        {"company_name": name}
        for name, in (
            db.query(CompanyName.name)
            .filter(
                CompanyName.company_id.in_(subquery),
                CompanyName.language_code == x_wanted_language,
            )
            .offset(offset)
            .limit(limit)
            .all()
        )
    ]


@router.get(
    "/companies/{company_name}",
    status_code=200,
    summary="기업 이름 검색(exact match)",
    response_model=CompanyFullInfo,
)
def get_company_by_name(
    company_name: str,
    x_wanted_language: str = Header(...),
    db: Session = Depends(get_db),
):
    company = (
        db.query(Company)
        .join(CompanyName)
        .filter(func.lower(CompanyName.name) == func.lower(company_name))
        .first()
    )

    if not company:
        raise HTTPException(
            status_code=404, detail=f"Company with name '{company_name}' not found"
        )

    name_in_language = (
        db.query(CompanyName.name)
        .filter(
            CompanyName.company_id == company.id,
            CompanyName.language_code == x_wanted_language,
        )
        .first()
    )

    if not name_in_language:
        name_in_language = (
            db.query(CompanyName.name)
            .filter(CompanyName.company_id == company.id)
            .first()
        )

    tags_in_language = (
        db.query(MultiLanguageTagName.name)
        .join(Tag)
        .join(CompanyTag)
        .filter(
            CompanyTag.company_id == company.id,
            MultiLanguageTagName.language_code == x_wanted_language,
        )
        .all()
    )

    return {
        "company_name": name_in_language[0],
        "tags": [tag[0] for tag in tags_in_language],
    }


@router.get(
    "/tags",
    status_code=200,
    summary="태그명으로 기업 검색",
    response_model=list[CompanyFullInfo],
)
def search_companies_by_tag(
    query: str, x_wanted_language: str = Header(...), db: Session = Depends(get_db)
):
    matching_tags = (
        db.query(Tag.id)
        .join(MultiLanguageTagName)
        .filter(func.lower(MultiLanguageTagName.name) == func.lower(query))
        .all()
    )

    if not matching_tags:
        return []

    tag_ids = [tag_id[0] for tag_id in matching_tags]

    companies = (
        db.query(Company)
        .join(Company.tags)
        .filter(Tag.id.in_(tag_ids))
        .distinct()
        .all()
    )

    if not companies:
        return []

    results = []
    for company in companies:
        name_in_language = next(
            (
                name.name
                for name in company.names
                if name.language_code == x_wanted_language
            ),
            None,
        )

        fallback_name = next((name.name for name in company.names), None)

        tags_in_language = [
            tag_name.name
            for tag in company.tags
            for tag_name in tag.multi_language_names
            if tag_name.language_code == x_wanted_language
        ]

        results.append(
            CompanyFullInfo(
                company_name=name_in_language or fallback_name, tags=tags_in_language
            )
        )

    return results
