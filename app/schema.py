import app
from marshmallow_sqlalchemy import ModelSchema as BaseModelSchema
from flask_marshmallow import Marshmallow
from marshmallow import fields, post_dump, validate
import app.model as model
from sqlalchemy import desc

schema=Marshmallow(app.app)

BaseModelSchema=schema.ModelSchema

class ModelSchema(BaseModelSchema):
    @post_dump
    def remove_nones(self, data):
        return {
            key: value for key, value in data.items()
            if value is not None
        }
        
    class Meta:
        sqla_session=app.db.session
        
           

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
        

def lang_from_code(c):
        return model.Language.query.filter_by(code=c).one()
class EbookSchema(ModelSchema):
    authors=fields.Nested(AuthorSchema, many=True, only=('id', 'first_name', 'last_name'))
    series=fields.Nested(SeriesSchema, only=('id', 'title'))
    language=fields.Function(serialize=lambda o: o.language.name, deserialize=lang_from_code)
    genres=fields.Nested(GenreSchema, many=True)
    sources=fields.Nested(SourceSchema, many=True, only=('id', 'format', 'location', 'quality','modified', 'size'))
    full_text=None
    class Meta:
        model=model.Ebook
        exclude=('full_text',)
        
    
#schemas are probably not thread safe, better to have new instance per each use        
ebook_serializer=lambda: EbookSchema()  
ebook_deserializer_update=lambda: EbookSchema()    
ebook_deserializer_insert=lambda: EbookSchema(exclude=('version_id',))      
ebooks_list_serializer=lambda: EbookSchema(many=True, only=('id', 'title', 'authors', 'series', 'series_index','language','genres'))

authors_list_serializer=lambda: AuthorSchema(many=True, only=('id', 'first_name', 'last_name'))
series_list_serializer=lambda: SeriesSchema(many=True, only=('id', 'title'))