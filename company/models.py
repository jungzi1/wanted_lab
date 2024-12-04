from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import mapped_column, relationship

from config.database import Base


class CompanyTag(Base):
    __tablename__ = "company_tags"
    id = mapped_column(Integer, primary_key=True, autoincrement=True)
    company_id = mapped_column(Integer, ForeignKey("companies.id", ondelete="CASCADE"))
    tag_id = mapped_column(Integer, ForeignKey("tags.id", ondelete="CASCADE"))


class Company(Base):
    __tablename__ = "companies"

    id = mapped_column(Integer, primary_key=True, autoincrement=True)
    main_name = mapped_column(String(255), nullable=False)

    names = relationship(
        "CompanyName", back_populates="company", cascade="all, delete-orphan"
    )

    tags = relationship("Tag", secondary="company_tags", back_populates="companies")


class CompanyName(Base):
    __tablename__ = "company_names"

    id = mapped_column(Integer, primary_key=True, autoincrement=True)
    language_code = mapped_column(String(10), nullable=False)
    name = mapped_column(String(255), nullable=False)
    company_id = mapped_column(
        Integer, ForeignKey("companies.id", ondelete="CASCADE"), nullable=False
    )

    company = relationship("Company", back_populates="names")


class Tag(Base):
    __tablename__ = "tags"

    id = mapped_column(Integer, primary_key=True, autoincrement=True)
    main_name = mapped_column(String(255), nullable=False)

    multi_language_names = relationship(
        "MultiLanguageTagName", back_populates="tag", cascade="all, delete-orphan"
    )

    companies = relationship("Company", secondary="company_tags", back_populates="tags")


class MultiLanguageTagName(Base):
    __tablename__ = "multi_language_tag_names"

    id = mapped_column(Integer, primary_key=True, autoincrement=True)
    name = mapped_column(String(255), nullable=False)
    language_code = mapped_column(String(10), nullable=False)
    tag_id = mapped_column(
        Integer, ForeignKey("tags.id", ondelete="CASCADE"), nullable=False
    )

    tag = relationship("Tag", back_populates="multi_language_names")
