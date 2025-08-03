import os
from datetime import datetime
from flask import Flask, render_template, redirect, url_for, flash, request
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, BooleanField
from wtforms.validators import DataRequired
from sqlalchemy.exc import SQLAlchemyError

# Initialize Flask app
app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY") or "dev-secret-key-12345"
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://coe:CoEpasswd@localhost:5432/coedb"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["TEMPLATES_AUTO_RELOAD"] = True

db = SQLAlchemy(app)

# Database Models
note_tags = db.Table('note_tags',
    db.Column('note_id', db.Integer, db.ForeignKey('notes.id'), primary_key=True),
    db.Column('tag_id', db.Integer, db.ForeignKey('tags.id'), primary_key=True)
)

class Tag(db.Model):
    __tablename__ = 'tags'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    notes = db.relationship('Note', secondary=note_tags, backref='tags')

    # เพิ่มเมธอดนี้เพื่อนับจำนวนโน้ต
    def notes_count(self):
        return len(self.notes)

class Note(db.Model):
    __tablename__ = 'notes'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    is_pinned = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

# Forms
class NoteForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    content = TextAreaField('Content', validators=[DataRequired()])
    tags = StringField('Tags (comma separated)')
    is_pinned = BooleanField('Pin this note')

class TagForm(FlaskForm):
    name = StringField('Tag Name', validators=[DataRequired()])

# Context Processor
@app.context_processor
def inject_now():
    return {'now': datetime.utcnow()}

# Routes
@app.route("/")
def index():
    try:
        notes = Note.query.order_by(
            Note.is_pinned.desc(), 
            Note.updated_at.desc()
        ).all()
        return render_template("index.html", notes=notes)
    except SQLAlchemyError as e:
        flash("Database error occurred", "danger")
        return render_template("index.html", notes=[])

@app.route("/notes/create", methods=["GET", "POST"])
def notes_create():
    form = NoteForm()
    all_tags = Tag.query.all()
    
    if form.validate_on_submit():
        try:
            note = Note(
                title=form.title.data.strip(),
                content=form.content.data.strip(),
                is_pinned=form.is_pinned.data
            )
            
            if form.tags.data:
                tag_names = [t.strip().lower() for t in form.tags.data.split(",") if t.strip()]
                for tag_name in tag_names:
                    tag = Tag.query.filter_by(name=tag_name).first()
                    if not tag:
                        tag = Tag(name=tag_name)
                        db.session.add(tag)
                    note.tags.append(tag)
            
            db.session.add(note)
            db.session.commit()
            flash("Note created successfully!", "success")
            return redirect(url_for("index"))
        except SQLAlchemyError as e:
            db.session.rollback()
            flash(f"Error creating note: {str(e)}", "danger")
    
    return render_template("notes/create.html", form=form, all_tags=all_tags)

@app.route("/notes/<int:note_id>")
def note_detail(note_id):
    note = Note.query.get_or_404(note_id)
    return render_template("notes/detail.html", note=note)

@app.route("/notes/<int:note_id>/edit", methods=["GET", "POST"])
def note_edit(note_id):
    note = Note.query.get_or_404(note_id)
    form = NoteForm(obj=note)
    all_tags = Tag.query.all()
    
    if form.validate_on_submit():
        try:
            note.title = form.title.data.strip()
            note.content = form.content.data.strip()
            note.is_pinned = form.is_pinned.data
            
            note.tags = []
            if form.tags.data:
                tag_names = [t.strip().lower() for t in form.tags.data.split(",") if t.strip()]
                for tag_name in tag_names:
                    tag = Tag.query.filter_by(name=tag_name).first()
                    if not tag:
                        tag = Tag(name=tag_name)
                        db.session.add(tag)
                    note.tags.append(tag)
            
            db.session.commit()
            flash("Note updated successfully!", "success")
            return redirect(url_for("note_detail", note_id=note.id))
        except SQLAlchemyError as e:
            db.session.rollback()
            flash(f"Error updating note: {str(e)}", "danger")
    
    form.tags.data = ", ".join([tag.name for tag in note.tags])
    return render_template("notes/edit.html", form=form, note=note, all_tags=all_tags)

@app.route("/notes/<int:note_id>/delete", methods=["POST"])
def note_delete(note_id):
    note = Note.query.get_or_404(note_id)
    try:
        db.session.delete(note)
        db.session.commit()
        flash("Note deleted successfully!", "success")
    except SQLAlchemyError as e:
        db.session.rollback()
        flash(f"Error deleting note: {str(e)}", "danger")
    return redirect(url_for("index"))

# Tag Management
@app.route("/tags")
def tags_list():
    tags = Tag.query.all()
    form = TagForm()
    return render_template("tags/list.html", tags=tags, form=form)

@app.route("/tags/add", methods=["POST"])
def tag_add():
    form = TagForm()
    if form.validate_on_submit():
        try:
            tag_name = form.name.data.strip().lower()
            existing_tag = Tag.query.filter_by(name=tag_name).first()
            if existing_tag:
                flash("Tag already exists!", "info")
            else:
                tag = Tag(name=tag_name)
                db.session.add(tag)
                db.session.commit()
                flash("Tag added successfully!", "success")
        except SQLAlchemyError as e:
            db.session.rollback()
            flash(f"Error adding tag: {str(e)}", "danger")
    return redirect(url_for("tags_list"))

@app.route("/tags/<int:tag_id>/edit", methods=["GET", "POST"])
def tag_edit(tag_id):
    tag = Tag.query.get_or_404(tag_id)
    form = TagForm()
    
    if request.method == "POST":
        if form.validate_on_submit():
            try:
                tag.name = form.name.data.strip().lower()
                db.session.commit()
                flash("Tag updated successfully!", "success")
                return redirect(url_for("tags_list"))
            except SQLAlchemyError as e:
                db.session.rollback()
                flash(f"Error updating tag: {str(e)}", "danger")
    
    # สำหรับ GET request
    form.name.data = tag.name
    return render_template("tags/edit.html", form=form, tag=tag)

@app.route("/tags/<int:tag_id>/delete", methods=["POST"])
def tag_delete(tag_id):
    tag = Tag.query.get_or_404(tag_id)
    try:
        db.session.execute(
            note_tags.delete().where(note_tags.c.tag_id == tag_id)
        )
        db.session.delete(tag)
        db.session.commit()
        flash("Tag deleted successfully!", "success")
    except SQLAlchemyError as e:
        db.session.rollback()
        flash(f"Error deleting tag: {str(e)}", "danger")
    return redirect(url_for("tags_list"))

@app.route("/tags/<int:tag_id>/notes")
def notes_by_tag(tag_id):
    tag = Tag.query.get_or_404(tag_id)
    notes = Note.query.join(note_tags).filter(note_tags.c.tag_id == tag.id).order_by(
        Note.is_pinned.desc(), 
        Note.updated_at.desc()
    ).all()
    return render_template("index.html", notes=notes, title=f"Notes tagged with '{tag.name}'")

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)