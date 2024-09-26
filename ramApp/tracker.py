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
        incidentnum = request.form['inum']
        shiptype = request.form['shiptype'] #sending or receiving
        gunser = request.form['gunser']
        baseser = request.form['baseser']
        cable = request.form['cable']
        shipdate = request.form['shipdate']
        notes = request.form['notes']

        

        db = get_db()
        error = None

        if shiptype == "sending":
            shiptype = 0
        elif shiptype == "receiving":
            shiptype = 1

        #Create shipment logic
        try:
            db.execute("INSERT INTO SHIPMENT (INCIDENTNUM, DIRECTION, GUNSER, BASESER, CABLE, SHIPDATE, NOTES) VALUES (?,?,?,?,?,?,?)", 
                    (incidentnum, shiptype, gunser, baseser, cable, shipdate, notes))
            db.commit()
        except db.IntegrityError:
            error = f"Incident number {incidentnum} doesn't exist!"
        except db.Error as e:
            print(e)
            error = "An error occurred while inserting values into database"
        
        if error is not None:
            flash(error, "error")
        else:
            flash(f"Shipment added to database.")

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
            db.execute("INSERT INTO INCIDENT (INCIDENTNUM, CALLDATE, STORENUM, STORECONTACT, NOTES) VALUES (?,?,?,?,?)", 
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
    incidents=get_all_incidents()
    return render_template('tracker/viewincidents.html', incidents=incidents)

@bp.route('/search', methods=('POST',))
@login_required
def search():
    db=get_db()
    search = request.form["searchinput"].lower()
    res = db.execute('''SELECT *, 
                     instr(lower(INCIDENTNUM), ?) AS A, 
                     instr(lower(CALLDATE), ?) AS B,
                     instr(lower(STORENUM), ?) AS C,
                     instr(lower(STORECONTACT), ?) AS D
                     FROM INCIDENT
                     WHERE A>0 OR B>0 OR C>0 OR D>0
                     ''', (search, search, search, search)).fetchall()
    return render_template("tracker/components/incidentcard.html", incidents=res)

@bp.route('/details', methods=('GET', 'POST'))
@login_required
def details():
    _incnum = request.args.get("_incnum")

    #Check for if a user manually goes to /edit endpoint without an argument
    if _incnum == None:
        return redirect(url_for('tracker.viewincidents'))
    
    db=get_db()

    #We start with just the incident number

    #From this we must gather:
    #   - the rest of the incident info
    #   - related sending and recieving info
    #   - related itemtransactions 

    #Then we want to pass each of the responses as a dictionary
    #to render_template

    inc_res = db.execute('''SELECT * FROM INCIDENT
                         WHERE INCIDENTNUM = ?''', (_incnum, )).fetchone()
    
    send_res = db.execute('''SELECT * FROM SHIPMENT
                          WHERE INCIDENTNUM = ? AND DIRECTION = 0''', (_incnum, )).fetchall()
    
    recv_res = db.execute('''SELECT * FROM SHIPMENT
                          WHERE INCIDENTNUM = ? AND DIRECTION = 1''', (_incnum, )).fetchall()

    return render_template("tracker/incidentdetails.html", incident=inc_res, send_list=send_res, recv_list=recv_res)


def get_all_incidents(open=None,limit=None):
    db=get_db()
    return db.execute("SELECT * FROM INCIDENT").fetchall()

