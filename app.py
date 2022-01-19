from flask import *
from vehicle_access import *
import teslapy
from tesla_email import *
import time

app = Flask(__name__)

@app.route('/', methods=["POST", "GET"])
@app.route('/index', methods=["POST", "GET"])
def index():
    '''
    Homepage
    '''
    messages = []
    print("index() route being called:")
    if request.method == "POST":
        print("POST REQUEST RECEIVED")
        email = request.form.get("email") 
        token = request.form.get("token")
        
        tesla = teslapy.Tesla(email)

        fetch = fetch_login_object(email, token)
        if email and token:
            tesla = fetch
            print("Branch 1")
            print(tesla.vehicle_list())
        elif email and not fetch:
            print("Branch 2")
            return redirect(url_for('dashboard', email=email))
            print(tesla.vehicle_list())
            
        else:
            print("Branch 3")
            msg = get_login_url(email)
            if msg == "None":
                messages.append("Account Already validated.")
            else:
                messages.append(msg)
    return render_template('index.html',messages = messages)

@app.route('/dashboard/<email>/', methods=["POST", "GET"])
def dashboard(email):
    messages = []
    tesla = teslapy.Tesla(email)
    vehicles = email_data(tesla)
    out_str = []
    if request.method == "POST":
        print("\trequest data", request.form)
        if len(dict(request.form)) == 1:
            target = list(dict(request.form).keys())[0]
            action = list(dict(request.form).values())[0]
            target = target[target.find("_")+1::]
            target = [target]
        else:
            target = list(dict(request.form).keys())
            email_vehicle_list = []
            for vehicle in target:
                name = vehicle[vehicle.find("_")+1::]
                if name != "sendemail":
                    email_vehicle_list.append(name)
                else:
                    action = name
            target = email_vehicle_list
            print("\tThis is the email list of the vehicles:",target)
        print("\tthe target is:", target)
        for vehicle in tesla.vehicle_list():
            if vehicle["display_name"] in target:
                if action == "lock":
                    print("locking", vehicle["display_name"])
                    vehicle.command("LOCK")
                    time.sleep(5)
                    render_template('dashboard.html', data=out_str, messages=messages, email=email)
                elif action == "unlock":
                    print("unlocking:",vehicle["display_name"])
                    vehicle.command("UNLOCK")
                elif action == "remotestart":
                    print("remotely starting:",vehicle["display_name"])
                    vehicle.command("REMOTE_START")
                elif action == "sendemail":
                    print("\tWe can now send an email to:", vehicle["display_name"])
                    email_information = email_data(tesla, names=target)
                    send_email_with_data(email_information)
            else:
                continue
    for name,stats in vehicles.items():
        out_str.append( (str(name), stats) )
    return render_template('dashboard.html', data=out_str, messages=messages, email=email)

@app.route('/logout/<email>/')
def logout(email):
    tesla_logout(email)
    return render_template(url_for('index'))
    

def main():
    app.run(debug=True)
main()