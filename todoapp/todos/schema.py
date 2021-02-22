import graphene
from graphene_django import DjangoObjectType
from django.db.models import Q

from .models import ToDo


class TodoType(DjangoObjectType):
    class Meta:
        model = ToDo


class Query(graphene.ObjectType):
    todos = graphene.List(TodoType, search=graphene.String())
    todo_by_id = graphene.Field(TodoType, id=graphene.Int())

    def resolve_todos(self, info, search=None):
        if search:
            filter_by = (
                Q(title__icontains=search)
                | Q(priority__icontains=search)
                | Q(status__icontains=search)
            )
            return ToDo.objects.filter(filter_by)
        return ToDo.objects.all()

    def resolve_todo_by_id(self, info, id):
        return ToDo.objects.get(id=id)


class CreateTodo(graphene.Mutation):
    todo = graphene.Field(TodoType)

    class Arguments:
        title = graphene.String(required=True)
        description = graphene.String(required=True)
        priority = graphene.String(default_value="low")

    def mutate(self, info, **kwargs):
        todo = ToDo(
            title=kwargs.get("title"),
            description=kwargs.get("description"),
            priority=kwargs.get("priority").upper(),
        )

        todo.save()

        return CreateTodo(todo=todo)


class UpdateTodo(graphene.Mutation):
    todo = graphene.Field(TodoType)

    class Arguments:
        todo_id = graphene.Int(required=True)
        title = graphene.String()
        description = graphene.String()
        priority = graphene.String()
        status = graphene.String()

    def mutate(self, info, **kwargs):
        todo = ToDo.objects.get(id=kwargs.get("todo_id"))
        todo.title = kwargs.get("title") or todo.title
        todo.description = kwargs.get("description") or todo.description
        todo.priority = (
            kwargs.get("priority").upper() if kwargs.get("priority") else todo.priority
        )
        todo.status = (
            kwargs.get("status").upper() if kwargs.get("status") else todo.status
        )

        todo.save()

        return CreateTodo(todo=todo)


class DeleteTodo(graphene.Mutation):
    todo_id = graphene.Int()

    class Arguments:
        todo_id = graphene.Int(required=True)

    def mutate(self, info, todo_id):
        todo = ToDo.objects.get(id=todo_id)

        todo.delete()

        return DeleteTodo(todo_id=todo_id)


class Mutation(graphene.ObjectType):
    create_todo = CreateTodo.Field()
    update_todo = UpdateTodo.Field()
    delete_todo = DeleteTodo.Field()
