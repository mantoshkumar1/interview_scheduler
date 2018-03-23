# Interview Scheduler

This application allows interviewers and candidates to submit their time availabilities
for the<b>next week</b>through its RESTful API.

Based on the time availabilities of interviewers and candidates, this application can calculates
the mutually agreeable interview time slots.

# How to install the application software requirements:
<code> $ sudo pip install -r requirements.txt </code> <br>
 - This application has been developed and test on Ubuntu 16.04 LTS OS using Python2.7. For other OS platform, few instructions might need to be adapted.


# How to run the application
<code> $ cd scheduler </code> <br>
<code> $ export PYTHONPATH=$PWD </code> <br>
<code> $ python run_scheduler.py </code> <br>

# How to run a demo use case
First run the application in a terminal and execute the following command in another terminal
<code> cd scheduler </code>
<code> sh demo_usecase_run.sh </code>

# How to reset the application before its usage
<code> curl -d '{}' -H "Content-Type: application/json" -X POST http://localhost:5000/reset_scheduler </code>

Response
--------
```json
{
    "Status": "Content of previous week is deleted from DBs. Application is now ready for use."
}
```

# How does a candidate use the application through RESTful API

<code> curl -d '{"name":"Candidate Name", "email":"c1@gmail.com", "day": "Monday", "start_time": "13:20", "end_time": "14:00"}' -H "Content-Type: application/json" -X POST http://localhost:5000/candidate_schedule </code>
<br>

Response
--------
```json
{
    "candidate_id": 1,
    "day": "Monday",
    "end_time": "14:00",
    "start_time": "13:20"
}
```

A candidate can submit multiple time availabilities using this way.

# How does an interviewer use the application through RESTful API

<code> curl -d '{"name":"Interviewer Name", "email":"e1@gmail.com", "day": "Monday", "start_time": "13:20", "end_time": "14:00"}' -H "Content-Type: application/json" -X POST http://localhost:5000/emp_schedule </code>
<br>

Response
--------
```json
{
    "day": "Monday",
    "emp_id": 1,
    "end_time": "14:00",
    "start_time": "13:20"
}
```

An interviewer can submit multiple time availabilities using this way.

# How to evaluate the agreeable time schedule for a candidate with a list of interviewers
<code> curl -d '{"candidate_email": "candidate1@gmail.com", "interviewers_email": "interviewer1@gmail.com, interviewer2@gmail.com"}' -H "Content-Type: application/json" -X POST http://localhost:5000/schedule_interview </code>

<br><br>
An example of result returned by above POST RPC:
<br>

```json
{
    "candidate_email": "c1@gmail.com",
    "day": "Monday",
    "end_time": "14:30",
    "interviewers_emails": "e1@gmail.com, e2@gmail.com",
    "start_time": "12:30"
}
```

Notes regarding format of candidate_schedule, emp_schedule and schedule_interview form fields
--------------------------------------------------------------------------
All fields anticipates values in<b>string</b>format. <br>
<ul style="list-style-type:disc">
<li><b>"name"</b>: Name of a candidate or an interviewer, e.g; "Test Test".</li>
<li><b>"email"</b>: We trust users to provide a valid email address, e.g; "test@test.com".</li>
<li><b>"day"</b>: The value must belongs to one of these - "Monday", "Tuesday", "Wednesday", "Thursday", and "Friday".</li>
<li><b>"start_time"</b> and <b>"end_time"</b>:  Provide these values in 24 hours HH:MM format, e.g; "16:30" </li>
<li><b>"candidate_email"</b>: It must be a string</li>
<li><b>"interviewers_emails"</b>: The email addresses of interviewers should be seprated by comma</li>
</ul>  


