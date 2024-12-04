from fastapi import Depends, HTTPException, APIRouter, Header
from sqlalchemy.orm import Session

from company.models import Company, MultiLanguageTagName, CompanyTag, Tag, CompanyName
from company.schema import TagCreate, CompanyFullInfo
from config.database import get_db

router = APIRouter()


@router.delete(
    "/companies/{company_name}/tags/{tag_name}",
    status_code=200,
    response_model=CompanyFullInfo,
)
def delete_company_tag(
    company_name: str,
    tag_name: str,
    x_wanted_language: str = Header(...),
    db: Session = Depends(get_db),
):
    company = db.query(Company).filter(Company.main_name == company_name).first()
    if not company:
        raise HTTPException(
            status_code=404, detail=f"Company '{company_name}' not found"
        )

    tag = (
        db.query(Tag)
        .join(MultiLanguageTagName)
        .filter(MultiLanguageTagName.name == tag_name)
        .first()
    )
    if not tag:
        raise HTTPException(status_code=404, detail=f"Tag '{tag_name}' not found")

    db.query(Tag).filter(Tag.id == tag.id).delete()
    db.flush()

    db.commit()

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
