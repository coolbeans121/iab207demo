from flask import Blueprint, render_template, request, redirect, url_for, flash
from .models import Destination, Comment
from .forms import DestinationForm, CommentForm
from . import db
import os
from werkzeug.utils import secure_filename
#task 3 wk 12
from flask_login import login_required, current_user
#task 3 wk 12
from datetime import datetime



destbp = Blueprint('destination', __name__, url_prefix='/destinations')

@destbp.route('/<id>')
def show(id):
    destination = db.session.scalar(db.select(Destination).where(Destination.id==id))
    # create the comment form
    form = CommentForm()    
    return render_template('destinations/show.html', destination=destination, form=form)

#task 3 wk12
@destbp.route('/create', methods=['GET', 'POST'])
@login_required
def create():
  print('Method type: ', request.method)
  form = DestinationForm()
  if form.validate_on_submit():
    #call the function that checks and returns image
    db_file_path = check_upload_file(form)
    destination = Destination(name = form.name.data, description = form.description.data, 
    image=db_file_path,currency = form.currency.data)
    # add the object to the db session
    db.session.add(destination)
    # commit to the database
    db.session.commit()
    flash('Successfully created new travel destination', 'success')
    #Always end with redirect when form is valid
    return redirect(url_for('destination.create'))
  return render_template('destinations/create.html', form=form)

def check_upload_file(form):
  #get file data from form  
  fp = form.image.data
  filename = fp.filename
  #get the current path of the module file… store image file relative to this path  
  BASE_PATH = os.path.dirname(__file__)
  #upload file location – directory of this file/static/image
  upload_path = os.path.join(BASE_PATH, 'static/image', secure_filename(filename))
  #store relative path in DB as image location in HTML is relative
  db_upload_path = '/static/image/' + secure_filename(filename)
  #save the file and return the db upload path
  fp.save(upload_path)
  return db_upload_path

#task3 wk12
@destbp.route('/<id>/comment', methods = ['GET', 'POST'])  
@login_required
def comment(id):  
    form = CommentForm()
    now = datetime.now()
    date_time = now.strftime("%d/%m/%Y")  
    #get the destination object associated to the page and the comment
    destination = db.session.scalar(db.select(Destination).where(Destination.id==id))
    if form.validate_on_submit():  
      #task 3 wk 12
      comment = Comment(text=form.text.data, destination=destination,
                        user=current_user, created_at=date_time) 
      #here the back-referencing works - comment.destination is set
      # and the link is created
      db.session.add(comment) 
      db.session.commit() 
      #flashing a message which needs to be handled by the html
      flash('Your comment has been added', 'success')  
      # print('Your comment has been added', 'success') 
    # using redirect sends a GET request to destination.show
    return redirect(url_for('destination.show', id = id))
