"""Schema to define ToDo CRUD operations."""

import graphene
from graphene_django import DjangoObjectType
from django.db.models import Q

from .models import ToDo


class TodoType(DjangoObjectType):
    """A class to define the todo model."""

    class Meta:
        """Defines the behavior of the class."""

        model = ToDo


class Query(graphene.ObjectType):
    """A class to query all todos.

    ...

    Methods
    -------
    resolve_todos(info, search=None):
        Gets all created todo items

    resolve_todo_by_id(info, id):
        Gets details about a specified todo item

    """

    todos = graphene.List(TodoType, search=graphene.String())
    todo_by_id = graphene.Field(TodoType, id=graphene.Int())

    def resolve_todos(self, info, search=None):
        """Get all todos or all searched todos.

        Parameters
        ----------
        info: object
            Reference to meta information about the execution
            of the current GraphQL Query

            access to per-request context which can be used
            to store anything useful for resolving the query.

        search: str (default None)
            search parameter for searching todos

        Returns
        -------
        todos: list
            A list of all todo items or all searched todos

        """
        if search:
            filter_by = (
                Q(title__icontains=search)
                | Q(priority__icontains=search)
                | Q(status__icontains=search)
            )
            return ToDo.objects.filter(filter_by)
        return ToDo.objects.all()

    def resolve_todo_by_id(self, info, id):
        """Get details of the specified todo item.

        Parameters
        ----------
        info: object
            Reference to meta information about the execution
            of the current GraphQL Query

            access to per-request context which can be used
            to store anything useful for resolving the query.

        id: str
            id parameter for fetching a particular todo item

        Returns
        -------
        todo: object
            An object containing details of the specified todo item

        """
        return ToDo.objects.get(id=id)


class CreateTodo(graphene.Mutation):
    """A class to create a new todo item.

    Methods
    -------
    mutate(info, **kwargs):
        creates a new todo

    """

    todo = graphene.Field(TodoType)

    class Arguments:
        """Class arguments.

        Arguments
        ---------
        title: str
            The todo item title

        description: str
            The todo item description

        priority: str (default low)
            The todo item priority

        """

        title = graphene.String(required=True)
        description = graphene.String(required=True)
        priority = graphene.String(default_value="low")

    def mutate(self, info, **kwargs):
        """Create a new todo.

        Parameters
        ----------
        info:
            Reference to meta information about the execution
            of the current GraphQL Query

            access to per-request context which can be used
            to store anything useful for resolving the query.

        **kwargs: dict
            A dictionary of arguments

        Returns
        -------
        todo: object
            An object with the created todo details

        Raises
        ------
        GraphQLError:
            If user is not logged in

        """
        todo = ToDo(
            title=kwargs.get("title"),
            description=kwargs.get("description"),
            priority=kwargs.get("priority").upper(),
        )

        todo.save()

        return CreateTodo(todo=todo)


class UpdateTodo(graphene.Mutation):
    """A class to update todo information.

    ...

    Methods
    -------
    mutate(info, **kwargs):
        updates a specified todo information

    """

    todo = graphene.Field(TodoType)

    class Arguments:
        """Class arguments.

        Arguments
        ---------
        todo_id: int
            The ID of the todo item to update

        title: str (optional)
            The todo item title

        description: str (optional)
            The todo item description

        priority: str (optional)
            The todo item priority

        status: str (optional)
            The todo item status

        """

        todo_id = graphene.Int(required=True)
        title = graphene.String()
        description = graphene.String()
        priority = graphene.String()
        status = graphene.String()

    def mutate(self, info, **kwargs):
        """Update infomation about a todo item.

        Parameters
        ----------
        info:
            Reference to meta information about the execution
            of the current GraphQL Query

            access to per-request context which can be used
            to store anything useful for resolving the query.

        **kwargs: dict
            A dictionary of arguments

        Returns
        -------
        todo: object
            An object with the updated todo information

        Raises
        ------
        GraphQLError:
            If the current user didn't create the todo item / task

        """
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
    """A class to delete a todo item.

    ...

    Methods
    -------
    mutate(info, todo_id):
        deletes a todo item

    """

    todo_id = graphene.Int()

    class Arguments:
        """Class arguments.

        Arguments
        ---------
        todo_id: int
            The ID of the todo item to delete

        """

        todo_id = graphene.Int(required=True)

    def mutate(self, info, todo_id):
        """Delete a todo item.

        Parameters
        ----------
        info:
            Reference to meta information about the execution
            of the current GraphQL Query

            access to per-request context which can be used
            to store anything useful for resolving the query.

        todo_id: int
            The ID of the todo item to delete

        Returns
        -------
        todo_id: int
            The ID of the deleted todo item

        Raises
        ------
        GraphQLError:
            If the current user didn't create the todo item / task

        """
        todo = ToDo.objects.get(id=todo_id)

        todo.delete()

        return DeleteTodo(todo_id=todo_id)


class Mutation(graphene.ObjectType):
    """A class of all Mutations."""

    create_todo = CreateTodo.Field()
    update_todo = UpdateTodo.Field()
    delete_todo = DeleteTodo.Field()
