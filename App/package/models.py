import keras
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler


def converter_short_month(month):
    short_month = ''
    if month == 'April':
        short_month = 'Apr'
    elif month == 'August':
        short_month = 'Aug'
    elif month == 'December':
        short_month = 'Dec'
    elif month == 'February':
        short_month = 'Feb'
    elif month == 'January':
        short_month = 'Jan'
    elif month == 'July':
        short_month = 'Jul'
    elif month == 'June':
        short_month = 'Jun'
    elif month == 'March':
        short_month = 'Mar'
    elif month == 'May':
        short_month = 'May'
    elif month == 'November':
        short_month = 'Nov'
    elif month == 'October':
        short_month = 'Oct'
    elif month == 'September':
        short_month = 'Sep'
    return short_month


def create_searched_row(hour, dry_bulb, month, week_day):
    data_frame = pd.read_csv('../Data/Raw_data_2023.csv', encoding='unicode_escape', sep=",")
    base_data_frame = data_frame.drop(['Month',
                                       'Week day',
                                       'Day',
                                       'Chiller Output (kW)',
                                       'Chiller Input (kW)',
                                       'Heating Load (kW)',
                                       'Total Building Electric [kW]',
                                       'Precool Coil Load (kW)',
                                       'Preheat Coil Load (kW)',
                                       'Terminal Cooling Coil Load (kW)',
                                       'Terminal Heating Coil Load (kW)',
                                       'Ventilation Fan (kW)',
                                       'Exhaust Fan (kW)',
                                       'Terminal Fan (kW)',
                                       'Vent. Reclaim Device (kW)',
                                       'Lighting (kW)',
                                       'Electric Equipment (kW)'

                                       ], axis=1)
    # Dodawanie hour i dry_bulb
    base_data_frame.loc[len(base_data_frame)] = [int(hour), float(dry_bulb)]

    # Dodawanie month
    month_data_frame = data_frame['Month'].values
    month_data_frame = np.append(month_data_frame, month)
    month_encoded = pd.get_dummies(month_data_frame, columns=['Month'])

    # Dodawanie weekday
    week_day_data_frame = data_frame['Week day'].values
    week_day_data_frame = np.append(week_day_data_frame, week_day)
    week_day_encoded = pd.get_dummies(week_day_data_frame, columns=['Week day'])

    concat_data_frame = np.concatenate((base_data_frame, month_encoded, week_day_encoded), axis=1)

    scaler = StandardScaler()
    concat_scaled_data_frame = scaler.fit_transform(concat_data_frame)

    searched_row = concat_data_frame[-1]

    reshaped_searched_row = searched_row.reshape(1, 21)
    searched_row_scaled = concat_scaled_data_frame[-1]
    reshaped_searched_row_scaled = searched_row_scaled.reshape(1, 21)
    return reshaped_searched_row, reshaped_searched_row_scaled


def predict(model, searched_row):
    return model.predict(searched_row)


def check_if_negative(result):
    result_con = float(result[0][0])
    if result_con < 0:
        return 0
    else:
        return result[0][0]


def load_models():
    cooling_model = keras.models.load_model('../Models/Cooling_nonscaled_model.keras')
    heating_model = keras.models.load_model("../Models/Heating_scaled_model.keras")
    total_building_model = keras.models.load_model("../Models/Total_building_nonscaled_model.keras")
    return cooling_model, heating_model, total_building_model


def percent_error(expected, predicted):
    error = abs(expected - predicted) / abs(expected) * 100
    return error
