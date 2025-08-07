from flask import Flask, render_template, request, url_for, redirect
import logging

app = Flask(__name__)


@app.route('/')
def homepage():
    return render_template('index.html')
    # return "our site is live"

@app.route('/blogs', methods = ['GET', 'POST'] )
def blogs():


    return render_template('blogs.html')

@app.route('/contact', methods = ['GET', 'POST'] )
def contact():

#     if request.method == 'POST':
#         # name = request.form['name']
#         # email = request.form['email']
#         # logger = logging.logger(logging.DEBUG)
#         # handler = logging.FileHandler('info.log')
#         # formatter = logging.Formatter('%(message)s')
#         # handler.setFormatter(formatter)
#         # logger.addFileHandler(handler)

# #         logging.basicConfig(
# #         filename = 'info.log',
# #         filemode = 'w',
# #         level = logging.DEBUG,
# #         format = '%(asctime)s-%(name)s-%(levelname)s-%(message)s',
# #         datefmt= '%Y-%m-%d %H:%M:%S'
# # )
        


#         # logging.debug(name )
#         # logging.debug(email )
#         return redirect(url_for('projects'))
#     else:
     return render_template('contact.html')
    
@app.route('/projects', methods = ['GET', 'POST'] )
def projects():

    return render_template('projects.html')


@app.route('/collect_contact')
def collect_contact():
    if request.method == "POST":
        # name = request.form['name']
        # email = request.form['email']
        # # logger = logging.logger(logging.DEBUG)
        # # handler = logging.FileHandler('info.log')
        # # formatter = logging.Formatter('%(message)s')
        # # handler.setFormatter(formatter)
        # # logger.addFileHandler(handler)

        # logging.basicConfig(
        # filename = 'info.log',
        # filemode = 'w',
        # level = logging.DEBUG,
        # format = '%(asctime)s-%(name)s-%(levelname)s-%(message)s',
        # datefmt= '%Y-%m-%d %H:%M:%S')
        # logging.debug(name )
        # logging.debug(email )
        return 'Successfully logged'
    else:
        return 'not looged'


if __name__ == '__main__' :

    app.run(debug  = True)