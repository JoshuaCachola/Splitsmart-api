import json

from graphene.test import Client

from src.schema import schema


def test_register_user():
    """
    Tests registering a user
    """
    client = Client(schema)
    mut_str = """
         mutation registerUser(
            $firstName: String!, $lastName: String!, $email: String!,
            $password: String!) {
                registerUser(firstName: $firstName, lastName: $lastName,
                email: $email, password: $password) {
                    user {
                        id
                    }
                    authToken

                }
            }
    """
    variables = {
        "firstName": "test",
        "lastName": "user",
        "email": "test@user.com",
        "password": "test_password"
    }
    executed = client.execute(mut_str, variable_values=variables)
    assert "data" in executed
