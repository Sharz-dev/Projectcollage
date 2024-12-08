#Creating the Rating class        
class Rating:
    def __init__(self,rateid:str,userid:str,movieid:str,rating:str):
        self.rateid=rateid
        self.userid=userid
        self.movieid=movieid
        self.rating=rating