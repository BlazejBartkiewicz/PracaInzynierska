import os
import tkinter as tk
from tkinter import ttk
import numpy as np
#from App.package.models import converter_short_month, check_if_negative, load_models, create_searched_row
from package.models import converter_short_month, check_if_negative, load_models, create_searched_row

os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

def run_app():
    root = tk.Tk()
    root.title("Building monitoring")
    root.geometry("700x600")
    label = tk.Label(root, text="Insert values:", font=("Arial", 16))
    label.grid(row=0, column=0, padx=10, pady=10, sticky="e")

    # Month
    month_label = tk.Label(root, text="Month:", font=("Arial", 14))
    month_label.grid(row=1, column=0, padx=10, pady=10)
    month_combobox = ttk.Combobox(root, values=["January",
                                                "February",
                                                "March",
                                                "April",
                                                "May",
                                                "June",
                                                "July",
                                                "August",
                                                "September",
                                                "October",
                                                "November",
                                                "December"], state="readonly")
    month_combobox.grid(row=1, column=1, padx=10, pady=10)
    month_combobox.current(0)

    # Week day
    week_day_label = tk.Label(root, text="Week day:", font=("Arial", 14))
    week_day_label.grid(row=2, column=0, padx=10, pady=10)
    week_day_combobox = ttk.Combobox(root, values=['Monday',
                                                   'Tuesday',
                                                   'Wednesday',
                                                   'Thursday',
                                                   'Friday',
                                                   'Saturday',
                                                   'Sunday'], state="readonly")
    week_day_combobox.current(0)
    week_day_combobox.grid(row=2, column=1, padx=0, pady=10)

    # Hour
    hour_label = tk.Label(root, text="Hour:", font=("Arial", 14))
    hour_label.grid(row=3, column=0, padx=10, pady=10)
    hour_combobox = ttk.Combobox(root, values=['0',
                                               '1',
                                               '2',
                                               '3',
                                               '4',
                                               '5',
                                               '6',
                                               '7',
                                               '8',
                                               '9',
                                               '10',
                                               '11',
                                               '12',
                                               '13',
                                               '14',
                                               '15',
                                               '16',
                                               '17',
                                               '18',
                                               '19',
                                               '20',
                                               '21',
                                               '22',
                                               '23', ], state="readonly")
    hour_combobox.current(0)
    hour_combobox.grid(row=3, column=1, padx=0, pady=10)

    # Dry bulb temp
    dry_bulb_label = tk.Label(root, text="Temp:", font=("Arial", 14))
    dry_bulb_label.grid(row=4, column=0, padx=10, pady=10)
    dry_bulb_entry = tk.Entry(root, width=10)
    dry_bulb_entry.grid(row=4, column=1, padx=0, pady=10)

    #Column names
    predicted_label = tk.Label(root, text="Predicted", font=("Arial", 14))
    predicted_label.grid(row=4, column=2, padx=10, pady=10)
    diff_label = tk.Label(root, text="Difference", font=("Arial", 14))
    diff_label.grid(row=4, column=3, padx=10, pady=10)

    # Heating load
    heating_load_label = tk.Label(root, text="Heating load (kW):", font=("Arial", 14))
    heating_load_label.grid(row=5, column=0, padx=10, pady=10)
    heating_load_entry = tk.Entry(root, width=10)
    heating_load_entry.grid(row=5, column=1, padx=10, pady=10)

    heating_load_predicted_label = tk.Label(root, text="", font=("Arial", 14))
    heating_load_predicted_label.grid(row=5, column=2, padx=10, pady=10)
    heating_load_diff_label = tk.Label(root, text="", font=("Arial", 14))
    heating_load_diff_label.grid(row=5, column=3, padx=10, pady=10)

    # Chiller Load
    chiller_output_label = tk.Label(root, text="Chiller output (kW):", font=("Arial", 14))
    chiller_output_label.grid(row=6, column=0, padx=10, pady=10)
    chiller_output_entry = tk.Entry(root, width=10)
    chiller_output_entry.grid(row=6, column=1, padx=10, pady=10)

    chiller_output_predicted_label = tk.Label(root, text="", font=("Arial", 14))
    chiller_output_predicted_label.grid(row=6, column=2, padx=10, pady=10)
    chiller_output_diff_label = tk.Label(root, text="", font=("Arial", 14))
    chiller_output_diff_label.grid(row=6, column=3, padx=10, pady=10)

    # Total building Electric
    total_building_label = tk.Label(root, text="Total building Electric (kW):", font=("Arial", 14))
    total_building_label.grid(row=7, column=0, padx=10, pady=10)
    total_building_entry = tk.Entry(root, width=10)
    total_building_entry.grid(row=7, column=1, padx=10, pady=10)

    total_building_predicted_label = tk.Label(root, text="", font=("Arial", 14))
    total_building_predicted_label.grid(row=7, column=2, padx=10, pady=10)
    total_building_diff_label = tk.Label(root, text="", font=("Arial", 14))
    total_building_diff_label.grid(row=7, column=3, padx=10, pady=10)

    cooling_model, heating_model, total_building_model = load_models()

    def get_data():
        month_combobox_data = month_combobox.get()
        week_day_data = week_day_combobox.get()
        hour_data = hour_combobox.get()
        dry_bulb_data = dry_bulb_entry.get()

        heating_load_data = float(heating_load_entry.get())
        chiller_output_data = float(chiller_output_entry.get())
        total_building_data = float(total_building_entry.get())

        converted_month = converter_short_month(month_combobox_data)

        searched_row, searched_row_scaled = create_searched_row(
            hour_data,
            dry_bulb_data,
            converted_month,
            week_day_data
        )

        cooling_prediction = float(check_if_negative(cooling_model.predict(searched_row)))
        heating_prediction = float(check_if_negative(heating_model.predict(searched_row_scaled)))
        total_building_prediction = float(check_if_negative(total_building_model.predict(searched_row)))

        heating_load_predicted_label.config(text=f"{np.round(heating_prediction, 1)}", font=("Arial", 14))
        heating_diff = heating_prediction - heating_load_data
        heating_load_diff_label.config(text=f"{np.round(abs(heating_diff), 1)}", font=("Arial", 14))

        chiller_output_predicted_label.config(text=f"{np.round(cooling_prediction, 1)}", font=("Arial", 14))
        cooling_diff = cooling_prediction - chiller_output_data
        chiller_output_diff_label.config(text=f"{np.round(abs(cooling_diff), 1)}", font=("Arial", 14))

        total_building_predicted_label.config(text=f"{np.round(total_building_prediction, 1)}", font=("Arial", 14))
        total_building_diff = total_building_prediction - total_building_data
        total_building_diff_label.config(text=f"{np.round(abs(total_building_diff), 1)}", font=("Arial", 14))

    button2 = tk.Button(root, text="Predict", command=get_data, font=("Arial", 14))
    button2.grid(row=19, column=1, padx=10, pady=10)

    close_button = tk.Button(root, text="Close", command=root.quit, font=("Arial", 14))
    close_button.grid(row=20, column=1, padx=10, pady=10)
    root.mainloop()
