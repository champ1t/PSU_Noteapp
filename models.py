from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import sqlalchemy as sa
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy.sql import func
from typing import List, Optional
from datetime import datetime

class Base(DeclarativeBase):
    """Base class for all database models"""
    pass

# Initialize SQLAlchemy with custom model class
db = SQLAlchemy(model_class=Base)

def init_app(app: Flask):
    """Initialize the database with Flask application"""
    db.init_app(app)
    
    with app.app_context():
        # Create all database tables
        db.create_all()
        
        # Reflect database schema
        db.reflect()

# Many-to-many relationship table with additional metadata
note_tag_association = db.Table(
    "note_tag",
    sa.Column("note_id", sa.Integer, sa.ForeignKey("notes.id"), primary_key=True, index=True),
    sa.Column("tag_id", sa.Integer, sa.ForeignKey("tags.id"), primary_key=True, index=True),
    sa.Column("created_at", sa.DateTime(timezone=True), server_default=func.now()),
    sa.Column("modified_at", sa.DateTime(timezone=True), server_default=func.now(), onupdate=func.now()),
    sa.Index('idx_note_tag', 'note_id', 'tag_id', unique=True)
)

class Tag(db.Model):
    """Tag model for categorizing notes"""
    __tablename__ = "tags"
    __table_args__ = (
        sa.UniqueConstraint('name', name='uq_tag_name'),
    )

    id: Mapped[int] = mapped_column(sa.Integer, primary_key=True)
    name: Mapped[str] = mapped_column(
        sa.String(50), 
        nullable=False,
        index=True,
        doc="Name of the tag (must be unique)"
    )
    description: Mapped[Optional[str]] = mapped_column(
        sa.Text,
        doc="Optional description for the tag"
    )
    
    # Timestamps with timezone
    created_at: Mapped[datetime] = mapped_column(
        sa.DateTime(timezone=True), 
        server_default=func.now(),
        doc="Timestamp when tag was created"
    )
    updated_at: Mapped[datetime] = mapped_column(
        sa.DateTime(timezone=True), 
        server_default=func.now(),
        onupdate=func.now(),
        doc="Timestamp when tag was last updated"
    )

    # Relationship configuration
    notes: Mapped[List["Note"]] = relationship(
        secondary=note_tag_association, 
        back_populates="tags",
        lazy="dynamic",
        doc="Notes associated with this tag"
    )

    def __repr__(self):
        return f"<Tag(id={self.id}, name='{self.name}')>"

class Note(db.Model):
    """Note model for storing user content"""
    __tablename__ = "notes"
    __table_args__ = (
        sa.Index('idx_note_title', 'title'),
    )

    id: Mapped[int] = mapped_column(sa.Integer, primary_key=True)
    title: Mapped[str] = mapped_column(
        sa.String(100), 
        nullable=False,
        index=True,
        doc="Title of the note"
    )
    content: Mapped[Optional[str]] = mapped_column(
        sa.Text,
        doc="Main content of the note"
    )
    is_pinned: Mapped[bool] = mapped_column(
        sa.Boolean,
        default=False,
        server_default="false",
        doc="Whether the note is pinned for quick access"
    )
    is_archived: Mapped[bool] = mapped_column(
        sa.Boolean,
        default=False,
        server_default="false",
        doc="Whether the note is archived"
    )
    
    # Timestamps with timezone
    created_at: Mapped[datetime] = mapped_column(
        sa.DateTime(timezone=True), 
        server_default=func.now(),
        doc="Timestamp when note was created"
    )
    updated_at: Mapped[datetime] = mapped_column(
        sa.DateTime(timezone=True), 
        server_default=func.now(),
        onupdate=func.now(),
        doc="Timestamp when note was last updated"
    )

    # Relationship configuration
    tags: Mapped[List[Tag]] = relationship(
        secondary=note_tag_association,
        back_populates="notes",
        lazy="dynamic",
        doc="Tags associated with this note"
    )

    def __repr__(self):
        return f"<Note(id={self.id}, title='{self.title}')>"