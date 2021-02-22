import graphene
import users.schema
import todos.schema


class Query(users.schema.Query, todos.schema.Query, graphene.ObjectType):
    pass


class Mutation(users.schema.Mutation, todos.schema.Mutation, graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)