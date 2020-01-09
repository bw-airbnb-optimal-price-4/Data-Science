import pandas as pd
import numpy as np
import shap
import onnxruntime as rt
from flask import request, jsonify
from app.models.listing import Listing


def predict():
    # check for id
    if 'id' not in request.args:
        # TODO validate
        return "Error: no id field provided"

    # load mappers
    property_type_mapper = {'Aparthotel':             34,
                            'Apartment':              17,
                            'Barn':                   5,
                            'Bed and breakfast':      16,
                            'Boat':                   2,
                            'Boutique hotel':         31,
                            'Bungalow':               23,
                            'Bus':                    1,
                            'Cabin':                  15,
                            'Camper/RV':              7,
                            'Campsite':               0,
                            'Casa particular (Cuba)': 29,
                            'Chalet':                 30,
                            'Condominium':            19,
                            'Cottage':                22,
                            'Dome house':             25,
                            'Farm stay':              10,
                            'Guest suite':            9,
                            'Guesthouse':             12,
                            'Hostel':                 3,
                            'Hotel':                  28,
                            'House':                  18,
                            'Hut':                    13,
                            'Loft':                   27,
                            'Nature lodge':           26,
                            'Other':                  14,
                            'Resort':                 33,
                            'Serviced apartment':     24,
                            'Tent':                   4,
                            'Tiny house':             8,
                            'Tipi':                   20,
                            'Townhouse':              21,
                            'Treehouse':              11,
                            'Villa':                  32,
                            'Yurt':                   6}
    room_type_mapper = {'Entire Home/Apt': 2, 'Hotel Room': 3,
                        'Private Room':    1, 'Shared Room': 0}
    neighborhood_mapper = {'Allendale':                  35,
                           'Anderson Mill':              6,
                           'Angus Valley':               12,
                           'Balcones Civic Association': 25,
                           'Balcony Woods':              17,
                           'Barton Creek':               54,
                           'Barton Hills':               73,
                           'Bouldin Creek':              67,
                           'Brentwood':                  24,
                           'Bryker Woods':               69,
                           'Bull Creek':                 28,
                           'Canyon Mesa':                74,
                           'Cat Mountian':               27,
                           'Cherry Creek':               18,
                           'Circle C':                   31,
                           'Clarksville':                53,
                           'Copperfield':                7,
                           'Crestview':                  56,
                           'Dawson':                     52,
                           'Downtown':                   75,
                           'East Congress':              39,
                           'East Downtown':              57,
                           'East Riverside':             44,
                           'Galindo':                    58,
                           'Gateway':                    66,
                           'Georgian Acres':             0,
                           'Govalle':                    47,
                           'Gracywoods':                 15,
                           'Hancock':                    41,
                           'Highland':                   32,
                           'Holly':                      59,
                           'Hyde Park':                  36,
                           'Lamplight Village':          3,
                           'Long Canyon':                42,
                           'MLK & 183':                  21,
                           'McKinney':                   10,
                           'Mesa Park':                  8,
                           'Milwood':                    9,
                           'Montopolis':                 19,
                           'Mueller':                    45,
                           'North Loop':                 13,
                           'North Shoal Creek':          14,
                           'Northwest Hills':            22,
                           'Oak Hill':                   23,
                           'Old Enfield':                68,
                           'Old West Austin':            65,
                           'Parker Lane':                26,
                           'Pecan Spings':               16,
                           'Pleasant Valley':            20,
                           'Rainey Street':              77,
                           'Rollingwood':                63,
                           'Rosedale':                   60,
                           'Rosewood':                   49,
                           'SW Williamson Co.':          5,
                           'Scofield Ridge':             4,
                           'South Congress':             62,
                           'South First':                64,
                           'South Lamar':                55,
                           'South Manchaca':             46,
                           'St. Edwards':                48,
                           'St. Johns':                  1,
                           'Steiner Ranch':              40,
                           'Sunset Valley':              51,
                           'Tarrytown':                  71,
                           'Travis Heights':             61,
                           'University Hills':           37,
                           'University of Texas':        38,
                           'Upper Boggy Creek':          50,
                           'Walnut Creek':               33,
                           'West Austin':                76,
                           'West Campus':                29,
                           'West Congress':              34,
                           'Westgate':                   43,
                           'Westlake Hills':             72,
                           'Windsor Hills':              2,
                           'Windsor Park':               30,
                           'Wooten':                     11,
                           'Zilker':                     70}

    mappers = [property_type_mapper, room_type_mapper, neighborhood_mapper]

    # load the coefficients and intercepts for the model
    coefs = np.array(
        [-0.32036224007606506, -2.128312587738037, 2.175335645675659,
         33.625144958496094, 1.2222827672958374, 8.58727741241455,
         23.42928695678711, 25.776762008666992, -1.0877704620361328])
    intercepts = np.array([-55.68082046508789])

    # numeric and categorical features
    numeric_features = ['month', 'year', 'accommodates', 'bedrooms',
                        'bathrooms', 'beds']
    categorical_features = ['property_type', 'room_type', 'neighborhood']

    # save month and year
    month = 12
    year = 19

    # get listing
    listing = Listing.query.get(int(request.args['id']))
    if listing is None:
        # TODO validate
        return "Listing Not Found"

    # get info about listing
    listing = pd.DataFrame({
        "month":         month,
        "year":          year,
        "property_type": listing.property_type.property_type,
        "room_type":     listing.room_type,
        "neighborhood":  listing.neighborhood.neighborhood,
        "accommodates":  listing.accommodates,
        "bedrooms":      listing.bedrooms,
        "bathrooms":     listing.bathrooms,
        "beds":          listing.bedrooms
    }, index=[0])

    listing_trans = listing.copy()

    # map features
    for idx, cat_feature in enumerate(categorical_features):
        listing_trans[cat_feature] = listing_trans[cat_feature].map(mappers[idx])

    listing_trans = listing_trans.astype(float)

    # load the training data
    X_train_trans = pd.read_csv('app/data/X_train_trans.csv')

    # predict listing price
    sess = rt.InferenceSession("app/airbnb-models/airbnb.onnx")
    input_name = sess.get_inputs()[0].name
    label_name = sess.get_outputs()[0].name
    pred_onx = sess.run([label_name], {input_name: listing_trans.values.astype(
        np.float32)})[0]
    pred = pred_onx[0][0]

    # get shapley values
    explainer = shap.LinearExplainer((coefs, intercepts), X_train_trans)
    shap_values = explainer.shap_values(listing_trans)

    feature_names = listing.columns
    feature_values = listing.values[0]
    shaps = pd.Series(shap_values[0], zip(feature_names, feature_values))

    pros = shaps.sort_values(ascending=False)[:2].index
    cons = shaps.sort_values(ascending=True)[:2].index

    output_str = jsonify(prediction=float(pred),
                         pros1=pros[0],
                         pros2=pros[1],
                         cons1=cons[0],
                         cons2=cons[1])

    return output_str
