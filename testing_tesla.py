import teslapy

tesla = teslapy.Tesla('4kand1m@gmail.com')
if not tesla.authorized:
    print('Use browser to login. Page Not Found will be shown at success.')
    print('Open this URL: ' + tesla.authorization_url())
    tesla.fetch_token(authorization_response=input('Enter URL after authentication: '))
vehicles = tesla.vehicle_list()

information = ""
for vehicle in vehicles:
    information += str(vehicle.get_vehicle_data())
    data = vehicle.api('VEHICLE_DATA')['response']
    data = dict(data)
    # print(type(dict(data)))
    # print(data)
    # print(str(vehicle.api('VEHICLE_DATA')['response']))
    # information+=str(vehicle.api('VEHICLE_DATA')['response'])
    information+= str(data)
    information+=  "\n==============================SEPARATION================================="

# print(information)
tesla.close()
