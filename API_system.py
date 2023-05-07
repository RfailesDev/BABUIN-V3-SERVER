import variables


def account_exists(secret_key):
    return secret_key in variables.USERS_DATABASE