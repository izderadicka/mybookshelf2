# coding: utf-8
import app
from sqlalchemy import Column, Date, DateTime, Float, Index, Integer, SmallInteger, String, \
    BigInteger, Boolean, ForeignKey, Text, Enum, Table, desc
from sqlalchemy.ext.declarative import declarative_base,declared_attr
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship, deferred, backref
from flask.ext.login import UserMixin
from sqlalchemy_utils import TSVectorType
from app.utils import initials



class Base(app.db.Model):
    __abstract__=True

    id =  Column(BigInteger, primary_key=True)
    version_id = Column("version_id", Integer, nullable=False)

    __mapper_args__ = {
        'version_id_col': version_id,
    }
    
    def __repr__(self, attrs=None):
        base= '<%s id=%s' % (self.__class__.__name__, self.id)
        if attrs:
            base+=' '+' '.join(['%s="%s"'%(a, getattr(self,a)) for a in attrs])
        return base +'>'

#Base = declarative_base(cls=Base)

ebook_genres = Table('ebook_genres', Base.metadata,
                      Column('ebook_id', ForeignKey('ebook.id',ondelete="CASCADE"), primary_key=True, index=True),
                      Column('genre_id', ForeignKey('genre.id',ondelete="CASCADE"), primary_key=True, index=True))

ebook_authors = Table('ebook_authors', Base.metadata, 
                      Column('ebook_id', ForeignKey('ebook.id', ondelete="CASCADE"), primary_key=True, index=True),
                      Column('author_id', ForeignKey('author.id',ondelete="CASCADE"), primary_key=True, index=True))

user_roles = Table('user_roles', Base.metadata, 
                      Column('user_id', ForeignKey('user.id', ondelete="CASCADE"), primary_key=True, index=True),
                      Column('role_id', ForeignKey('role.id'), primary_key=True, index=True))

# series_authors = Table('series_authors', Base.metadata, 
#                       Column('series_id', ForeignKey('series.id'), primary_key=True),
#                       Column('author_id', ForeignKey('author.id'), primary_key=True))


class Auditable(object):
    created = Column(DateTime, nullable=False, default=func.now())
    modified = Column(DateTime, nullable=False,index=True,  default=func.now(), onupdate=func.now())
    
    @declared_attr
    def created_by_id(cls):  # @NoSelf
        return Column(BigInteger, ForeignKey('user.id'))
    
    @declared_attr
    def created_by(cls):  # @NoSelf\
        return relationship('User', primaryjoin="User.id==%s.created_by_id" % cls.__name__)
    
    @declared_attr
    def modified_by_id(cls):  # @NoSelf
        return Column(BigInteger, ForeignKey('user.id'))
    
    @declared_attr
    def modified_by(cls):  # @NoSelf\
        return relationship('User', primaryjoin="User.id==%s.modified_by_id" % cls.__name__)
    
class User(Base, Auditable, UserMixin):
    user_name= Column(String(128), nullable=False, unique=True)
    email= Column(String(128), nullable=False, unique=True)
    password = Column(String(128), nullable=False)
    active= Column(Boolean)
    roles=relationship('Role', secondary=user_roles)
    
    @property
    def is_active(self):
        return self.active
    
    def has_role(self, *roles):
        if not self.active:
            return False
        if not roles:
            return True
        return bool(app.db.session.query(func.user_has_roles(1, list(roles))).one()[0])  # @UndefinedVariable
    
class Role(Base):
    name=Column(String(64), nullable=False)
    parent_id=Column(BigInteger, ForeignKey('role.id'))
    children = relationship("Role")
    
    def __repr__(self):
        return super(Role,self).__repr__(['name'])
Role.parent=relationship("Role", remote_side=[Role.id])
    
class Author(Base, Auditable):
    
    last_name = Column(String(128), nullable=False)
    first_name = Column(String(128), nullable=True)
    description = Column(Text)
    
    def __repr__(self):
        return super(Author,self).__repr__(['first_name', 'last_name'])


class Bookshelf(Base, Auditable):
    name = Column(String(256), nullable=False, index=True)
    description = Column(String)
    public = Column(Boolean, default=True)
    rating = Column(Float(asdecimal=True))
    items=relationship('BookshelfItem', back_populates='bookshelf')
    
    def __repr__(self):
        return super(Bookshelf,self).__repr__(['name'])


class BookshelfItem(Base, Auditable):
    
    type = Column(Enum('EBOOK', 'SERIES', name='BOOKSHELF_ITEM_TYPE'), nullable=False)
    bookshelf_id = Column(BigInteger, ForeignKey('bookshelf.id'), nullable=False)
    ebook_id = Column(BigInteger, ForeignKey('ebook.id'))
    ebook= relationship('Ebook')
    series_id = Column(BigInteger, ForeignKey('series.id'))
    series=relationship('Series')
    order = Column(Integer)
    note = Column(Text)
    bookshelf=relationship('Bookshelf', back_populates='items')
    
    def __repr__(self):
        return super(BookshelfItem,self).__repr__(['type'])


class Conversion(Base, Auditable):
    
    batch_id = Column(BigInteger, ForeignKey('conversion_batch.id'))
    source_id = Column(BigInteger, ForeignKey('source.id'), nullable=False)
    source=relationship('Source')
    location = Column(String(512), nullable=False)
    format_id = Column(BigInteger, ForeignKey('format.id'), nullable=False)
    format=relationship('Format', lazy='joined', innerjoin=True)
    batch=relationship('ConversionBatch', back_populates='items')


class ConversionBatch(Base, Auditable):
    
    name = Column(String(100), nullable=False)
    for_entity = Column(Enum('SERIES','AUTHOR', 'EBOOK', 'SOURCE', name='CONVERSION_BATCH_ENTITY'))
    entity_id = Column(BigInteger)
    format_id = Column(BigInteger, ForeignKey('format.id'), nullable=False)
    items=relationship('Conversion', back_populates='batch')



class Ebook(Base, Auditable):
    title = Column(String(256), nullable=False, index=True)
    description = Column(Text)
    language_id = Column(BigInteger, ForeignKey('language.id'), nullable=False)
    language = relationship('Language', lazy='joined', innerjoin=True)
    series_id = Column(BigInteger, ForeignKey('series.id'), index=True)
    series=relationship('Series', back_populates='books', lazy='joined')
    series_index = Column(Integer)
    rating = Column(Float(asdecimal=True))
    sources = relationship('Source', back_populates='ebook')
    genres = relationship('Genre', secondary=ebook_genres)
    #for lazy="subquery limited queries must be always ! ordered
    authors= relationship('Author', secondary=ebook_authors, order_by='Author.id', lazy='joined')
    cover= Column(String(512))
    full_text = deferred(Column(TSVectorType(regconfig='custom')))
    
    @property
    def authors_str(self):
        if not self.authors:
            return 'No Authors'
        if len(self.authors)==1:
            return '{a.last_name} {a.first_name}'.format(a=self.authors[0])
        else:
            l=len(self.authors)
            authors=[]
            for i in range(min(3,l)):
                authors.append('{a.last_name} {initials}'.format(a=self.authors[i], 
                               initials=initials(self.authors[i].first_name)))
            s=', '.join(authors)
            if l>3:
                s+=' and others'
            return s
                
    
    def __repr__(self):
        return super(Ebook,self).__repr__(['title'])



class Format(Base):
    mime_type = Column(String(128), nullable=False)
    name = Column(String(64), nullable=False)
    extension = Column(String(8), nullable=False, unique=True)
    
    def __repr__(self):
        return super(Format,self).__repr__(['extension', 'mime_type', 'name'])


class Language(Base):
    code = Column(String(6), nullable=False, unique=True)
    name = Column(String(64), nullable=False)
    
    def __repr__(self):
        return super(Language,self).__repr__(['name', 'code'])


class Series(Base, Auditable):
    title = Column(String(256), nullable=False, index=True)
    rating = Column(Float(asdecimal=True))
    description = Column(Text)
    books=relationship('Ebook', back_populates='series', lazy='dynamic')
    
    #authors= relationship('Author', secondary=ebook_authors, order_by='author.id', lazy='subquery')
    
    def __repr__(self):
        return super(Series,self).__repr__(['title'])


class Source(Base, Auditable):
    ebook_id = Column(BigInteger, ForeignKey('ebook.id', ondelete="CASCADE"), nullable=False)
    ebook= relationship('Ebook', back_populates='sources')
    location = Column(String(512), nullable=False)
    load_source = Column(String(256))
    format_id = Column(BigInteger, ForeignKey('format.id'), nullable=False)
    format=relationship('Format', lazy='joined', innerjoin=True)
    size = Column(Integer, nullable=False)
    hash = Column(String(128), nullable=False)
    quality = Column(Float(asdecimal=True))
    
    def __repr__(self):
        return super(Source,self).__repr__(['location'])
    
class Genre(Base):
    name = Column(String(64), nullable=False, unique=True)
    
    
    def __repr__(self):
        return super(Genre,self).__repr__(['name'])
    
    
    
sortings={'ebook':{'title': [Ebook.title],
                   '-title':[desc(Ebook.title)],
                   'created':[Ebook.created],
                   '-created':[desc(Ebook.created)],
                   },
          'author': {'name':[Author.last_name, Author.first_name],
                     '-name':[desc(Author.last_name), desc(Author.first_name)],
                     'created':[Author.created],
                   '-created':[desc(Author.created)],
                     },
          'series':{'title': [Series.title],
                   '-title':[desc(Series.title)],
                   'created':[Series.created],
                   '-created':[desc(Series.created)],
                   },
        }    
