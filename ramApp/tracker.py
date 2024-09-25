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
    return render_template("tracker/components/incidentcards.html", incidents=res)

@bp.route('/edit', methods=('GET', 'POST'))
@login_required
def edit():
    _incnum = request.args.get("_incnum")
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

    return render_template("tracker/editincident.html", incnum=_incnum)


def get_all_incidents(open=None,limit=None):
    db=get_db()
    return db.execute("SELECT * FROM INCIDENT").fetchall()
