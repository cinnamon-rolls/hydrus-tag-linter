from argparse import Namespace
from flask.app import Flask
from flask_sqlalchemy import SQLAlchemy
from tag_linter.hydrus_util import clean_tag


def create_models(app: Flask, db: SQLAlchemy):
    "Creates all the models and utility functions"

    def get_first(ModelClass, **kwargs):
        return ModelClass.query.filter_by(**kwargs).first()

    def get_or_create(ModelClass, **kwargs):
        found = get_first(ModelClass, **kwargs)
        if found:
            return found

        print("new instance of " + str(ModelClass) + ": " + str(kwargs))
        new_instance = ModelClass(**kwargs)
        try:
            db.session.add(new_instance)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise Exception("Failed to create instance") from e

        return new_instance

    def remove_if_present(ModelClass, **kwargs):
        found = get_first(ModelClass, **kwargs)
        if found is None:
            return False
        try:
            db.session.delete(found)
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            raise Exception("Failed to delete instance") from e

    class Tag(db.Model):
        __tablename__ = "tags"
        _id = db.Column("id", db.Integer, primary_key=True)
        tag_name = db.Column(db.String(1024), unique=True)

        def __init__(self, tag_name):
            super().__init__()
            if not isinstance(tag_name, str):
                raise ValueError("Expected a string, got: " + str(tag_name))
            self.tag_name = clean_tag(tag_name)

        @classmethod
        def get(cls, tag_name):
            return get_first(cls, tag_name=tag_name)

        @classmethod
        def get_or_create(cls, tag_name):
            return get_or_create(cls, tag_name=tag_name)

        @classmethod
        def get_id(cls, tag_name):
            return cls.get_or_create(tag_name)._id

    class SoftParentRelation(db.Model):
        __tablename__ = "soft_parents"
        _id = db.Column("id", db.Integer, primary_key=True)
        parent_id = db.Column(db.Integer)
        child_id = db.Column(db.Integer)

        def __init__(self, parent_id, child_id):
            self.parent_id = parent_id
            self.child_id = child_id

        @classmethod
        def get(cls, parent_id, child_id):
            return cls.query.filter_by(parent_id=parent_id, child_id=child_id).first()

        @classmethod
        def ensure(cls, parent_tag_name, child_tag_name):
            parent_id = Tag.get_id(parent_tag_name)
            child_id = Tag.get_id(child_tag_name)
            get_or_create(cls, parent_id=parent_id, child_id=child_id)

        @classmethod
        def remove(cls, parent_tag_name, child_tag_name):
            parent_id = Tag.get_id(parent_tag_name)
            child_id = Tag.get_id(child_tag_name)
            found = cls.get(parent_id, child_id)
            if found is not None:
                db.session.delete(found)
                db.session.commit()

    return Namespace(Tag=Tag, SoftParentRelation=SoftParentRelation)
