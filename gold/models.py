from django.db import models
from uuid import uuid4

class Book(models.Model):
    '''
    Represents a book of music. A book may contain multiple book parts
    represented by the BookPart model.
    '''
    uuid = models.CharField(primary_key=True, max_length=64, editable=False, default=uuid4)
    title = models.CharField(max_length=100)
    description = models.TextField(max_length=500, blank=True)
    is_manuscript = models.BooleanField(default=False)
    printers = models.ManyToManyField('Printer')
    publication_date = models.DateField()
    location = models.CharField(max_length=100)
    printing_technology = models.ForeignKey('PrintingTechnology')
    genre = models.ManyToManyField('Genre')
    is_sacred = models.BooleanField(default=False)
    alternate_id = models.OneToOneField('AlternateBookID', null=True, blank=True)

    def __unicode__(self):
        return self.title

class BookPart(models.Model):
    '''
    Represents a segment of a music book. A book part contains multiple pages
    of music.
    E.g., Soprano part, Organ part.
    A book part must be part of a single book.
    '''

    uuid = models.CharField(primary_key=True, max_length=64, editable=False, default=uuid4)
    book = models.ForeignKey('Book')
    part_type = models.CharField(max_length=100)

    def __unicode__(self):
        return '%s [%s]' % (self.book.title, self.part_type)

class Page(models.Model):
    '''
    Represents a page of music. This is a wrapper for an image of a page
    of music and its associated mei file describing the glyphs on the page.
    '''

    uuid = models.CharField(primary_key=True, max_length=64, editable=False, default=uuid4)
    book_part = models.ForeignKey('BookPart')
    image = models.ImageField(upload_to='images/', width_field='image_width', height_field='image_height')
    image_width = models.IntegerField(editable=False)
    image_height = models.IntegerField(editable=False)
    mei = models.FileField(upload_to='mei/')
    sequence = models.IntegerField()

    def __unicode__(self):
        return '%s (p. %d)' % (self.book_part.book.title, self.sequence)

class Printer(models.Model):
    '''
    Printers of books. Books have a Many-to-Many relationship
    with Printers. That is, a Book may have many printers (or scribes)
    and a printer may have printed many books.
    '''

    name = models.CharField(max_length=100)

    def __unicode__(self):
        return self.name

class PrintingTechnology(models.Model):
    '''
    Technology used for printing the book.
    '''

    technology_type = models.CharField(max_length=100)

    def __unicode__(self):
        return self.technology_type

class Genre(models.Model):
    '''
    The genre of books.
    This model has a Many-to-Many relationship with book, meaning that
    a Book may have many genres and a genre may be associated with more
    than one book.
    '''

    genre_name = models.CharField(max_length=100)

    def __unicode__(self):
        return self.genre_name

class AlternateBookID(models.Model):
    '''
    Alternate book identifier (apart from the UUID of the book).
    This model has a One-To-(Zero or One) relationship with Book, meaning that
    a Book may have an alternate ID, and an alternate book ID references a single book.
    Given an AlternateBookID object, say abid, the associated book can be accessed
    by abid.book.
    The type field stores a description of the identifier, e.g., RISM ID, Chant No..
    '''

    id = models.CharField(max_length=150, primary_key=True)
    id_type = models.CharField(max_length=100)

    def __unicode__(self):
        return self.id
