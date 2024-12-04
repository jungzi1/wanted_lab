import csv
from sqlalchemy.orm import Session

from company.models import (
    Base,
    Company,
    CompanyName,
    CompanyTag,
    Tag,
    MultiLanguageTagName,
)
from config.database import engine, SessionLocal

Base.metadata.create_all(bind=engine)

file_path = "./company_tag_sample.csv"


def save_csv_to_db(file_path: str, db: Session):
    with open(file_path, "r", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)

        for row in reader:
            company_main_name = (
                row.get("company_ko") or row.get("company_en") or row.get("company_ja")
            )
            if not company_main_name:
                continue

            company = Company(main_name=company_main_name)
            db.add(company)
            db.flush()

            for column_name, language_code in [
                ("company_ko", "ko"),
                ("company_en", "en"),
                ("company_ja", "ja"),
            ]:
                name = row.get(column_name)
                if name:
                    db.add(
                        CompanyName(
                            company_id=company.id,
                            name=name,
                            language_code=language_code,
                        )
                    )

            tag_ids = set()
            for column_name, language_code in [
                ("tag_ko", "ko"),
                ("tag_en", "en"),
                ("tag_ja", "jp"),
            ]:
                tag_data = row.get(column_name)
                if tag_data:
                    tags = tag_data.split("|")
                    for tag in tags:
                        try:
                            main_name = tag.split("_")[-1]
                        except IndexError:
                            continue

                        tag_entity = (
                            db.query(Tag)
                            .filter(Tag.main_name == main_name)
                            .one_or_none()
                        )
                        if not tag_entity:
                            tag_entity = Tag(main_name=main_name)
                            db.add(tag_entity)
                            db.flush()

                        tag_ids.add(tag_entity.id)

                        existing_ml_tag = (
                            db.query(MultiLanguageTagName)
                            .filter(
                                MultiLanguageTagName.tag_id == tag_entity.id,
                                MultiLanguageTagName.name == tag,
                                MultiLanguageTagName.language_code == language_code,
                            )
                            .one_or_none()
                        )
                        if not existing_ml_tag:
                            db.add(
                                MultiLanguageTagName(
                                    tag_id=tag_entity.id,
                                    name=tag,
                                    language_code=language_code,
                                )
                            )

            for tag_id in tag_ids:
                existing_company_tag = (
                    db.query(CompanyTag)
                    .filter(
                        CompanyTag.company_id == company.id, CompanyTag.tag_id == tag_id
                    )
                    .one_or_none()
                )
                if not existing_company_tag:
                    db.add(CompanyTag(company_id=company.id, tag_id=tag_id))

        db.commit()


if __name__ == "__main__":
    db = SessionLocal()
    try:
        save_csv_to_db(file_path, db)
        print("Data has been successfully saved to the database.")
    except Exception as e:
        db.rollback()
        print(f"An error occurred: {e}")
    finally:
        db.close()
