# Description

API for managing Course entity with CRUD endpoints, created for Yalantis Python School

## Requirements

Ubuntu 20.04.1 LTS \
Docker 20.10.6 

## Installation
```
sudo bash start.sh
```

Actions:

1) Remove old image, containers, pycache and db
2) Install libs
3) Run tests
4) Run application

## Usage

You may access the app on your local browser by using

```
http://127.0.0.1:5000
```
You may run queries in-browser interface or do it with the help of python, only requests library is required
### Available endpoints and examples
1)
courses/add_course
 ```
import requests
domain = 'http://127.0.0.1:5000'
data = {
      "title": "Yalantis Python School",
      "start_date": "17-05-2021",
      "end_date": "30-08-2021",
      "lectures_count": 22
  }
response = requests.post(domain + '/courses/add_course', json=data)
course_id = response.json()['id']
 ```
2)
courses/get_courses_by_attribute
 ```
import requests
domain = 'http://127.0.0.1:5000'
query_string = {
     "title": "Yalantis Python School",
     "start_date": "17-05-2021",
     "end_date": "19-05-2021"
 }
response = requests.get(domain + '/courses/get_courses_by_attribute', params=query_string)
filtered_cources = response.json()
 ```

3)
courses/change_attributes
```

import requests
# course id from example 1
course_id = 1
domain = 'http://127.0.0.1:5000'
new_attributes = {
      "title": "new_title",
      "lectures_count": 322
  }
requests.post(domain + f'/courses/change_attributes/{course_id}', json=new_attributes)

```

4)
courses/get_courses_list
```
import requests
domain = 'http://127.0.0.1:5000'
response = requests.get(domain + '/courses/get_courses_list')
print(response.json())
```

5)
courses/delete_course
```
import requests
# course id from example 1
course_id = 1
domain = 'http://127.0.0.1:5000'
requests.delete(domain + f'/courses/delete_course/{course_id}')
```

# P.S.

## Explanation about get_courses_by_attribute

1) You can combine filters
2) Date filters work like range filters Example:
   DB has 3 records -
   ```   
   {"id":1,"start_date":"10-05-2021","end_date": "15-05-2021"}\
   {"id":1,"start_date":"14-05-2021","end_date": "18-05-2021"}\
   {"id":1,"start_date":"20-05-2021","end_date": "25-05-2021"}\
   ```
   If you pass filters -
   ```
   {"start_date":"13-05-2021","end_date": "16-05-2021"}
   ```
   API will return - 
   ```
   {"id":1,"start_date":"10-05-2021","end_date": "15-05-2021"}\
   {"id":1,"start_date":"14-05-2021","end_date": "18-05-2021"}\
   ```
   Because only these records match the date range that is defined in filters

3) You can see tests and API logs in tests.log and api.log
