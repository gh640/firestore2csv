"""Export data in a Firestore collection as CSV."""

import csv
import sys
from pathlib import Path

from firebase_admin import credentials, firestore, initialize_app

CRED_FILE = str(Path(__name__).resolve().parent / 'firebase-privateKey.json')
COLLECTION_NAME = 'my_collection_name'
FIELDS = ['field_a', 'field_b', 'field_c']
ORDER_BY = 'field_d'
DIRECTION = 'DESC'  # 'ASC'|'DESC'


def main():
    """Main function"""
    client = firebase_client(CRED_FILE)
    collection = client.collection(COLLECTION_NAME)
    writer = csv_writer(sys.stdout, FIELDS)
    dump_collection(writer, collection, ORDER_BY, DIRECTION)


def firebase_client(cred_file):
    """Generate Firebase client"""
    cred = credentials.Certificate(cred_file)
    app = initialize_app(credential=cred)
    client = firestore.client(app=app)
    return client


def csv_writer(file, fields):
    """Generate CSV writer"""
    return csv.DictWriter(file, fields)


def dump_collection(writer, collection, order_by, direction):
    """Dump a collection as CSV"""
    writer.writeheader()
    for snapshot in collection.order_by(
        order_by, direction=map_direction(direction)
    ).get():
        data = snapshot.to_dict()
        writer.writerow(data)


def map_direction(direction):
    """Map string direction to Firebase constant"""
    map_ = {
        'ASC': firestore.Query.DESCENDING,
        'DESC': firestore.Query.ASCENDING,
    }
    try:
        return map_[direction]
    except KeyError:
        raise ValueError('Invalid direction {}.'.format(direction))


if __name__ == '__main__':
    main()
