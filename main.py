import requests
import json
import pandas as pd

# Domain API *fill in your own client_id, client_secret, email_address
client_id = 'your_client_id'
client_secret = 'your_client_secret'
auth_url = 'https://auth.domain.com.au/v1/connect/token'
locater_endpoint = 'https://api.domain.com.au/v1/addressLocators/'
property_endpoint = 'https://api.domain.com.au/v1/properties/'
scope = 'api_properties_read','api_addresslocators_read',

# User info and requirement *fill in your own user info
searchlevel = 'Suburb'
email_address = 'your_email_address'
area = 'gold coast area'
suburb = 'Surfers Paradise'
postcode = '4217'
state = 'QLD'
street_name = 'Harris'
street_type = 'Street'
street_number = '1'
unit_number = '1'

#Get access token
def get_access_token():
    payload = {
        'client_id': client_id,
        'client_secret': client_secret,
        'grant_type': 'client_credentials',
        'scope': scope,
        'content-type': 'text/json'
    }
    response = requests.post(auth_url, data=payload)
    access_token = response.json()['access_token']
    return access_token

# Get properties id by search
def get_properties_id_by_search(access_token):
    property_id = []
    headers = {
        'Authorization': 'Bearer ' + access_token,
    }
    url = property_endpoint + '_suggest?terms=' + street_number + '+' + street_name + '+' + street_type + '%2C+' + suburb + '+' + state + '+' + postcode + '&channel=Residential'
    response = requests.post(url, headers=headers)
    if response.ok:
        data = response.json():
        property_id.append(data['id'])
    else:
        print("Error: " + response.text)
    return property_id

# Get properties info
def get_properties_info(access_token,property_id):
    properties = pd.DataFrame({'address':[],'suburb':[],'price':[],'bedrooms':[],'bathrooms':[],'car_spaces':[],'property_type':[]})
    for id in property_id:
        headers = {
            'Authorization': 'Bearer ' + access_token,
        }
        url = property_endpoint + id
        response = requests.get(url, headers=headers)
        if response.ok:
            data = response.json()
            for item in data:
                if item['status'] == 'onMarket':
                    address = item['address']
                    suburb = item['suburb']
                    price = data['priceDetails']['displayPrice']
                    bedrooms = data['generalFeatures']['bedrooms']
                    bathrooms = data['generalFeatures']['bathrooms']
                    car_spaces = data['generalFeatures']['carSpaces']
                    property_type = data['propertyDetails']['propertyType']
                    properties = properties.append({'address':address,'suburb':suburb,'price':price,'bedrooms':bedrooms,'bathrooms':bathrooms,'car_spaces':car_spaces,'property_type':property_type},ignore_index=True)
                else:
                    return None
        else:
            print("Error: " + response.text)
    return properties

# convert to csv
def convert_to_csv(properties):
    properties.to_csv('properties.csv',index=False)