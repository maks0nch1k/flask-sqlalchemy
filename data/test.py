from requests import get, post, delete


# all jobs
print(get("http://127.0.0.1:5000/api/v2/jobs").json())

# add a user
print(post("http://127.0.0.1:5000/api/v2/jobs",
           json={"team_leader": 3,
                 "job": "Job1",
                 "work_size": 23,
                 "collaborators": "2, 6, 8, 9",
                 "is_finished": True
                 }).json())

# current job
print(get("http://127.0.0.1:5000/api/v2/jobs/2").json())

# delete job
print(delete("http://127.0.0.1:5000/api/v2/jobs/2").json())

# missing id
print(delete("http://127.0.0.1:5000/api/v2/jobs/4767867654").json())

# str instead of int
print(delete("http://127.0.0.1:5000/api/v2/jobs/fdadsa").json())

# absence of a parametr
print(post('http://127.0.0.1:5000/api/v2/jobs',
           json={"id": 13,
                 'team_leader': 5,
                 "collaborators": "1, 3, 4, 7",
                 "is_finished": 1}).json())

# used id
print(post('http://127.0.0.1:5000/api/v2/jobs',
           json={"id": 1,
                 'team_leader': 5,
                 'job': 3,
                 "work_size": 343,
                 "collaborators": "1, 3, 4, 7",
                 "is_finished": 1}).json())
