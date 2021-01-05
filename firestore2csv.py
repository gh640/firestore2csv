"""Export data in a Firestore collection as CSV."""

import argparse
import csv
import sys

from firebase_admin import credentials, firestore, initialize_app

DIRECTIONS = {'ASC', 'DESC'}


def main():
    """Main function"""
    args = get_args()
    cred_file = args.cred_file.name
    collection_name = args.collection_name
    fields = args.fields.split(',')
    order_by = args.order_by
    direction = args.direction

    client = firebase_client(cred_file)
    collection = client.collection(collection_name)

    writer = csv_writer(sys.stdout, fields)
    dump_collection(writer, collection, fields, order_by, direction)


def get_args():
    """Get command line args"""
    parser = argparse.ArgumentParser()
    parser.add_argument('--cred-file', type=argparse.FileType('r'), required=True)
    parser.add_argument('--collection-name', required=True)
    parser.add_argument('--fields', required=True)
    parser.add_argument('--order-by', required=True)
    parser.add_argument('--direction', choices=DIRECTIONS, required=True)

    return parser.parse_args()


def firebase_client(cred_file):
    """Generate Firebase client"""
    cred = credentials.Certificate(cred_file)
    app = initialize_app(credential=cred)
    client = firestore.client(app=app)
    return client


def csv_writer(file, fields):
    """Generate CSV writer"""
    return csv.DictWriter(file, fields)


def dump_collection(writer, collection, fields, order_by, direction_str):
    """Dump a collection as CSV"""
    direction = map_direction(direction_str)
    writer.writeheader()
    for snapshot in collection.order_by(order_by, direction=direction).get():
        data = snapshot.to_dict()
        writer.writerow({k: v for k, v in data.items() if k in fields})


def map_direction(direction_str):
    """Map string direction to Firebase constant"""
    map_ = {
        'ASC': firestore.Query.DESCENDING,
        'DESC': firestore.Query.ASCENDING,
    }
    try:
        return map_[direction_str]
    except KeyError:
        raise ValueError('Invalid direction {}.'.format(direction_str))


if __name__ == '__main__':
    main()
