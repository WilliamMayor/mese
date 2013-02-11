from flask import render_template
from flask import request
from Database import Database

class Music:
    
    def __init__(self, artist=None, album=None, song=None):
        self.artist = artist
        self.album = album
        self.song = song

    def render(self):
        if self.song:
            return "You chose %s from %s's %s album" % (self.song, self.artist, self.album)
        elif self.album:
            return render_template('music/tracks.html', tracks=self.getTracks(self.album), slim=request.args.get('slim', False))
        elif self.artist:
            return render_template('music/albums.html', albums=self.getAlbums(self.artist), slim=request.args.get('slim', False))
        else:
            return render_template('music/artists.html', artists=self.getArtists(), slim=request.args.get('slim', False))

    def getArtists(self):
        return Database().query("SELECT rowid, * FROM music_artist")

    def getAlbums(self, artistid):
        return Database().query("SELECT rowid, * FROM music_album WHERE artistid = ?", [artistid])

    def getTracks(self, albumid):
        return Database().query("SELECT rowid, * FROM music_track WHERE albumid = ? ORDER BY position", [albumid])
        