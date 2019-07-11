from flask import Flask, request
import os
import jinja2

app = Flask(__name__)
app.config['DEBUG'] = True

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir), autoescape=True)

# user details
# I know that, in the context of this assignment, we could keep this within the scope 
# of the index method, but in a real-world scenario, that might not be desirable. 
user_name = ''
password = ''
email = ''

def validate_element(string_to_validate, element_name, error_string):
    if len(string_to_validate) < 3 or len(string_to_validate) > 20:
        error_string = "length of " + element_name + " out of bounds (minimum 3, maximum 20)"
    if " " in string_to_validate:
        if len(error_string) > 0:
            error_string += '; '
        error_string += "spaces in " + element_name + " are not allowed."
    if element_name == "email address":
        if string_to_validate.count("@") != 1 or string_to_validate.count(".") != 1:
            if len(error_string) > 0:
                error_string += ';'
            error_string += "one '.' and one '@' (no less or more than 1) required in email address"
    return error_string


@app.route('/', methods=['GET', 'POST'])
def index():
    signup_template = jinja_env.get_template('signup.html')
    if request.method == 'GET':
        return signup_template.render()
    else:
        user_name_error = ''
    password_error = ''
    password_verification_error = ''
    email_error = ''
    user_name = request.form['username']
    password = request.form['password']
    verify_password = request.form['verify']
    email = request.form['email']

    user_name_error = validate_element(user_name, "user name", user_name_error)
    password_error = validate_element(password, "password", password_error)
    if verify_password != password: 
        password_verification_error += "passwords do not match."
    email_error = validate_element(email, "email address", email_error)
    

    if len(user_name_error) > 0 or len(password_error) > 0 or len(password_verification_error) > 0 or len(email_error) > 0:
        return signup_template.render(username = user_name, 
        userNameError = user_name_error,
        passwordError = password_error,
        passwordVerificationError = password_verification_error,
        email = email,
        emailError = email_error)
    else:
        return '<h1>Welcome, ' + user_name + '!</h1>'

app.run()