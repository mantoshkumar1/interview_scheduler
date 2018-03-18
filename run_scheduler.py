from setting import app, db
from task.employee import EmpLogic
#from model.employee import EmployeeScheduleSchema

emp_logic = EmpLogic()
#employee_schema = EmployeeScheduleSchema()
#employees_schema = EmployeeScheduleSchema(many=True)

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


if __name__ == '__main__':
    app.run(debug=True)
