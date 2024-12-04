from fastapi import Depends, HTTPException, APIRouter, Header
from sqlalchemy.orm import Session

from company.models import Company, MultiLanguageTagName, CompanyTag, Tag, CompanyName
from company.schema import TagCreate, CompanyFullInfo
from config.database import get_db

router = APIRouter()


@router.put(
    "/companies/{company_name}/tags", status_code=200, response_model=CompanyFullInfo
)
def update_company_tags(
    company_name: str,
    tags: list[TagCreate],
    x_wanted_language: str = Header(...),
    db: Session = Depends(get_db),
):
    company = db.query(Company).filter(Company.main_name == company_name).first()
    if not company:
        raise HTTPException(
            status_code=404, detail=f"Company '{company_name}' not found"
        )

    current_tags = (
        db.query(Tag)
        .join(CompanyTag, CompanyTag.tag_id == Tag.id)
        .filter(CompanyTag.company_id == company.id)
        .all()
    )

    current_tag_names = {
        tag_name.name: tag
        for tag in current_tags
        for tag_name in tag.multi_language_names
        if tag_name.language_code == x_wanted_language
    }

    for tag_input in tags:
        tag_name_in_requested_language = tag_input.tag_name.get(x_wanted_language)
        if not tag_name_in_requested_language:
            raise HTTPException(
                status_code=400, detail="Requested language tag name is missing"
            )

        if tag_name_in_requested_language in current_tag_names:
            existing_tag = current_tag_names[tag_name_in_requested_language]

            db.query(MultiLanguageTagName).filter(
                MultiLanguageTagName.tag_id == existing_tag.id
            ).delete()
            db.flush()

            for lang_code, name in tag_input.tag_name.items():
                db.add(
                    MultiLanguageTagName(
                        tag_id=existing_tag.id,
                        name=name,
                        language_code=lang_code,
                    )
                )
        else:
            new_tag = Tag(main_name=tag_name_in_requested_language)
            db.add(new_tag)
            db.flush()

            for lang_code, name in tag_input.tag_name.items():
                db.add(
                    MultiLanguageTagName(
                        tag_id=new_tag.id,
                        name=name,
                        language_code=lang_code,
                    )
                )

            db.add(CompanyTag(company_id=company.id, tag_id=new_tag.id))

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

    updated_tags = (
        db.query(MultiLanguageTagName.name)
        .join(Tag)
        .join(CompanyTag, CompanyTag.tag_id == Tag.id)
        .filter(
            CompanyTag.company_id == company.id,
            MultiLanguageTagName.language_code == x_wanted_language,
        )
        .all()
    )

    return {
        "company_name": name_in_language[0],
        "tags": sorted(
            [tag[0] for tag in updated_tags], key=lambda x: int(x.split("_")[-1])
        ),
    }
