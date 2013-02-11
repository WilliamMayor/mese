import sqlite3
import os
import re

class Database:
    PATH = 'database.db'
    MUSIC_PATH = os.path.join('static', 'music')

    def __init__(self):
            self.db = sqlite3.connect(Database.PATH)

    def query(self, query, args=(), one=False):
        cur = self.db.execute(query, args)
        rv = [dict((cur.description[idx][0], value)
                for idx, value in enumerate(row)) for row in cur.fetchall()]
        return (rv[0] if rv else None) if one else rv

    def insert(self, query, args=()):
        cursor = self.db.execute(query, args)
        return cursor.lastrowid

    def commit(self):
        self.db.commit()

    def close(self):
        self.db.close()

    def clean(self):
        self.query('DROP TABLE IF EXISTS music_artist')
        self.query('CREATE TABLE music_artist(name TEXT)')

        self.query('DROP TABLE IF EXISTS music_album')
        self.query('CREATE TABLE music_album(artistid INTEGER, name TEXT, artwork TEXT, FOREIGN KEY(artistid) REFERENCES music_artist(rowid))')

        self.query('DROP TABLE IF EXISTS music_track')
        self.query('CREATE TABLE music_track(albumid INTEGER, position INTEGER, name TEXT, path TEXT, FOREIGN KEY(albumid) REFERENCES music_album(rowid))')

    def refresh(self):
        self.clean()
        self.__refresh_music()

                
        self.commit()
        return True

    def __refresh_music(self):
        for artistname in os.listdir(Database.MUSIC_PATH):
            artistpath = os.path.join(Database.MUSIC_PATH, artistname)
            if os.path.isdir(artistpath):
                artistid = self.insert("INSERT INTO music_artist('name') VALUES(?)", [unicode(artistname,"utf-8")])
                for albumname in os.listdir(artistpath):
                    albumpath = os.path.join(artistpath, albumname)
                    if os.path.isdir(albumpath):
                        albumid = self.insert("INSERT INTO music_album('artistid', 'name') VALUES(?,?)", [artistid, unicode(albumname,"utf-8")])
                        for trackname in os.listdir(albumpath):
                            regexp = re.compile("^(\d\d) ")
                            parts = regexp.split(trackname)
                            if len(parts) == 3:
                                position = int(parts[1])
                                name = unicode(os.path.splitext(parts[2])[0], "utf-8")
                                path = unicode(os.path.join(albumpath, trackname), "utf-8")
                                print name
                                self.insert("INSERT INTO music_track('albumid', 'position', 'name', 'path') VALUES(?,?,?,?)", [albumid, position, name, path])
                            elif "artwork" in trackname:
                                self.query("UPDATE music_album SET artwork = ? WHERE rowid = ?", [os.path.join(albumpath, trackname), albumid])