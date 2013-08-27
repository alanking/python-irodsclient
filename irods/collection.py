from os.path import basename

from models import Collection, DataObject
from data_object import iRODSDataObject
from meta import iRODSMetaCollection

class iRODSCollection(object):
    def __init__(self, manager, result=None):
        self.manager = manager
        if result:
            self.id = result[Collection.id]
            self.path = result[Collection.name]
            self.name = basename(result[Collection.name])
        self._meta = None

    @property
    def metadata(self):
        if not self._meta:
            self._meta = iRODSMetaCollection(self.manager.sess.metadata, 
                Collection, self.path)
        return self._meta

    @property
    def subcollections(self):
        query = self.manager.sess.query(Collection)\
            .filter(Collection.parent_name == self.path)
        results = query.all()
        return [iRODSCollection(self.manager, row) for row in results]

    @property
    def data_objects(self):
        query = self.manager.sess.query(DataObject)\
            .filter(DataObject.collection_id == self.id)
        results = query.all()
        return [
            iRODSDataObject(self.manager.sess.data_objects, self, row) 
            for row in results
        ]

    def __repr__(self):
        return "<iRODSCollection %d %s>" % (self.id, self.name)
