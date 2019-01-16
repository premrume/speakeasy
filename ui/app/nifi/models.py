# nifi stuff
from app.extensions import dbm
class Input(dbm.EmbeddedDocument):
    meta = {
      'strict' : False
    }
    msg = dbm.StringField()
    start = dbm.StringField()
    filename = dbm.StringField()
    trigger = dbm.StringField()
    path =  dbm.StringField()
    fileSize =  dbm.StringField()


class Input_data(dbm.EmbeddedDocument):
    meta = {
      'strict' : False
    }
    grid = dbm.StringField()
    payload = dbm.FileField()
    context_type = dbm.StringField()

class Translate_data(dbm.EmbeddedDocument):
    meta = {
      'strict' : False
    }
    grid = dbm.StringField()
    payload = dbm.FileField()
    context_type = dbm.StringField()

class Translate(dbm.EmbeddedDocument):
    meta = {
      'strict' : False
    }
    msg = dbm.StringField()
    start = dbm.StringField()

class Ocr(dbm.EmbeddedDocument):
    meta = {
      'strict' : False
    }
    msg = dbm.StringField()
    start = dbm.StringField()
    lang = dbm.StringField()

class Ocr_data(dbm.EmbeddedDocument):
    meta = {
      'strict' : False
    }
    grid = dbm.StringField()
    payload = dbm.FileField()
    context_type = dbm.StringField()

class Clean_data(dbm.EmbeddedDocument):
    meta = {
      'strict' : False
    }
    grid = dbm.StringField()
    payload = dbm.FileField()
    context_type = dbm.StringField()

class Complete(dbm.EmbeddedDocument):
    meta = {
      'strict' : False
    }
    msg = dbm.StringField()
    start = dbm.StringField()

class Route(dbm.EmbeddedDocument):
    meta = {
      'strict' : False
    }
    msg = dbm.StringField()
    start = dbm.StringField()

class Metadata(dbm.EmbeddedDocument):
    meta = {
      'strict' : False
    }
    msg = dbm.StringField()
    start = dbm.StringField()
    summary = dbm.StringField()
    keywords = dbm.StringField()

class Nifi(dbm.Document):
    meta = {
      'strict' : False
    }
    uuid = dbm.StringField()
    source = dbm.StringField()
    model = dbm.StringField()
    sourceLanguage = dbm.StringField()
    targetLanguage = dbm.StringField()
    state = dbm.StringField()
    result = dbm.StringField()
    input = dbm.EmbeddedDocumentField(Input)
    input_data = dbm.EmbeddedDocumentField(Input_data)
    translate = dbm.EmbeddedDocumentField(Translate)
    translate_data = dbm.EmbeddedDocumentField(Translate_data)
    ocr = dbm.EmbeddedDocumentField(Ocr)
    ocr_data = dbm.EmbeddedDocumentField(Ocr_data)
    clean_data = dbm.EmbeddedDocumentField(Clean_data)
    complete = dbm.EmbeddedDocumentField(Complete)
    route = dbm.EmbeddedDocumentField(Route)
    metadata = dbm.EmbeddedDocumentField(Metadata)

####################################3
#  NIFI does NOT ROCK.
#  Nifi cannot save as ObjectId() 
#  Patch the ObjectId() ... ugh
#     read the fsgrid 
#     store as a objectId()
####################################3
class PatchSub(dbm.EmbeddedDocument):
    meta = {
      'strict' : False
    }
    grid = dbm.StringField()
    payload = dbm.ObjectIdField()
    context_type = dbm.StringField()

class PatchMain(dbm.Document):
    meta = {
      'strict' : False,
      'collection': 'nifi'
    }
    uuid = dbm.StringField()
    input_data = dbm.EmbeddedDocumentField(PatchSub)
    translate_data = dbm.EmbeddedDocumentField(PatchSub)
    ocr_data = dbm.EmbeddedDocumentField(PatchSub)
    clean_data = dbm.EmbeddedDocumentField(PatchSub)

