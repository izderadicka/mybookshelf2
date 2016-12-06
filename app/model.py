# coding: utf-8
import app
from sqlalchemy import Column, Date, DateTime, Float, Index, Integer, SmallInteger, String, \
    BigInteger, Boolean, ForeignKey, Text, Enum, Table, desc, select, func
from sqlalchemy.ext.declarative import declarative_base, declared_attr
from sqlalchemy.sql import func
from sqlalchemy.sql.expression import nullsfirst, nullslast
from sqlalchemy.orm import relationship, deferred, backref, column_property
from flask_login import UserMixin, current_user
from sqlalchemy_utils import TSVectorType, JSONType
# TODO - check if can use thse types instead
from sqlalchemy.dialects.postgresql import JSON, TSVECTOR
from common.utils import initials
import datetime

model_base = app.db.Model or declarative_base()

class Base(model_base):
    __abstract__ = True

    id = Column(BigInteger, primary_key=True)
    version_id = Column("version_id", Integer, nullable=False)

    __mapper_args__ = {
        'version_id_col': version_id,
    }

    def __repr__(self, attrs=None):
        base = '<%s id=%s' % (self.__class__.__name__, self.id)
        if attrs:
            base += ' ' + \
                ' '.join(['%s="%s"' % (a, getattr(self, a)) for a in attrs])
        return base + '>'

#Base = declarative_base(cls=Base)

ebook_genres = Table('ebook_genres', Base.metadata,
                     Column('ebook_id', ForeignKey(
                         'ebook.id', ondelete="CASCADE"), primary_key=True, index=True),
                     Column('genre_id', ForeignKey('genre.id', ondelete="CASCADE"), primary_key=True, index=True))

ebook_authors = Table('ebook_authors', Base.metadata,
                      Column('ebook_id', ForeignKey(
                          'ebook.id', ondelete="CASCADE"), primary_key=True, index=True),
                      Column('author_id', ForeignKey('author.id', ondelete="CASCADE"), primary_key=True, index=True))

user_roles = Table('user_roles', Base.metadata,
                   Column('user_id', ForeignKey(
                       'user.id', ondelete="CASCADE"), primary_key=True, index=True),
                   Column('role_id', ForeignKey('role.id'), primary_key=True, index=True))

# series_authors = Table('series_authors', Base.metadata,
#                       Column('series_id', ForeignKey('series.id'), primary_key=True),
# Column('author_id', ForeignKey('author.id'), primary_key=True))


class Auditable(object):
    created = Column(DateTime, nullable=False, default=func.now())
    modified = Column(
        DateTime, nullable=False, index=True,  default=func.now(), onupdate=func.now())

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
    user_name = Column(String(128), nullable=False, unique=True)
    email = Column(String(128), nullable=False, unique=True)
    password = Column(String(128), nullable=False)
    active = Column(Boolean)
    roles = relationship('Role', secondary=user_roles)
    preferences = Column(JSON)

    @property
    def is_active(self):
        return self.active

    @property
    def all_roles(self):
        # all_roles are cached for efficiency
        if not hasattr(self, '_all_roles'):
            self._all_roles = set(map(lambda x: x[0], app.db.session.query(
                func.user_roles(self.id)).all()))  # @UndefinedVariable
        return self._all_roles

    def has_role(self, *roles):
        if not self.active:
            return False
        if not roles:
            return True
        for role in roles:
            if role in self.all_roles:
                return True


class Role(Base):
    name = Column(String(64), nullable=False)
    parent_id = Column(BigInteger, ForeignKey('role.id'))
    children = relationship("Role")

    def __repr__(self):
        return super(Role, self).__repr__(['name'])
Role.parent = relationship("Role", remote_side=[Role.id])


class Author(Base, Auditable):

    last_name = Column(String(128), nullable=False)
    first_name = Column(String(128), nullable=True)
    description = Column(Text)
    ebooks = relationship('Ebook', secondary=ebook_authors, lazy="dynamic")

    def __repr__(self):
        return super(Author, self).__repr__(['first_name', 'last_name'])
    
class BookshelfItem(Base, Auditable):

    type = Column(
        Enum('EBOOK', 'SERIES', name='BOOKSHELF_ITEM_TYPE'), nullable=False)
    bookshelf_id = Column(
        BigInteger, ForeignKey('bookshelf.id'), nullable=False)
    ebook_id = Column(BigInteger, ForeignKey('ebook.id'))
    ebook = relationship('Ebook')
    series_id = Column(BigInteger, ForeignKey('series.id'))
    series = relationship('Series')
    order = Column(Integer)
    note = Column(Text)
    bookshelf = relationship('Bookshelf', back_populates='items')

    def __repr__(self):
        return super(BookshelfItem, self).__repr__(['type'])


class Bookshelf(Base, Auditable):
    name = Column(String(256), nullable=False, index=True)
    description = Column(Text)
    public = Column(Boolean, default=True)
    rating = Column(Float(asdecimal=True))
    rating_count = Column(Integer)
    items = relationship('BookshelfItem', back_populates='bookshelf', lazy='dynamic', cascade = 'all')
    
    def __repr__(self):
        return super(Bookshelf, self).__repr__(['name'])
    
    def add_ebook(self, ebook, user, note=None, order=None):
        ebook_id = ebook.id if isinstance(ebook, Ebook) else ebook
        if not self.items.filter(BookshelfItem.ebook_id == ebook_id).all():
            item = BookshelfItem(type='EBOOK', ebook_id=ebook_id, note=note, 
                                 order=order,bookshelf=self, created_by=user,
                                 modified_by=user)
            app.db.session.add(item)
        self.modified = datetime.datetime.now()
        
    def add_series(self, series, user, note=None, order=None):
        series_id = series.id if isinstance(series, Series) else series
        if not self.items.filter(BookshelfItem.series_id == series_id).all():
            item = BookshelfItem(type='SERIES', series_id=series_id, note=note, 
                                 order=order,bookshelf=self, created_by=user,
                                 modified_by=user)
            app.db.session.add(item)
        self.modified = datetime.datetime.now()
    
Bookshelf.items_count = column_property(
        select([func.count(BookshelfItem.id)]).\
        where(BookshelfItem.bookshelf_id == Bookshelf.id).\
        correlate_except(BookshelfItem)
            )

    
class BookshelfRating(Base, Auditable):
    bookshelf_id = Column(BigInteger, ForeignKey('bookshelf.id'), nullable=False)
    rating = Column(Float(asdecimal=True))
    description = Column(Text)
    bookshelf = relationship('Bookshelf')#, backref=backref('ratings', lazy='dynamic'))



class Conversion(Base, Auditable):

    batch_id = Column(BigInteger, ForeignKey('conversion_batch.id'))
    source_id = Column(BigInteger, ForeignKey('source.id'), nullable=False)
    source = relationship('Source', back_populates="conversions")
    location = Column(String(512), nullable=False)
    format_id = Column(BigInteger, ForeignKey('format.id'), nullable=False)
    format = relationship('Format', lazy='joined', innerjoin=True)
    batch = relationship('ConversionBatch', back_populates='items')
    


class ConversionBatch(Base, Auditable):

    name = Column(String(100), nullable=False)
    for_entity = Column(
        Enum('SERIES', 'AUTHOR', 'EBOOK', 'SOURCE', name='CONVERSION_BATCH_ENTITY'))
    entity_id = Column(BigInteger)
    format_id = Column(BigInteger, ForeignKey('format.id'), nullable=False)
    items = relationship('Conversion', back_populates='batch')
    zip_location = Column(String(512))
   


class Ebook(Base, Auditable):
    title = Column(String(256), nullable=False, index=True)
    description = Column(Text)
    language_id = Column(BigInteger, ForeignKey('language.id'), nullable=False)
    language = relationship('Language', lazy='joined', innerjoin=True)
    series_id = Column(BigInteger, ForeignKey('series.id'), index=True)
    series = relationship('Series', back_populates='books', lazy='joined')
    series_index = Column(Integer)
    rating = Column(Float(asdecimal=True))
    rating_count = Column(Integer)
    downloads = Column(Integer)
    sources = relationship('Source', back_populates='ebook', cascade="all")
    genres = relationship('Genre', secondary=ebook_genres)
    # for lazy="subquery limited queries must be always ! ordered
    authors = relationship(
        'Author', secondary=ebook_authors, order_by='Author.id', lazy='joined')
    cover = Column(String(512))
    base_dir = Column(String(512), nullable=False)
    full_text = deferred(Column(TSVectorType(regconfig='custom')))
    
    @property
    def my_rating(self):
        rating = EbookRating.query.filter(EbookRating.ebook_id == self.id, 
                                          EbookRating.created_by == current_user).one_or_none()
        if rating:
            return rating.rating
        

    @property
    def authors_str(self):
        if not self.authors:
            return 'No Authors'
        if len(self.authors) == 1:
            return '{a.last_name} {a.first_name}'.format(a=self.authors[0])\
                 if self.authors[0].first_name else self.authors[0].last_name
        else:
            l = len(self.authors)
            authors = []
            for i in range(min(3, l)):
                authors.append('{a.last_name} {initials}'.format(a=self.authors[i],
                                initials=initials(self.authors[i].first_name))\
                               if self.authors[i].first_name else self.authors[i].last_name
                               )
            s = ', '.join(authors)
            if l > 3:
                s += ' and others'
            return s

    def __repr__(self):
        return super(Ebook, self).__repr__(['title'])
    

class EbookRating(Base, Auditable):
    ebook_id = Column(BigInteger, ForeignKey('ebook.id'), nullable=False)
    rating = Column(Float(asdecimal=True))
    description = Column(Text)
    ebook = relationship('Ebook')#, backref=backref('ratings', lazy='dynamic'))    


class Format(Base):
    mime_type = Column(String(128), nullable=False)
    name = Column(String(64), nullable=False)
    extension = Column(String(8), nullable=False, unique=True)

    def __repr__(self):
        return super(Format, self).__repr__(['extension', 'mime_type', 'name'])


class Language(Base):
    code = Column(String(6), nullable=False, unique=True)
    name = Column(String(64), nullable=False)

    def __repr__(self):
        return super(Language, self).__repr__(['name', 'code'])


class Series(Base, Auditable):
    title = Column(String(256), nullable=False, index=True)
    rating = Column(Float(asdecimal=True))
    rating_count = Column(Integer)
    description = Column(Text)
    books = relationship('Ebook', back_populates='series', lazy='dynamic')

    authors= relationship('Author', 
                          secondary='join(ebook_authors, Ebook, ebook_authors.c.ebook_id == Ebook.id)', 
                          primaryjoin='Ebook.series_id == Series.id',
                          secondaryjoin ='ebook_authors.c.author_id == Author.id',
                          order_by='Author.id', 
                          viewonly=True,
                          lazy="joined", #subquery ...
                          )

    def __repr__(self):
        return super(Series, self).__repr__(['title'])

class SeriesRating(Base, Auditable):
    series_id = Column(BigInteger, ForeignKey('series.id'), nullable=False)
    rating = Column(Float(asdecimal=True))
    description = Column(Text)
    series = relationship('Series')#, backref=backref('ratings', lazy='dynamic'))    


class Source(Base, Auditable):
    ebook_id = Column(
        BigInteger, ForeignKey('ebook.id', ondelete="CASCADE"), nullable=False)
    ebook = relationship('Ebook', back_populates='sources')
    location = Column(String(512), nullable=False)
    load_source = Column(String(256))
    format_id = Column(BigInteger, ForeignKey('format.id'), nullable=False)
    format = relationship('Format', lazy='joined', innerjoin=True)
    size = Column(Integer, nullable=False)
    hash = Column(String(128), nullable=False)
    quality = Column(Float(asdecimal=True))
    quality_count = Column(Integer)
    conversions = relationship('Conversion', cascade = 'all')
    
    def __repr__(self):
        return super(Source, self).__repr__(['location'])
    
class SourceQuality(Base, Auditable):
    source_id = Column(BigInteger, ForeignKey('source.id'), nullable=False)
    quality = Column(Float(asdecimal=True))
    description = Column(Text)
    source = relationship('Source', backref=backref('ratings', lazy='dynamic'))    


class Upload(Base, Auditable):
    cover = Column(String(512))
    file = Column(String(512), nullable=False)
    load_source = Column(String(256))
    format_id = Column(BigInteger, ForeignKey('format.id'), nullable=False)
    format = relationship('Format')
    size = Column(Integer, nullable=False)
    hash = Column(String(128), nullable=False)
    meta = Column(JSON)
    
    def __repr__(self):
        return super(Upload, self).__repr__(['file'])
    


class Genre(Base):
    name = Column(String(64), nullable=False, unique=True)

    def __repr__(self):
        return super(Genre, self).__repr__(['name'])


class Synonym(Base):
    LANGUAGE_CODE = 'LNG'
    LANGUAGE_NAME = 'LGN'
    GENRE = 'GNR'

    other_name = Column(String(512), nullable=False)
    our_name = Column(String(512), nullable=False)
    category = Column(String(3), nullable=False)
    
class Version(Base):
    version = Column(Integer)

# It's critical for paging that sorting unambiguous 
sortings = {'ebook': {'title': [Ebook.title, Ebook.id],
                      '-title': [desc(Ebook.title), desc(Ebook.id)],
                      'created': [Ebook.created, Ebook.id],
                      '-created': [desc(Ebook.created), desc(Ebook.id)],
                      'rating': [nullslast(Ebook.rating), Ebook.rating_count, Ebook.id],
                      '-rating': [nullslast(desc(Ebook.rating)), desc(Ebook.rating_count), desc(Ebook.id)],
                      },
            'bookshelf': {'name': [Bookshelf.name, Bookshelf.id],
                      '-name': [desc(Bookshelf.name), desc(Bookshelf.id)],
                      'created': [Bookshelf.created, Bookshelf.id],
                      '-created': [desc(Bookshelf.created), desc(Bookshelf.id)],
                      'modified': [Bookshelf.modified, Bookshelf.id],
                      '-modified': [desc(Bookshelf.modified), desc(Bookshelf.id)],
                },
             'bookshelf_item': {'order': [BookshelfItem.order, BookshelfItem.id],
                      '-order': [desc(BookshelfItem.order), desc(BookshelfItem.id)],
                      'created': [BookshelfItem.created, BookshelfItem.id],
                      '-created': [desc(BookshelfItem.created), desc(BookshelfItem.id)],
                },
            'shelf': {'name': [Bookshelf.name, Bookshelf.id],
                      '-name': [desc(Bookshelf.name), desc(Bookshelf.id)],
                      'created': [Bookshelf.created, Bookshelf.id],
                      '-created': [desc(Bookshelf.created), desc(Bookshelf.id)],
                },
            'ebook_in_series': {'title': [Ebook.title, Ebook.id],
                      '-title': [desc(Ebook.title), desc(Ebook.id)],
                      'created': [Ebook.created, Ebook.id],
                      '-created': [desc(Ebook.created), desc(Ebook.id)],
                      'series_index': [Ebook.series_index, Ebook.title, Ebook.id],
                      '-series_index': [desc(Ebook.series_index), desc(Ebook.title), desc(Ebook.id)],
                      },
            'author': {'name': [Author.last_name, Author.first_name, Author.id],
                       '-name': [desc(Author.last_name), desc(Author.first_name), desc(Author.id)],
                       'created': [Author.created, Author.id],
                       '-created': [desc(Author.created), desc(Author.id)],
                       },
            'series': {'title': [Series.title, Series.id],
                       '-title': [desc(Series.title), desc(Series.id)],
                       'created': [Series.created, Series.id],
                       '-created': [desc(Series.created), desc(Series.id)],
                       },
            }
