import os
import json
import time
import pandas as pd
import matplotlib.pyplot as plt
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
import schedule

def calculate_averages(df):
    avg_temperature = df['Temperature'].mean()
    avg_moisture = df['Moisture'].mean()
    avg_light = df['Light'].mean()
    avg_conductivity = df['Conductivity'].mean()

    return {'Temperature': avg_temperature, 'Moisture': avg_moisture,
            'Light': avg_light, 'Conductivity': avg_conductivity}

def create_bar_graph(averages, output_file):
    labels = list(averages.keys())
    values = list(averages.values())

    fig, ax = plt.subplots()
    ax.bar(labels, values)
    ax.set_ylabel('Values')
    ax.set_title('Sensor Data Averages')

    fig.savefig(output_file)
    plt.close(fig)

def send_email(graph_image_path, to_email, from_email, password):
    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = 'Sensor Data Averages'

    body = "Here is the bar graph of the sensor data averages:"
    msg.attach(MIMEText(body, 'plain'))

    with open(graph_image_path, 'rb') as f:
        img = MIMEImage(f.read())
        msg.attach(img)

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(from_email, password)
        text = msg.as_string()
        server.sendmail(from_email, to_email, text)
        server.quit()
        print("Email sent successfully.")
    except Exception as e:
        print("Error while sending email: ", e)

def send_averages_email():
    # Read the saved data
    with open('sesh.json', 'r') as f:
        data = json.load(f)
    df = pd.DataFrame(data)

    # Calculate averages and create a bar graph
    averages = calculate_averages(df)
    output_file = 'averages_bar_graph.png'
    create_bar_graph(averages, output_file)

    # Send the email with the bar graph attached
    to_email = 'jsbarton96@hotmail.com'
    from_email = 'jsbarton96@hotmail.com'
    password = ''
    send_email(output_file, to_email, from_email, password)

# Schedule the email to be sent every 4 hours
schedule.every(4).hours.do(send_averages_email)

# Keep the script running and send the email according to the schedule
while True:
    schedule.run_pending()
    time.sleep(60)
