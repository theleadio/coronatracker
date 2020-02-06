"""
    created by : Edmund Hee
    email : edmund.hee05@gmail.com
"""
import logging
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from google.cloud.exceptions import NotFound
from .exceptions import DocumentNotSaved, DocumentExistInFirestore


class FireStoreModel(object):

    def __init__(self, collection_id):
        cred = credentials.Certificate('./cred/coronatracker-f8eea1bc1612.json')
        firebase_admin.initialize_app(cred)
        self.client = firestore.client()
        self.collection = self.client.collection(collection_id)

    def _doc_ref(self, document_id):
        return self.collection.document(document_id)

    def save(self, document_id, content):
        try:

            doc_ref = self._doc_ref(document_id=document_id)
            doc_ref.set(content)

            return {"is_saved": True, "doc_id": document_id}

        except DocumentNotSaved as e:
            logging.error(str(e))
            return {"is_saved": False}
        except DocumentExistInFirestore as e:
            logging.error(str(e))
            return {"is_saved": False}

    def exists(self, document_id):
        return True if self.get_by_id(document_id=document_id) else False

    def get_by_id(self, document_id):
        doc_ref = self._doc_ref(document_id=document_id)
        try:
            doc = doc_ref.get()
            return doc.to_dict()
        except NotFound:
            logging.info("No Document Found - {}".format(document_id))
            return {}

    def batch_save(self, dict_list):

        if not dict_list:
            return {"input_count: {}".format(0)}

        batch = self.client.batch()
        counter = 0
        for key, value in dict_list.iteritems():
            doc_ref = self._doc_ref(document_id=key)
            batch.set(doc_ref, value)
            counter += 1
        logging.info("Batch input size: {}".format(counter))
        batch.commit()
        return {"input_count: {}".format(counter)}
