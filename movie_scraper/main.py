from imdb import IMDb


###SAMPLE SCRIPT###
# create an instance of the IMDb class
ia = IMDb()

noir_movie = ia.search_movie("D.O.A (1949)")

print(noir_movie[0]["title"])
print(noir_movie[0].movieID)

doa = ia.get_movie(noir_movie[0].movieID)

for genre in doa['genres']:
    print(genre)
