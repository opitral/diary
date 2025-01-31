from sqlalchemy import Integer, String, Date
from sqlalchemy.orm import mapped_column, Mapped

from pkg.database import Base


class Record(Base):
    __tablename__ = "record"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    content: Mapped[str] = mapped_column(String(4096), nullable=False)
    date: Mapped[Date] = mapped_column(Date, nullable=False)

    @property
    def short_content(self) -> str:
        if len(self.content) > 50:
            return self.content[:50] + "..."
        return self.content

    def __repr__(self):
        return f"<Record id={self.id}, content={self.short_content}, date={self.date.strftime('%Y-%m-%d')}>"
