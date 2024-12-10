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
        incidentnum = request.form['incnum']
        shiptype = request.form['shiptype'] #sending or receiving
        gunser = request.form['gun']
        baseser = request.form['base']
        cable = request.form['cable']
        date = request.form['date']
        tracking = request.form['tracking']
        notes = request.form['notes']

        db = get_db()
        error = None

        if shiptype == "sending":
            shiptype = 0
        elif shiptype == "receiving":
            shiptype = 1
        else:
            error = "Invalid shipment type"
            

        if error is None:
            try:
                db.execute("INSERT INTO SHIPMENT (GUNSER, BASESER, CABLE, DATE, TRACKING, NOTES, DIRECTION, INCIDENTNUM) VALUES (?,?,?,?,?,?,?,?)", 
                        ( gunser, baseser, cable, date, tracking, notes, shiptype, incidentnum ))
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
   
    return render_template('tracker/createshipment.html', incnum=request.args.get('incnum'), shiptype=request.args.get('shiptype'))

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

@bp.route('/details')
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
    
    # print(inc_res)    -|
    # print(send_res)   -|- <sqlite3.Row object>
    # print(recv_res)   -|

    return render_template("tracker/incidentdetails.html", incident=inc_res, send_list=send_res, recv_list=recv_res)

@bp.route('/edit', methods=('GET', 'POST'))
@login_required
def edit():
    edittype = request.args.get("type")

    if edittype == "incident":
        incnum = request.args.get("_incnum")
        db = get_db()

        if request.method == 'POST':
            data = (
                request.form['calldate'],
                request.form['storenum'],
                request.form['storecontact'],
                request.form['notes'],
                request.form['incnum'],
            )
            
            db.execute('''UPDATE INCIDENT 
                          SET CALLDATE = ?,
                              STORENUM = ?,
                              STORECONTACT = ?,
                              NOTES = ?
                          WHERE INCIDENTNUM = ?''', data)
            db.commit()

        res = db.execute('''SELECT * FROM INCIDENT
                        WHERE INCIDENTNUM = ?''', (incnum,)).fetchone()
        

        return render_template("tracker/edit.html", type=edittype,data=res)

    if edittype == "shipment":
        id = request.args.get("id")
        db = get_db()

        if request.method == 'POST':
            
            data = (
                request.form['gun'],
                request.form['base'],
                request.form['cable'],
                request.form['date'],
                request.form['tracking'],
                request.form['notes'],
                id)
            
            db.execute('''UPDATE SHIPMENT 
                       SET GUNSER = ?,
                           BASESER = ?,
                           CABLE = ?,
                           DATE = ?,
                           TRACKING = ?,
                           NOTES = ?
                       WHERE ID = ?''', data)
            db.commit()

        res = db.execute('''SELECT * FROM SHIPMENT
                        WHERE ID = ?''', (id,)).fetchone()

        return render_template("tracker/edit.html", type=edittype, data=res)
    
    else:
    #edittype undefined
        return redirect(url_for('tracker.viewincidents'))
    
@bp.route('/deleteshipment/<id>', methods=["DELETE"])
@login_required
def delete_shipment(id):
    db = get_db()
    db.execute('''DELETE FROM SHIPMENT
               WHERE ID = ?''',(id,))
    db.commit()
    return "Shipment Deleted From Database"

@bp.route('/deleteincident/<incnum>', methods=["DELETE"])
@login_required
def delete_incident(incnum):
    db = get_db()
    db.execute('''DELETE FROM INCIDENT
               WHERE INCIDENTNUM = ?''',(incnum,))
    db.commit()
    return "Incident Deleted From Database"

@bp.route('/complete/<id>', methods=["POST"])
@login_required
def complete_shipment(id):
    from datetime import datetime
    current_date=datetime.now().strftime("%m/%d/%Y")
    db = get_db()
    db.execute('''UPDATE SHIPMENT
                  SET COMPLETED = ?
                  WHERE ID = ?''', (current_date ,id,))
    db.commit()
    return "<p class='text-green-700'>Marked complete just now.</p>"

def get_all_incidents(open=None,limit=None):
    db=get_db()
    return db.execute("SELECT * FROM INCIDENT").fetchall()

def convert_date(datestr, toForm=False):
    values = datestr.split('-')
    if toForm:
        rtnstr = "-".join([values[2],values[0],values[1]])
    else:
        rtnstr = "-".join([values[1],values[2],values[0]])
    return rtnstr


