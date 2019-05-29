import os
from flask import Flask, render_template, redirect, request, url_for
from flask_pymongo import PyMongo
from bson.objectid import ObjectId


app = Flask(__name__)
app.config["MONGO_DBNAME"] = 'task_manager'
app.config["MONGO_URI"] = 'mongodb+srv://root:rOOtUser@myfirstcluster-2whkw.mongodb.net/task_manager?retryWrites=true'

mongo = PyMongo(app)

@app.route('/')
@app.route('/get_tasks')
def get_tasks():
    return render_template("tasks.html", 
                           tasks=mongo.db.tasks.find())


@app.route('/add_task')
def add_task():
    return render_template('addtask.html',
                           categories=mongo.db.categories.find())


@app.route('/insert_task', methods=['POST'])
def insert_task():
    tasks =  mongo.db.tasks
    tasks.insert_one(request.form.to_dict())
    return redirect(url_for('get_tasks'))


@app.route('/edit_task/<task_id>')
def edit_task(task_id):
    the_task =  mongo.db.tasks.find_one({"_id": ObjectId(task_id)})
    all_categories =  mongo.db.categories.find()
    return render_template('edittask.html', task=the_task,
                           categories=all_categories)


@app.route('/update_task/<task_id>', methods=["POST"])
def update_task(task_id):
    tasks = mongo.db.tasks
    tasks.update( {'_id': ObjectId(task_id)},
    {
        'task_name':request.form.get('task_name'),
        'category_name':request.form.get('category_name'),
        'task_description': request.form.get('task_description'),
        'due_date': request.form.get('due_date'),
        'is_urgent':request.form.get('is_urgent')
    })
    return redirect(url_for('get_tasks'))
    
    
@app.route('/delete_task/<task_id>')
def delete_task(task_id): 
# we access the tasks collection and we call remove and we pass in the task_id as the parameter. 
# Key value pair inside the curly braces.We use the object ID to format or parse the task ID in a way that's acceptable to Mongo.
# Once that's in place, we want to return or redirect.So we redirect to get tasks.
# Why?
# Because once that function is complete, we want to see it disappear. We want visual evidence to see that that task is no longer on our list.
# So we redirect to the get_tasks function.
    mongo.db.tasks.remove({'_id': ObjectId(task_id)})
    return redirect(url_for('get_tasks'))


@app.route('/get_categories')
def get_categories():
    return render_template('categories.html',
                           categories=mongo.db.categories.find())


@app.route('/delete_category/<category_id>')
def delete_category(category_id):
    mongo.db.categories.remove({'_id': ObjectId(category_id)})
    return redirect(url_for('get_categories'))
    
    
@app.route('/edit_category/<category_id>')
def edit_category(category_id):
    return render_template('editcategory.html',
    category=mongo.db.categories.find_one({'_id': ObjectId(category_id)}))
    

@app.route('/update_category/<category_id>', methods=['POST'])
def update_category(category_id):
    mongo.db.categories.update(
        {'_id': ObjectId(category_id)},
        {'category_name': request.form.get('category_name')})
    return redirect(url_for('get_categories'))
    
    
@app.route('/insert_category', methods=['POST'])
def insert_category():
    # accessing mongoDB data base in preperstion of the insert. category_doc is creating a new BSON formatted doc. 
    category_doc = {'category_name': request.form.get('category_name')}
    # adding the category doc into the catergory table.
    mongo.db.categories.insert_one(category_doc)
    # then return a redirect back to categories.
    return redirect(url_for('get_categories'))
    
# the function that will direct us and render the view that allows us to add a new category in the first place.
@app.route('/add_category')
def add_category():
    return render_template('addcategory.html')


if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
        port=int(os.environ.get('PORT')),
        debug=True)
