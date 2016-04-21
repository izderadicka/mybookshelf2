from marshmallow_sqlalchemy import ModelSchema as BaseModelSchema
from marshmallow import fields, post_dump, validate
import model
from sqlalchemy import desc

sortings={'ebook':{'title': [model.Ebook.title],
                   '-title':[desc(model.Ebook.title)],
                   'created':[model.Ebook.created],
                   '-created':[desc(model.Ebook.created)],
                   }}


class ModelSchema(BaseModelSchema):
    @post_dump
    def remove_nones(self, data):
        return {
            key: value for key, value in data.items()
            if value is not None
        }

class AuthorSchema(ModelSchema):
    class Meta:
        model=model.Author
        
class SeriesSchema(ModelSchema):
    class Meta:
        model=model.Series
        
class LanguageSchema(ModelSchema):
    class Meta:
        model=model.Language
        
class GenreSchema(ModelSchema):
    class Meta:
        model=model.Genre
        
class FormatSchema(ModelSchema):
    class Meta:
        model=model.Format
        
class UserSchema(ModelSchema):
    email=fields.Email(validate=validate.Length(max=256))
    class Meta:
        model=model.User
        
class RoleSchema(ModelSchema):
    class Meta:
        model=model.Role
        
class SourceSchema(ModelSchema):
    format=fields.Function(serialize=lambda o: o.format.extension)
    class Meta:
        model=model.Source


class EbookSchema(ModelSchema):
    authors=fields.Nested(AuthorSchema, many=True, only=('id', 'first_name', 'last_name'))
    series=fields.Nested(SeriesSchema, only=('id', 'title'))
    language=fields.Function(serialize=lambda o: o.language.name)
    genres=fields.Nested(GenreSchema, many=True)
    sources=fields.Nested(SourceSchema, many=True, only=('id', 'format', 'location', 'quality','modified'))
    full_text=None
    class Meta:
        model=model.Ebook
        exclude=('full_text',)
        
    
        
ebook_serializer=EbookSchema()        
ebooks_list_serializer=EbookSchema(many=True, only=('id', 'title', 'authors', 'series', 'series_index','language','genres'))