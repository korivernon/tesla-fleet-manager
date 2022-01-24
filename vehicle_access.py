import teslapy
from tesla_email import *

from datetime import datetime


# tesla = teslapy.Tesla('4kand1m@gmail.com')
# if not tesla.authorized:
#     print('Use browser to login. Page Not Found will be shown at success.')
#     print('Open this URL: ' + tesla.authorization_url())
#     tesla.fetch_token(authorization_response=input('Enter URL after authentication: '))
# vehicles = tesla.vehicle_list()

def check_authorize(email):
    # redundant... authorization will need to be checked etiher way
    tesla = teslapy.Tesla(email)
    auth = not tesla.authorized
    return auth

def get_login_url(email):
    tesla = teslapy.Tesla(email)
    print("URL TO LOGIN:",tesla.authorization_url())
    return tesla.authorization_url()

def fetch_login_object(email, auth_token):
    tesla = teslapy.Tesla(email)
    return tesla.fetch_token(authorization_response=auth_token)


def vehicle_names(tesla, names=[]):
    vehicles = tesla.vehicle_list() #grab the vehicle object
    
    vehicle_name_list = []

    for vehicle in vehicles:
        ivd = {}
        try:
            data = vehicle.api('VEHICLE_DATA')['response']
        except:
            print("Error for" , vehicle["display_name"])
            continue
        data = dict(data)

        print(data.keys())

        #get vehicle name
        v_name = data["display_name"]
        
        # check against list of vehicle names
        if names == []:
            pass
        elif v_name not in names:
            continue
        ivd["name"] = v_name

        v_vin = data["vin"]
        ivd["vin"] = v_vin

        #car settings
        car = data["vehicle_config"]
        v_type = car["car_type"]
        ivd["model_type"] = v_type

        v_color = car["exterior_color"]
        ivd["color"] = v_color

        v_trim = car["trim_badging"]
        ivd["trim"] = v_trim

        v_wheel = car["wheel_type"]
        ivd["rim"] = v_wheel

        car_name = ivd["vin"][3] + ivd["trim"] + ivd["color"] + ivd["rim"]
        print(car_name)
        # add vehicle data
        vehicle_name_list.append(car_name)
    return vehicle_name_list

def email_data(tesla, names=[]):
    # ts = int('1284101485')

    # # if you encounter a "year is out of range" error the timestamp
    # # may be in milliseconds, try `ts /= 1000` in that case
    # print(datetime.utcfromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S'))
    
    vehicles = tesla.vehicle_list() #grab the vehicle object
    
    output_data = {}

    for vehicle in vehicles:
        ivd = {}
        try:
            data = vehicle.api('VEHICLE_DATA')['response']
        except:
            print("Error for" , vehicle["display_name"])
            continue
        data = dict(data)

        print(data.keys())

        #get vehicle name
        v_name = data["display_name"]
        
        # check against list of vehicle names
        if names == []:
            pass
        elif v_name not in names:
            continue
        ivd["name"] = v_name

        drive_state = data["drive_state"]["power"]
        ivd["drive_state"] = drive_state

        v_vin = data["vin"]
        ivd["vin"] = v_vin

        v_odo = data["vehicle_state"]["odometer"]
        ivd["odo"] = v_odo

        # get vehicle charge state
        v_charge = data["charge_state"]["battery_level"]
        ivd["charge"] = v_charge

        v_range = data["charge_state"]["battery_range"]
        ivd["range"] = v_range

        v_charge_limit = data["charge_state"]["charge_limit_soc"]
        ivd["limit"] = v_charge_limit

        est_battery_range = data["charge_state"]["est_battery_range"]
        ivd["real_range"] = est_battery_range

        time_unix = data["charge_state"]["timestamp"]
        ivd["unix_time"] = time_unix

        #get temp stats
        v_inside = data["climate_state"]["inside_temp"]
        ivd["temp_inside"] = v_inside

        #gui settings
        v_24hr = data["gui_settings"]["gui_24_hour_time"]
        ivd["time_settings"] = v_24hr

        v_charge_rate_units= data["gui_settings"]["gui_charge_rate_units"]
        ivd["charge_units"] = v_charge_rate_units

        v_temp_units = data["gui_settings"]["gui_temperature_units"]
        ivd["temp_units"] = v_temp_units

        #car settings
        car = data["vehicle_config"]
        v_type = car["car_type"]
        ivd["model_type"] = v_type

        v_color = car["exterior_color"]
        ivd["color"] = v_color

        v_trim = car["trim_badging"]
        ivd["trim"] = v_trim

        v_wheel = car["wheel_type"]
        ivd["rim"] = v_wheel

        # vehicle state
        state = data["vehicle_state"]
        v_locked = state["locked"]
        ivd["locked"] = v_locked

        # speed limit mode
        limit = data["vehicle_state"]["speed_limit_mode"]
        v_slm_act = limit["active"]
        ivd["speed_limit_mode_active"] = v_slm_act
        ivd["time"] = datetime.utcfromtimestamp(int(str(time_unix)[:-3:])).strftime('%Y-%m-%d %H:%M:%S')

        # add vehicle data
        output_data[v_name] = ivd
        print(v_name)
    return output_data

def send_email(tesla):
    send_email_with_data(str(email_data(tesla)))

def tesla_logout(email):
    tesla = teslapy.Tesla(email)
    tesla.close()
    return True