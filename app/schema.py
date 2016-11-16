import app
from copy import deepcopy
from flask_marshmallow import Marshmallow
from marshmallow import fields, post_dump, validate, Schema, post_load
import app.model as model


schema = Marshmallow(app.app)

BaseModelSchema = schema.ModelSchema

def PartialSchemaFactory(schema_cls, **kwargs):
    schema = schema_cls(**kwargs)
    for field_name, field in schema.fields.items():
        if isinstance(field, fields.Nested):
            new_field = deepcopy(field)
            new_field.schema.partial = True
            schema.fields[field_name] = new_field
    return schema


class ModelSchema(BaseModelSchema):

    @post_dump
    def remove_nones(self, data):
        return {
            key: value for key, value in data.items()
            if value is not None
        }

    class Meta:
        sqla_session = app.db.session
        
    @classmethod
    def create_entity_serializer(cls):
        return cls()
    
    @classmethod
    def create_insert_serializer(cls):
        return cls(exclude=('version_id',))
    
    @classmethod
    def create_list_serializer(cls):
        return cls(many=True)
    
    @classmethod
    def create_index_serializer(cls):
        return cls(many=True)
    
    @classmethod
    def create_update_serializer(cls):
        return cls(partial=True)


class AuthorSchema(ModelSchema):

    class Meta:
        model = model.Author
        
    @classmethod
    def create_list_serializer(cls):
        return AuthorSchema(
            many=True, only=('id', 'first_name', 'last_name'))


class SeriesSchema(ModelSchema):
    authors = fields.Nested(
        AuthorSchema, many=True, only=('id', 'first_name', 'last_name'))
    class Meta:
        model = model.Series
        
    @classmethod
    def create_index_serializer(cls):
        return cls(many=True, only=('id', 'title', 'authors'))

class LanguageSchema(ModelSchema):

    class Meta:
        model = model.Language
        exclude = ('version_id',)


class GenreSchema(ModelSchema):

    class Meta:
        model = model.Genre
        exclude = ('version_id',)
        
class ConversionSchema(ModelSchema):
    format = fields.Function(serialize=lambda o: o.format.extension)
    class Meta:
        model = model.Conversion
        exclude = ('version_id',)


class FormatSchema(ModelSchema):

    class Meta:
        model = model.Format
        exclude = ('version_id',)


class UserSchema(ModelSchema):
    email = fields.Email(validate=validate.Length(max=256))

    class Meta:
        model = model.User


class RoleSchema(ModelSchema):

    class Meta:
        model = model.Role
        exclude = ('version_id',)


class UploadSchema(ModelSchema):
    cover = fields.Function(serialize=lambda o: bool(o.cover))
    class Meta:
        model = model.Upload
        exclude = ('version_id',)


class SourceSchema(ModelSchema):
    format = fields.Function(serialize=lambda o: o.format.extension)

    class Meta:
        model = model.Source




class EbookSchema(ModelSchema):
    authors = fields.Nested(
        AuthorSchema, many=True, only=('id', 'first_name', 'last_name'), allow_none=True)
    series = fields.Nested(SeriesSchema, only=('id', 'title'), allow_none=True)
    language = fields.Nested(LanguageSchema, required=True)
    cover = fields.Function(serialize=lambda o: bool(o.cover))
    genres = fields.Nested(GenreSchema, many=True, allow_none=True)
    sources = fields.Nested(SourceSchema, many=True, only=(
        'id', 'format', 'location', 'quality', 'modified', 'size', 'created_by'), allow_none=True)
    full_text = None

    class Meta:
        model = model.Ebook
        exclude = ('full_text', 'base_dir')
        
    @classmethod
    def create_insert_serializer(cls):
        return PartialSchemaFactory(EbookSchema, exclude=('version_id',))
    
    @classmethod
    def create_list_serializer(cls):
        return EbookSchema(many=True, only=(
            'id', 'title', 'authors', 'series', 'series_index', 'language', 'cover'))
        
    @classmethod
    def create_update_serializer(cls):
        return PartialSchemaFactory(EbookSchema, partial=True)
    

class FileInfoSchema(Schema):
    mime_type = fields.String(required=True, validate=validate.Length(max=255))
    size = fields.Integer(required=True, validate=validate.Range(min=1))
    # hash = fields.String(validate=validate.Length(max=128))
    
class BookshelfSchema(ModelSchema):
    items_count = fields.Function(serialize = lambda o: o.items_count)
    class Meta:
        model = model.Bookshelf
        
    @classmethod
    def create_list_serializer(cls):
        return cls(many=True, only=('id', 'name', 'description', 'items_count'))
    
    @classmethod
    def create_index_serializer(cls):
        return cls(many=True, only=('id','name',))

        
class BookshelfItemSchema(ModelSchema):
    class Meta:
        model = model.BookshelfItem
