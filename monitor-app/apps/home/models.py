# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from datetime import datetime, timezone

from apps import db

class Data(db.Model):

    __tablename__ = 'data'

    id = db.Column(db.Integer, primary_key=True)

    code     = db.Column(db.String(64))   # product code 
    name     = db.Column(db.String(128))  # product name
    value    = db.Column(db.Integer)      # numeric
    currency = db.Column(db.String(10))   # string: usd, euro
    type     = db.Column(db.String(64))   # transaction
    ts       = db.Column(db.Integer, default=datetime.utcnow().timestamp())

    def __repr__(self):
        return str( self.id ) 

    def save(self):
        db.session.add(self)
        db.session.commit()

    def update_value(self, new_value):
        self.value = new_value

    @classmethod
    def get_by_id(cls, id):
        return cls.query.filter_by(id=id).first()

    def toDICT(self):

        cls_dict          = {}
        cls_dict['_id']   = self.id
        cls_dict['name'] = self.name
        cls_dict['value'] = self.value

        return cls_dict

    def toJSON(self):

        return self.toDICT()


class Fileinfo(db.Model):
    __tablename__ = 'fileinfos'

    id = db.Column(db.Integer, primary_key=True)

    path=db.Column(db.String(100), unique=True)     #file full path 
    filename = db.Column(db.String(100))            #file fullname
    filetype = db.Column(db.String(100))            #type of file
    filesize = db.Column(db.Integer)                #file size
    sha1_hash = db.Column(db.String(100))           # file hash
    date = db.Column(db.DateTime(timezone=True), nullable=False, default=datetime.now(timezone.utc))

    def __repr__(self):
        return str( self.id ) 

    def save(self):
        db.session.add(self)
        db.session.commit()

    def update_value(self, new_value):
        self.value = new_value

    @classmethod
    def get_by_id(cls, id):
        return cls.query.filter_by(id=id).first()

    def toDICT(self):

        cls_dict          = {}
        cls_dict['_id']   = self.id
        cls_dict['filename']   = self.filename
        cls_dict['filepath'] = self.path
        cls_dict['filetype'] = self.filetype
        cls_dict['file_hash'] = self.sha1_hash
        cls_dict['date'] = self.date

        return cls_dict


    def toJSON(self):
        
        return self.toDICT()

class UploadFile(db.Model):
    __tablename__ = 'upload_fileinfos'

    id = db.Column(db.Integer, primary_key=True)

    # path=db.Column(db.String(100), unique=True)     #file full path 
    filename = db.Column(db.String(100))            #file fullname
    filetype = db.Column(db.String(100))            #type of file
    filesize = db.Column(db.Integer)                #file size
    date = db.Column(db.DateTime(timezone=True), nullable=False, default=datetime.now(timezone.utc))

    def __repr__(self):
        return str( self.id ) 

    def save(self):
        db.session.add(self)
        db.session.commit()

    def update_value(self, new_value):
        self.value = new_value

    @classmethod
    def get_by_id(cls, id):
        return cls.query.filter_by(id=id).first()

    def toDICT(self):
        cls_dict          = {}
        cls_dict['_id']   = self.id
        cls_dict['filename']   = self.filename
        cls_dict['filetype'] = self.filetype
        cls_dict['date'] = self.date

        return cls_dict


    def toJSON(self):
        
        return self.toDICT()
