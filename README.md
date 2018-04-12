# Interview Scheduler

This application allows interviewers and candidates to submit their time availabilities for the <b>next week</b> (only) through its RESTful API.
Based on the time availabilities of interviewers and candidates, this application calculates the mutually agreeable interview time slots.

## How to install the application software requirements:
<code> $ cd interview_scheduler </code> <br>
<code> $ sudo -H pip install -r requirements.txt </code><br>
This application has been developed and test on Ubuntu 16.04 LTS OS using Python2.7. For other OS platform, few instructions might need to be adapted.


## How to run the application server
<code> $ cd interview_scheduler </code> <br>
<code> $ export PYTHONPATH=$PWD </code> <br>
<code> $ python run_scheduler.py </code> <br>

## REST API Endpoints

#### How to reset the application before its usage
<code> $ curl -d '{}' -H "Content-Type: application/json" -X POST http://localhost:5000/reset_scheduler </code>

URI: http://localhost:5000/reset_scheduler<br>
Method: POST<br>
Content-Type: application/json<br>
Body:
```json
{ }
```

Response:
```json
{
    "Status": "Content of previous week is deleted from DBs. Application is now ready for use."
}
```

#### How does a candidate submit his time availability to the application through RESTful API
<code> $ curl -d '{"name":"Candidate Name", "email":"c1@gmail.com", "day": "Monday", "start_time": "13:20", "end_time": "14:00"}' -H "Content-Type: application/json" -X POST http://localhost:5000/candidate_schedule </code>
<br>

URI: http://localhost:5000/candidate_schedule<br>
Method: POST<br>
Content-Type: application/json<br>
Body:
```json
{
    "name": "Candidate Name",
    "email": "candidate1@gmail.com",
    "day": "Monday",
    "start_time": "13:20",
    "end_time": "14:00"
}
```

Response:
```json
{
    "candidate_id": 1,
    "day": "Monday",
    "end_time": "14:00",
    "start_time": "13:20"
}
```

A candidate can submit multiple time availabilities in the similar manner.

#### How to get the submitted time availabilities of all candidates through RESTful API
<code> $ curl -X GET http://localhost:5000/candidate_schedule</code><br>

URI: http://localhost:5000/candidate_schedule<br>
Method: GET<br>
Response:
```json
{
    "candidates_schedules": [
        {
            "candidate_id": 1,
            "day": "Monday",
            "end_time": "14:00",
            "start_time": "13:20"
        }
    ]
}
```

#### How does an interviewer submit his time availability to the application through RESTful API
<code> $ curl -d '{"name":"Interviewer Name", "email":"e1@gmail.com", "day": "Monday", "start_time": "13:20", "end_time": "14:00"}' -H "Content-Type: application/json" -X POST http://localhost:5000/emp_schedule </code>
<br>

URI: http://localhost:5000/emp_schedule<br>
Method: POST<br>
Content-Type: application/json<br>
Body:
```json
{
    "name": "Interviewer Name",
    "email": "interviewer1@gmail.com",
    "day": "Monday",
    "start_time": "13:20",
    "end_time": "14:00"
}
```

Response:
```json
{
    "day": "Monday",
    "emp_id": 1,
    "end_time": "14:00",
    "start_time": "13:20"
}
```

An interviewer can submit multiple time availabilities in the similar manner.

#### How to get the submitted time availabilities of all interviewers through RESTful API
<code> $ curl -X GET http://localhost:5000/emp_schedule</code><br>

URI: http://localhost:5000/emp_schedule<br>
Method: GET<br>
Response:
```json
{
    "employees_schedules": [
        {
            "day": "Monday",
            "emp_id": 1,
            "end_time": "14:00",
            "start_time": "13:20"
        }
    ]
}
```

#### How to evaluate the agreeable time schedule for a candidate with a list of interviewers
<code> $ curl -d '{"candidate_email": "candidate1@gmail.com", "interviewers_email": "interviewer1@gmail.com, interviewer2@gmail.com"}' -H "Content-Type: application/json" -X POST http://localhost:5000/schedule_interview </code>

URI: http://localhost:5000/schedule_interview<br>
Method: POST<br>
Content-Type: application/json<br>
Body:
```json
{
    "candidate_email": "candidate1@gmail.com",
    "interviewers_email": "interviewer1@gmail.com, interviewer2@gmail.com"
}
```

A sample of response returned by above POST RPC:
```json
{
    "candidate_email": "candidate1@gmail.com",
    "day": "Monday",
    "end_time": "14:30",
    "interviewers_emails": "interviewer1@gmail.com, interviewer2@gmail.com",
    "start_time": "12:30"
}
```

#### How to get the already scheduled interviews through RESTful API
<code> $ curl -X GET http://localhost:5000/schedule_interview</code><br>
URI: http://localhost:5000/schedule_interview<br>
Method: GET<br>
Response:
```json
{
    "scheduled_interviews": [
        {
            "candidate_email": "candidate1@gmail.com",
            "day": "Monday",
            "end_time": "14:30",
            "interviewers_emails": "interviewer1@gmail.com, interviewer2@gmail.com",
            "start_time": "12:30"
        }
    ]
}
```

## HTTP Error Codes
400, 403, 404, 409, 500

## How to run a demo use case
First run the application server in a terminal and execute the following command in another terminal. <br>
<code>$ cd interview_scheduler </code> <br>
<code>$ sh demo_usecase_run.sh </code>

## How to execute unit tests for the application
<code>$ cd interview_scheduler</code><br>
<code>$ python -m unittest discover</code>

## Notes regarding format of candidate_schedule, emp_schedule and schedule_interview form fields
All fields anticipates values in <b>string</b> format. <br>
<ul style="list-style-type:disc">
<li><b>"name"</b>: Name of a candidate or an interviewer, e.g; "Test Test".</li>
<li><b>"email"</b>: We trust users to provide a valid email address, e.g; "test@test.com".</li>
<li><b>"day"</b>: The value must belongs to one of these - "Monday", "Tuesday", "Wednesday", "Thursday", or "Friday".</li>
<li><b>"start_time"</b> and <b>"end_time"</b>:  Provide these values in 24 hours HH:MM format, e.g; "05:30" </li>
<li><b>"candidate_email"</b>: It must be a string</li>
<li><b>"interviewers_emails"</b>: The email addresses of interviewers should be seprated by comma</li>
</ul>  


