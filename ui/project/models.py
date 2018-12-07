from project import db

class Input(db.EmbeddedDocument):
    meta = {
      'strict' : False
    }
    msg = db.StringField()
    start = db.StringField()
    filename = db.StringField()
    trigger = db.StringField()
    path =  db.StringField()


class Input_data(db.EmbeddedDocument):
    meta = {
      'strict' : False
    }
    grid = db.StringField()
    payload = db.FileField()
    context_type = db.StringField()

class Translate_data(db.EmbeddedDocument):
    meta = {
      'strict' : False
    }
    grid = db.StringField()
    payload = db.FileField()
    context_type = db.StringField()

class Translate(db.EmbeddedDocument):
    meta = {
      'strict' : False
    }
    msg = db.StringField()
    start = db.StringField()

class Ocr(db.EmbeddedDocument):
    meta = {
      'strict' : False
    }
    msg = db.StringField()
    start = db.StringField()

class Ocr_data(db.EmbeddedDocument):
    meta = {
      'strict' : False
    }
    grid = db.StringField()
    payload = db.FileField()
    context_type = db.StringField()

class Clean_data(db.EmbeddedDocument):
    meta = {
      'strict' : False
    }
    grid = db.StringField()
    payload = db.FileField()
    context_type = db.StringField()

class Complete(db.EmbeddedDocument):
    meta = {
      'strict' : False
    }
    msg = db.StringField()
    start = db.StringField()

class Route(db.EmbeddedDocument):
    meta = {
      'strict' : False
    }
    msg = db.StringField()
    start = db.StringField()

class Nifi(db.Document):
    meta = {
      'strict' : False
    }
    uuid = db.StringField()
    source = db.StringField()
    model = db.StringField()
    state = db.StringField()
    result = db.StringField()
    input = db.EmbeddedDocumentField(Input)
    input_data = db.EmbeddedDocumentField(Input_data)
    translate = db.EmbeddedDocumentField(Translate)
    translate_data = db.EmbeddedDocumentField(Translate_data)
    ocr = db.EmbeddedDocumentField(Ocr)
    ocr_data = db.EmbeddedDocumentField(Ocr_data)
    clean_data = db.EmbeddedDocumentField(Clean_data)
    complete = db.EmbeddedDocumentField(Complete)
    route = db.EmbeddedDocumentField(Route)

####################################3
#  NIFI does NOT ROCK.
#  Nifi cannot save as ObjectId() 
#  Patch the ObjectId() ... ugh
#     read the fsgrid 
#     store as a objectId()
####################################3
class PatchSub(db.EmbeddedDocument):
    meta = {
      'strict' : False
    }
    grid = db.StringField()
    payload = db.ObjectIdField()
    context_type = db.StringField()

class PatchMain(db.Document):
    meta = {
      'strict' : False,
      'collection': 'nifi'
    }
    uuid = db.StringField()
    input_data = db.EmbeddedDocumentField(PatchSub)
    translate_data = db.EmbeddedDocumentField(PatchSub)
    ocr_data = db.EmbeddedDocumentField(PatchSub)
    clean_data = db.EmbeddedDocumentField(PatchSub)

