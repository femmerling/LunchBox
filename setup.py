from subprocess import call
import os.path
import sys

BASEDIR = os.path.abspath(os.path.dirname(__file__))
box_path = os.path.join(BASEDIR, 'box/')
app_config_path = os.path.join(BASEDIR, 'app.yaml')
flask_temp_path = os.path.join(box_path, 'flask-pkg/')
jinja_temp_path = os.path.join(box_path, 'jinja2-pkg/')
werkzeug_temp_path = os.path.join(box_path, 'werkzeug-pkg/')
flask_path = os.path.join(box_path, 'flask')
jinja_path = os.path.join(box_path, 'jinja2')
werkzeug_path = os.path.join(box_path, 'werkzeug')
app_name = None

if len(sys.argv) > 1:
    app_name = sys.argv[1].lower()

print "\nCreating boxes..."
call(['mkdir',flask_temp_path])
call(['mkdir',jinja_temp_path])
call(['mkdir',werkzeug_temp_path])

print "\nGetting Flask\n"
call(['git', 'clone', 'https://github.com/mitsuhiko/flask.git', flask_temp_path])
call(['ln','-s',flask_temp_path+'flask/',flask_path])

print "\nGetting Jinja2\n"
call(['git', 'clone', 'https://github.com/mitsuhiko/jinja2.git', jinja_temp_path])
call(['ln','-s',jinja_temp_path+'jinja2/',jinja_path])


print "\nGetting Werkzeug\n"
call(['git', 'clone', 'https://github.com/mitsuhiko/werkzeug.git', werkzeug_temp_path])
call(['ln','-s',werkzeug_temp_path+'werkzeug/',werkzeug_path])



if app_name:
	print "\nCreating config file\n"
	app_file = open(app_config_path, 'r')
	original_lines = app_file.readlines()
	original_lines[0] = 'application: '+app_name+"\n"
	app_file.close()
	app_file = open(app_config_path, 'w')
	for lines in original_lines:
		app_file.write(lines)
	app_file.close()

print "\nProcess done! Your EmeraldBox Package for AppEngine is ready to use"


