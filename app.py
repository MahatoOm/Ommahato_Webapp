from flask import Flask, render_template, request, url_for, redirect, flash
import logging

app = Flask(__name__)
app.secret_key = "secret_key_here" # for flashing notification

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
        return 'not logged'
    

# for collecting user detail from contact.html
@app.route('/collectsubscribe', methods = ['POST', 'GET'])
def collectsubscribe():
    if request.method == "POST":
        

        name = request.form['Name']
        email = request.form['Email']
        message = request.form['Message']
        
        
        flash('Submission Sucessfull') # flashes notification of submission
        # return f'Your name is {name}, email is {email}, message is {message} '

        return redirect(url_for('contact'))
      
    else:
        return 'not logged'
    

def showNotifica():
    pass

@app.route('/portfolio')
def portfolio():
    return render_template('projects.html')

@app.route('/services')
def services():
    return 'Services'

    


if __name__ == '__main__' :

    app.run(debug  = True)