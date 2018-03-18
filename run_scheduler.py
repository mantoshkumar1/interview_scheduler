from setting import app, db
from task.employee import EmpLogic
from task.candidate import CandidateLogic

emp_logic = EmpLogic()
candidate_logic = CandidateLogic()

# generating SQLite database
with app.app_context():
    db.create_all()


@app.route('/')
def hello_world():
    return 'Application is up!'


@app.route("/emp_schedule", methods=['GET'])
# schedule detail of all employees
def get_emp_schedule():
    return emp_logic.get_emp_schedule()


# endpoint to add an employee schedule
@app.route("/emp_schedule", methods=['POST'])
def add_emp_schedule():
    return emp_logic.add_emp_schedule()

@app.route("/candidate_schedule", methods=['GET'])
# schedule detail of all candidates
def get_candidate_schedule():
    return candidate_logic.get_candidate_schedule()


# endpoint to add a candidate schedule
@app.route("/candidate_schedule", methods=['POST'])
def add_candidate_schedule():
    return candidate_logic.add_candidate_schedule()


if __name__ == '__main__':
    app.run(debug=True)
