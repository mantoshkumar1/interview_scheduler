#!/bin/sh

# Description: This file contains series of RPC calls that test Interview Scheduler application

# resetting dbs
curl -d '{}' -H "Content-Type: application/json" -X POST http://localhost:5000/reset_scheduler

# sending schedules choices of candidate 1
curl -d '{"name":"Candidate 1", "email":"c1@gmail.com", "day": "Monday", "start_time": "12:30", "end_time": "14:30"}' -H "Content-Type: application/json" -X POST http://localhost:5000/candidate_schedule
curl -d '{"name":"Candidate 1", "email":"c1@gmail.com", "day": "Monday", "start_time": "14:00", "end_time": "15:00"}' -H "Content-Type: application/json" -X POST http://localhost:5000/candidate_schedule
curl -d '{"name":"Candidate 1", "email":"c1@gmail.com", "day": "Tuesday", "start_time": "10:00", "end_time": "12:00"}' -H "Content-Type: application/json" -X POST http://localhost:5000/candidate_schedule
curl -d '{"name":"Candidate 1", "email":"c1@gmail.com", "day": "Tuesday", "start_time": "14:00", "end_time": "15:00"}' -H "Content-Type: application/json" -X POST http://localhost:5000/candidate_schedule

# sending schedules choices of candidate 2
curl -d '{"name":"Candidate 2", "email":"c2@gmail.com", "day": "Tuesday", "start_time": "12:30", "end_time": "14:00"}' -H "Content-Type: application/json" -X POST http://localhost:5000/candidate_schedule
curl -d '{"name":"Candidate 2", "email":"c2@gmail.com", "day": "Tuesday", "start_time": "14:00", "end_time": "16:00"}' -H "Content-Type: application/json" -X POST http://localhost:5000/candidate_schedule
curl -d '{"name":"Candidate 2", "email":"c2@gmail.com", "day": "Wednesday", "start_time": "10:00", "end_time": "12:00"}' -H "Content-Type: application/json" -X POST http://localhost:5000/candidate_schedule
curl -d '{"name":"Candidate 2", "email":"c2@gmail.com", "day": "Wednesday", "start_time": "14:00", "end_time": "15:00"}' -H "Content-Type: application/json" -X POST http://localhost:5000/candidate_schedule

# sending schedules choices of interviewer 1
curl -d '{"name":"Emp 1", "email":"e1@gmail.com", "day": "Monday", "start_time": "10:00", "end_time": "15:00"}' -H "Content-Type: application/json" -X POST http://localhost:5000/emp_schedule
curl -d '{"name":"Emp 1", "email":"e1@gmail.com", "day": "Monday", "start_time": "18:00", "end_time": "20:00"}' -H "Content-Type: application/json" -X POST http://localhost:5000/emp_schedule
curl -d '{"name":"Emp 1", "email":"e1@gmail.com", "day": "Thursday", "start_time": "10:00", "end_time": "11:00"}' -H "Content-Type: application/json" -X POST http://localhost:5000/emp_schedule
curl -d '{"name":"Emp 1", "email":"e1@gmail.com", "day": "Thursday", "start_time": "13:00", "end_time": "14:00"}' -H "Content-Type: application/json" -X POST http://localhost:5000/emp_schedule

# sending schedules choices of interviewer 2
curl -d '{"name":"Emp 2", "email":"e2@gmail.com", "day": "Monday", "start_time": "12:30", "end_time": "14:30"}' -H "Content-Type: application/json" -X POST http://localhost:5000/emp_schedule
curl -d '{"name":"Emp 2", "email":"e2@gmail.com", "day": "Monday", "start_time": "18:00", "end_time": "20:00"}' -H "Content-Type: application/json" -X POST http://localhost:5000/emp_schedule
curl -d '{"name":"Emp 2", "email":"e2@gmail.com", "day": "Friday", "start_time": "20:00", "end_time": "22:00"}' -H "Content-Type: application/json" -X POST http://localhost:5000/emp_schedule
curl -d '{"name":"Emp 2", "email":"e2@gmail.com", "day": "Friday", "start_time": "00:00", "end_time": "02:00"}' -H "Content-Type: application/json" -X POST http://localhost:5000/emp_schedule

# calculating interview schedule time
curl -d '{"candidate_email": "c1@gmail.com", "interviewers_email": "e1@gmail.com, e2@gmail.com"}' -H "Content-Type: application/json" -X POST http://localhost:5000/schedule_interview
curl -d '{"candidate_email": "c2@gmail.com", "interviewers_email": "e1@gmail.com, e2@gmail.com"}' -H "Content-Type: application/json" -X POST http://localhost:5000/schedule_interview
