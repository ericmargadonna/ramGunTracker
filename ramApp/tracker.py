from flask import Blueprint, flash, g, redirect, render_template, request, session, url_for
from ramApp.db import get_db
from ramApp.auth import login_required

bp = Blueprint('tracker', __name__)

@bp.route('/')
@login_required
def index():
    return render_template('tracker/index.html')

@bp.route('/createshipment',methods=('GET','POST'))
@login_required
def createshipment():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        key = request.form['key']
        db = get_db()
        error = None


        #Create shipment logic
        pass
    return render_template('tracker/createshipment.html')

@bp.route('/createincident', methods=('GET','POST'))
@login_required
def createincident():
    if request.method == 'POST':
        incidentnum = request.form['inum']
        calldate = request.form['calldate']
        storenum = request.form['storenum']
        storecontact = request.form['storecontact']
        notes = request.form['notes']
        db = get_db()
        error = None

        try:
            db.execute("INSERT INTO INCIDENT (INCIDENTNUM, CALLDATE, STORE_NUM, STORE_CONTACT, NOTES) VALUES (?,?,?,?,?)", 
                    (incidentnum, calldate, storenum, storecontact, notes))
            db.commit()
        except db.IntegrityError:
            error = f"Incident with number {incidentnum} already exists!"
        except db.Error as e:
            print(e)
            error = "An error occurred while inserting values into database"
        
        if error is not None:
            flash(error, "error")
        else:
            flash(f"Incident number {incidentnum} added to database.")

    return render_template('tracker/createincident.html')

@bp.route('/viewincidents')
@login_required
def viewincidents():
    incidents=get_incidents()
    return render_template('tracker/viewincidents.html', incidents=incidents)

def get_incidents(open=None,limit=None):
    db=get_db()
    return db.execute("SELECT * FROM INCIDENT").fetchall()
