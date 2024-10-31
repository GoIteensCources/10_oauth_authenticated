from werkzeug.security import generate_password_hash

fake_users_db = {
    "johndoe": {
        "username": "johndoe",
        "full_name": "John Doe",
        "email": "johndoe@example.com",
        "hashed_password": generate_password_hash("secret"),
        "disabled": False,
        "is_admin": True,
    },
    "alice": {
        "username": "alice",
        "full_name": "Alice Wonderson",
        "email": "alice@example.com",
        "hashed_password":  generate_password_hash("secret2"),
        "disabled": True,
        "is_admin": False,
    },
}
