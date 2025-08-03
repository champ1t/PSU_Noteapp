from flask_wtf import FlaskForm
from wtforms import (
    StringField, SubmitField, 
    TextAreaField, SelectMultipleField,
    BooleanField, HiddenField
)
from wtforms.validators import DataRequired, Optional, Length
from datetime import datetime
from typing import List

class TagListField(StringField):
    """Custom field for handling comma-separated tags"""
    def process_formdata(self, valuelist):
        if valuelist:
            # Split by comma, strip whitespace, and remove empty strings
            self.data = [tag.strip() for tag in valuelist[0].split(",") if tag.strip()]
        else:
            self.data = []

    def _value(self):
        """Convert list back to comma-separated string"""
        return ", ".join(self.data) if self.data else ""

class NoteForm(FlaskForm):
    """Form for creating and editing notes"""
    title = StringField(
        'Title',
        validators=[
            DataRequired(message="Title is required"),
            Length(max=100, message="Title cannot exceed 100 characters")
        ]
    )
    content = TextAreaField(
        'Content',
        validators=[Optional()]
    )
    tags = TagListField(
        'Tags',
        description="Comma-separated list of tags (max 50 chars each)",
        validators=[
            Optional(),
            Length(max=500, message="Total tags length cannot exceed 500 characters")
        ]
    )
    is_pinned = BooleanField(
        'Pin this note',
        default=False
    )
    submit = SubmitField('Save Note')
    cancel = SubmitField('Cancel', render_kw={'formnovalidate': True})

class EditNoteForm(NoteForm):
    """Form for editing existing notes"""
    id = HiddenField()
    updated_at = StringField(
        'Last Updated', 
        render_kw={'readonly': True}
    )
    submit = SubmitField('Update Note')

class DeleteNoteForm(FlaskForm):
    """Form for note deletion confirmation"""
    id = HiddenField()
    confirm = SubmitField('Confirm Delete', render_kw={'class': 'btn-danger'})
    cancel = SubmitField('Cancel', render_kw={'formnovalidate': True})

class TagForm(FlaskForm):
    """Form for creating and editing tags"""
    id = HiddenField()
    name = StringField(
        'Tag Name', 
        validators=[
            DataRequired(message="Tag name is required"),
            Length(min=2, max=50, message="Tag must be between 2-50 characters")
        ],
        render_kw={"placeholder": "Enter tag name"}
    )
    description = TextAreaField(
        'Description',
        validators=[Optional(), Length(max=200)],
        render_kw={"placeholder": "Optional description"}
    )
    submit = SubmitField('Save Tag')
    cancel = SubmitField('Cancel', render_kw={'formnovalidate': True})

class DeleteTagForm(FlaskForm):
    """Form for tag deletion confirmation"""
    id = HiddenField()
    confirm = SubmitField('Confirm Delete', render_kw={'class': 'btn-danger'})
    cancel = SubmitField('Cancel', render_kw={'formnovalidate': True})

class NoteSearchForm(FlaskForm):
    """Form for searching notes"""
    query = StringField(
        'Search',
        validators=[Optional()],
        render_kw={"placeholder": "Search notes..."}
    )
    tag = SelectMultipleField(
        'Filter by Tag',
        coerce=int,
        validators=[Optional()]
    )
    pinned_only = BooleanField('Pinned Only')
    submit = SubmitField('Search')