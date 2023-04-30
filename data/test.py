from requests import get, post, delete


# all jobs
print(get("http://127.0.0.1:5000/api/users").json())
print()
print(delete("http://127.0.0.1:5000/api/users/6").json())