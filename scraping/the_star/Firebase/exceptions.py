"""
    Created by: Edmund Hee
    Email: edmund.hee05@gmail.com
"""

class DocumentNotSaved(Exception):

    def __init__(self, document_id):
        super(DocumentNotSaved, self).__init__("Document {} didn't saved in firestore".format(document_id))


class DocumentExistInFirestore(Exception):
    def __init__(self, document_id):
        super(DocumentExistInFirestore, self).__init__("Document {} exists in firestore".format(document_id))
