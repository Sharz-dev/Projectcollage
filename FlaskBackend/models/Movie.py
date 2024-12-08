# creating the moive class
class Movie:
    def __init__(self,movieid:int, moviename: str, moviegenre: str, director: str, language: int):
        self.movieid=movieid
        self.moviename = moviename
        self.moviegenre = moviegenre
        self.director = director
        self.language = language
        