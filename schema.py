import graphene
from starwars.schema import Query as StarwarsQuery, Mutation as StarwarsMutation

class RootQuery(StarwarsQuery, graphene.ObjectType):
    pass

class RootMutation(StarwarsMutation, graphene.ObjectType):
    pass

schema = graphene.Schema(query=RootQuery, mutation=RootMutation)
