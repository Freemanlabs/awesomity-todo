# Todo API - Awesomity Challenge
The implemented API is a [GraphQL](https://graphql.org/) based API, implemented in Python and utilizing the [Django](https://www.djangoproject.com/) Framework. A major advantage of [GraphQL](https://graphql.org/) compared to REST is solving the problem of *overfetching*. In GraphQL you dont have to fetch all the data within an endpoint. You basically retrieve the data you *need* from an endpoint.

## Features
1. CRUD todo items
2. Search
3. User Authentication

## Requirements
1. [pipenv](https://pipenv-fork.readthedocs.io/en/latest/install.html#installing-pipenv)

    Similar to virtualenv, we use pipenv to create and work within our virtual environment. To install, run
    
    `pip install pipenv`

2. [Insomnia](https://insomnia.rest/download/core/) OR [Postman](https://www.postman.com/)

    However, for the rest of this documentation we would be working with Insomnia. You can download [insomnia](https://insomnia.rest/download/core/) for your OS from this [link](https://insomnia.rest/download/core/). Insomnia is the recommended client for testing GrapghQL APIs.


## Steps to Reproduce
1. Clone the github repo
2. `cd` to where you have the cloned directory. E.g. **all-todo-apis**
3. run `pipenv shell` from your terminal to create a virtual environment for your project. You know you are in your virtual environment if you see the name of the present directory (where the cloned files are) in brackets. 
    
    E.g. If I have all submissions in a directory called **all-todo-apis**, my terminal looks like the following:
    ```
    (all-todo-apis) ~/path/to/all-todo-apis
    ```
4. In your virtual environment, run `pipenv install`. This installs all the dependencies in the pipfile and the piplock file in your virtual environment.
5. Still within your virtual environment, `cd` to `todoapi` which contains the main project code.
6. Run
    ```
    python manage.py runserver
    ```
   This creates a development server with a URL. E.g. `http://127.0.0.1:8000/`
   
   
## Working with insomnia
Insomnia is a *simple* API client for REST, GraphQL and gRPC.


![authentication](https://res.cloudinary.com/freeman/image/upload/v1614107092/github-readme/awesomity/insomnia-client.png)

1. Open insomnia *(already installed on your PC)*
2. Select **New Request**
3. Select the **Body** dropdown and choose **GraphQL Query**
4. By default, every request in GraphQL is a `POST` request, so you should see the `POST` option at the top (beside the URL bar)
5. Copy and paste the earlier created development server url + */graphql/* into the address bar like so `http://127.0.0.1:8000/graphql/` in the Insomnia client and hit `send`.

## Working with GraphQL
A major advantage of [GraphQL](https://graphql.org/) compared to REST is solving the problem of *overfetching*. In GraphQL you dont have to fetch all the data within an endpoint. You basically retrieve the data you *need* from an endpoint.

GraphQL has two major operations. *Queries* and *Mutations*

### Queries
A query is simply a **Read** operation. 

#### Read
For example, to see **all todos** created, we use the following code"
```
query{
  todos{
    id
    title
    description
    priority
    status
    createdBy{
      id
      username
    }
    createDate
    modifiedDate
  }
}
```
Unlike REST, In GraphQL, you fetch the data you want and not all data within the endpoint. For example. To search for todos by **title, priority or status**, in which we require only the title and piority of the todo, GraphQl makes that possible. 

For example to search for all todos with low priority, we do:
```
query{
  todos(search:"low"){
    title
    priority
  }
}
```

To search for a particular todo item by **ID**, we can use the following code:
```
query{
  todoById(id:3){
    id
    title
    description
    priority
    status
    createDate
  }
}
```

### Mutation
In GraphQL, a mutation is simply a write operation **(Create, Update, Delete)**.

Before we create a new todo item, we want to make sure a user is registered and authenticated, since ideally, a guest user cannot create a todo item, nor can they update or delete.

To register a new user, we do:
```
mutation{
  register(firstName:"firstname", lastName:"lastname", username:"username", email:"email", password:"password", password2:"password2"){
    user{
      id
      firstName
      lastName
      username
      email
    }
  }
}
```
After a user is regirstered, to login, we generate a token (that can be stored in a local storage on the frontend). To do this , we do:
```
mutation{
  tokenAuth(email: "yourregistered@email.com", password:"yourpassword"){
    token
  }
}
```

The result looks like the following:
```
{
  "data": {
    "tokenAuth": {
      "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VybmFtZSI6ImN5dXN1ZiIsImV4cCI6MTYxNDEwNTgyMiwib3JpZ0lhdCI6MTYxNDEwNTUyMn0.F5w-ZSJDNEWYnjNgImWDbcSxNs_r9GtsqiRlgOjQJJ4"
    }
  }
}
```

As with every other API client, we want to make sure this token is recognized in our header. To do that we go back to *Insomnia*, on the header section, under the *Authorization* field, type `JWT` *[space]* `followed by your token`. Like the image below

![authentication](https://res.cloudinary.com/freeman/image/upload/v1614106312/github-readme/awesomity/authentication.png)

Once you are set up, we can continue with the rest of the operations.

#### Create
Next, to create a **new todo**, we use the following code"
```
mutation{
  createTodo(title: "todo-title", description: "todo-description", priority:"todo-priority"){
    todo{
      id
      title
    }
  }
}
```
By default, the *priority* field is set to **low** if not specified. The rest argument are required.

#### Update
To update a todo item, simply specify the todo *ID* and specify the field to update. Like so,

```
mutation{
  updateTodo(todoId:2, priority:"high"){
    todo{
      title
      priority
    }
  }
}
```

#### Delete
To delete a todo item, simply specify the todo *ID*, Like so,

```
mutation{
  deleteTodo(todoId:5){
    todoId
  }
}
```


*Thank you all for reading. Please, feel free to open an issue for any issue at all such as bugs, questions, suggestions, etc*
