import orm


class Movies(orm.Model):
    id = orm.IdField()
    movies_name = orm.CharField(max_length=255)
    actors_name = orm.TextField(null=True)
    genres = orm.CharField(max_length=200)
    date_of_issue = orm.IntegerField(null=True)
    rates = orm.FloatField()


print(Movies())
new_data = {'movies_name': '', 'actors_name': '', 'genres': '', 'date_of_issue': '2000', 'rates': 9.9}
# Movies.object.insert(movies_name='', actors_name='', genres='', rates=8.8)
# print(Movies.object.select('movies_name', 'actors_name'))
# print(Movies.object.select('movies_name', 'actors_name', movies_name='nhbh'))
# Movies.object.update(new_data, movies_name='')
# Movies.object.update(new_data)
# Movies.object.delete()
# Movies.object.delete(id=162)
# print(Movies.object.all())
