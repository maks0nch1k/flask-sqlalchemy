from requests import get, post, delete


# all users
print(get("http://127.0.0.1:5000/api/v2/users").json())

# add a user
print(post("http://127.0.0.1:5000/api/v2/users",
           json={"name": "User_name_1",
                 "surname": "User_surname_1",
                 "age": 23,
                 "position": "Mars",
                 "speciality": "programmer",
                 "address": "qwerty",
                 "hashed_password": "sdadasdas",
                 "email": "E@e",
                 "city_from": "Lima"
                 }).json())

# current user
print(get("http://127.0.0.1:5000/api/v2/users/2").json())

# delete user
print(delete("http://127.0.0.1:5000/api/v2/users/6"))

# wrong add user (missing password and not int age)
print(post("http://127.0.0.1:5000/api/v2/users",
           json={"name": "User_name_1",
                 "surname": "User_surname_1",
                 "age": "sdadasdas",
                 "position": "Mars",
                 "speciality": "programmer",
                 "address": "qwerty",
                 "email": "E@e",
                 "city_from": "Lima"
                 }).json())

# get missing user
print(get("http://127.0.0.1:5000/api/v2/users/445645456456").json())

# delete missing user
print(delete("http://127.0.0.1:5000/api/v2/users/44456456456"))

# get user not int id
print(get("http://127.0.0.1:5000/api/v2/users/asdasda").json())

# delete user not int id
print(delete("http://127.0.0.1:5000/api/v2/users/sadasdad"))
