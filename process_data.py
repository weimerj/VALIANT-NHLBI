import pandas as pd
import numpy as np
import scipy
import matplotlib.pyplot as plt


def plot_dataframe(dataframe, x_column, y_column, ystr, title):
    """
    Plots data from a Pandas DataFrame as an x-y plot.

    Parameters:
        dataframe (pd.DataFrame): The DataFrame containing the data.
        x_column (str): Name of the column to use as the x-axis.
        y_column (str): Name of the column to use as the y-axis.
    """
    try:
        # Check if the specified columns exist in the DataFrame
        if x_column not in dataframe.columns or y_column not in dataframe.columns:
            raise ValueError(f"Columns '{x_column}' or '{y_column}' do not exist in the provided DataFrame.")

        # Plot the data
        plt.figure(figsize=(10, 6))
        plt.plot(dataframe[x_column]/1000/60, dataframe[y_column], linestyle='-')
        plt.xlabel(x_column)
        plt.ylabel(y_column)
        plt.title(title)
        plt.xlabel('minutes')
        plt.ylabel(ystr)
        plt.grid(True)
        plt.show()

    except Exception as e:
        print(f"An error occurred: {e}")




# Read the CSV file into a Pandas DataFrame
file_path = "valiant-nhlbi.csv"  # Replace with the correct path to your CSV file
df = pd.read_csv(file_path)

df['ts'] = df['epoch'] - np.min(df['epoch'])
df_ppg = df[df['key'] == 'ntGGvKdfQc_LED_GREENval']
df_hr = df[df['key'] == 'ntGGvKdfQc_HRMhrm']
df_acc_x = df[df['key'] == 'ntGGvKdfQc_ACCx']
df_acc_y = df[df['key'] == 'ntGGvKdfQc_ACCy']
df_acc_z = df[df['key'] == 'ntGGvKdfQc_ACCz']
df_acc_xy = pd.merge(df_acc_x, df_acc_y, on='epoch', how='inner')
df_acc = pd.merge(df_acc_xy, df_acc_z, on='epoch', how='inner')
df_acc['mag'] = np.sqrt(np.pow(df_acc['val'], 2) + np.pow(df_acc['val_x'],2) + np.pow(df_acc['val_y'],2))


plot_dataframe(df_hr,'ts','val', 'beats per minute', 'Heart Rate')
plot_dataframe(df_ppg,'ts','val','', 'Photoplethsymgraphy')
plot_dataframe(df_acc,'ts','mag','meters per second squared', 'Motion Magnitude')