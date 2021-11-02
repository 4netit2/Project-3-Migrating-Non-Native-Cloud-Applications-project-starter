import logging
import azure.functions as func
import psycopg2
import os
from datetime import datetime
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

def main(msg: func.ServiceBusMessage):

    notification_id = int(msg.get_body().decode('utf-8'))
    logging.info('Python ServiceBus queue trigger processed message: %s',notification_id)

    # TODO: Get connection to database
    connection = psycopg2.connect(user="tech@techconfdb-server",
                                  password="pass321!",
                                  host="techconfdb-server.postgres.database.azure.com",
                                  port="5432",
                                  database="techconfdb")
    cursor = connection.cursor()

    try:
        # TODO: Get notification message and subject from database using the notification_id

        cursor.execute("SELECT subject, message FROM notification WHERE id={};".format(notification_id))
        rows=cursor.fetchall()
        rows=rows[0]
        subject = str(rows[0])
        body = str(rows[1])

        # TODO: Get attendees email and name

        cursor.execute("SELECT first_name, last_name, email FROM attendee;")
        attendees = cursor.fetchall()

        # TODO: Loop through each attendee and send an email with a personalized subject

        for attendee in attendees:
           for (email, first_name) in attendees:
            mail = Mail(
                from_email='info@techconf.com',
                to_emails= email,
                subject= subject,
                plain_text_content= "Hi {}, \n {}".format(first_name, body))
            try:
                SENDGRID_API_KEY = os.environ['SENDGRID_API_KEY']
                sg = SendGridAPIClient(SENDGRID_API_KEY)
                response = sg.send(mail)
            except Exception as e:
                logging.error(e)
        status = "Notified {} attendees".format(len(attendees))

        # TODO: Update the notification table by setting the completed date and updating the status with the total number of attendees notified

        notification_completed_date = datetime.utcnow()
        notification_status = 'Notified {} attendees'.format(len(attendees))
        update_query = cursor.execute("UPDATE notification SET status = '{}', completed_date = '{}' WHERE id = {};".format(notification_status, notification_completed_date, notification_id))
        connection.commit()

    except (Exception, psycopg2.DatabaseError) as error:
        logging.error(error)
    finally:
        # TODO: Close connection

        cursor.close()
        connection.close()
```
