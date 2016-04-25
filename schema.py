from marshmallow_sqlalchemy import ModelSchema as BaseModelSchema
from flask_marshmallow import Marshmallow
from marshmallow import fields, post_dump, validate
import model
from sqlalchemy import desc

schema=Marshmallow()

BaseModelSchema=schema.ModelSchema

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
        
    class Meta:
        sqla_session=model.db.session
        
           

class AuthorSchema(ModelSchema):
    class Meta:
        model=model.Author
        
class SeriesSchema(ModelSchema):
    class Meta:
        model=model.Series
        
class LanguageSchema(ModelSchema):
    class Meta:
        model=model.Language
        exclude=('version_id',)
        
class GenreSchema(ModelSchema):
    class Meta:
        model=model.Genre
        exclude=('version_id',)
        
class FormatSchema(ModelSchema):
    class Meta:
        model=model.Format
        exclude=('version_id',)
        
class UserSchema(ModelSchema):
    email=fields.Email(validate=validate.Length(max=256))
    class Meta:
        model=model.User
        
class RoleSchema(ModelSchema):
    class Meta:
        model=model.Role
        exclude=('version_id',)
        
class SourceSchema(ModelSchema):
    format=fields.Function(serialize=lambda o: o.format.extension)
    class Meta:
        model=model.Source
        


class EbookSchema(ModelSchema):
    authors=fields.Nested(AuthorSchema, many=True, only=('id', 'first_name', 'last_name'))
    series=fields.Nested(SeriesSchema, only=('id', 'title'))
    language=fields.Function(serialize=lambda o: o.language.name, deserialize=lambda x: model.Language())
    genres=fields.Nested(GenreSchema, many=True)
    sources=fields.Nested(SourceSchema, many=True, only=('id', 'format', 'location', 'quality','modified'))
    full_text=None
    class Meta:
        model=model.Ebook
        exclude=('full_text',)
        
    
        
ebook_serializer=EbookSchema()  
ebook_deserializer_update=EbookSchema()    
ebook_deserializer_insert=EbookSchema(exclude=('version_id',))      
ebooks_list_serializer=EbookSchema(many=True, only=('id', 'title', 'authors', 'series', 'series_index','language','genres'))