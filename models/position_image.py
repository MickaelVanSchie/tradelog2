import uuid

from sqlalchemy import Column, UUID, Text, ForeignKey
from sqlalchemy.orm import relationship

from consts.position_consts import ImageType, ImageExtension
from models import Base


class PositionImage(Base):
    __tablename__ = "position_image"
    id: uuid.UUID = Column(UUID(as_uuid=True), primary_key=True)
    position_id: uuid.UUID = Column(UUID(as_uuid=True), ForeignKey("position.id"))
    type: ImageType = Column(Text, nullable=False)
    extension: ImageExtension = Column(Text, nullable=False)

    position = relationship('Position', back_populates='images')