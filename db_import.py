import os
import sqlite3


def _dirname(path):
    (head, tail) = os.path.split(path)
    if len(tail) == 0:
        (head, tail) = os.path.split(head)
    return tail


def _collection_id(name, parent_id=None):
    query = 'SELECT id FROM Collection WHERE name = ?'
    args = (name,)
    if parent_id:
        query += ' AND parentId = ?'
        args = (name, parent_id,)
    with sqlite3.connect('mese.db') as connection:
        cursor = connection.cursor()
        cursor.execute(query, args)
        results = cursor.fetchall()
        if len(results) == 1:
            return results[0][0]
        else:
            query = 'INSERT INTO Collection(name, parentId) VALUES (?, ?)'
            args = (name, parent_id,)
            cursor.execute(query, args)
            return cursor.lastrowid


def db_import(path, make_url, parent_id=None):
    if not os.path.isdir(path):
        raise Exception("Not a directory: " + path)
    dirname = _dirname(path)
    collection_id = _collection_id(dirname, parent_id)
    for name in os.listdir(path):
        child_path = os.path.join(path, name)
        if os.path.isdir(child_path):
            db_import(child_path, make_url, collection_id)
        elif os.path.splitext(child_path)[1] in ['.mp4', '.mp3', '.avi']:
            with sqlite3.connect('mese.db') as connection:
                cursor = connection.cursor()
                cursor.execute("INSERT INTO Media(url, name) VALUES (?,?)", (make_url(child_path), os.path.splitext(os.path.split(child_path)[1])[0],))
                cursor.execute("INSERT INTO CollectionMedia(collectionId, mediaId) VALUES (?,?)", (collection_id, cursor.lastrowid,))

if __name__ == "__main__":
    def url(path):
        return path.replace("/Users/william/Projects/mese", "")
    db_import('/Users/william/Projects/mese/static/media/tv', url)
    db_import('/Users/william/Projects/mese/static/media/movies', url)
    db_import('/Users/william/Projects/mese/static/media/music', url)
