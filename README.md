# TechConf Registration Website

## Project Overview
The TechConf website allows attendees to register for an upcoming conference. Administrators can also view the list of attendees and notify all attendees via a personalized email message.

The application is currently working but the following pain points have triggered the need for migration to Azure:
 - The web application is not scalable to handle user load at peak
 - When the admin sends out notifications, it's currently taking a long time because it's looping through all attendees, resulting in some HTTP timeout exceptions
 - The current architecture is not cost-effective 

In this project, you are tasked to do the following:
- Migrate and deploy the pre-existing web app to an Azure App Service
- Migrate a PostgreSQL database backup to an Azure Postgres database instance
- Refactor the notification logic to an Azure Function via a service bus queue message

## Dependencies

You will need to install the following locally:
- [Postgres](https://www.postgresql.org/download/)
- [Visual Studio Code](https://code.visualstudio.com/download)
- [Azure Function tools V3](https://docs.microsoft.com/en-us/azure/azure-functions/functions-run-local?tabs=windows%2Ccsharp%2Cbash#install-the-azure-functions-core-tools)
- [Azure CLI](https://docs.microsoft.com/en-us/cli/azure/install-azure-cli?view=azure-cli-latest)
- [Azure Tools for Visual Studio Code](https://marketplace.visualstudio.com/items?itemName=ms-vscode.vscode-node-azure-pack)

## Project Instructions

### Part 1: Create Azure Resources and Deploy Web App
1. Create a Resource group
2. Create an Azure Postgres Database single server
   - Add a new database `techconfdb`
   - Allow all IPs to connect to database server
   - Restore the database with the backup located in the data folder
3. Create a Service Bus resource with a `notificationqueue` that will be used to communicate between the web and the function
   - Open the web folder and update the following in the `config.py` file
      - `POSTGRES_URL`
      - `POSTGRES_USER`
      - `POSTGRES_PW`
      - `POSTGRES_DB`
      - `SERVICE_BUS_CONNECTION_STRING`
4. Create App Service plan
5. Create a storage account
6. Deploy the web app

### Part 2: Create and Publish Azure Function
1. Create an Azure Function in the `function` folder that is triggered by the service bus queue created in Part 1.

      **Note**: Skeleton code has been provided in the **README** file located in the `function` folder. You will need to copy/paste this code into the `__init.py__` file in the `function` folder.
      - The Azure Function should do the following:
         - Process the message which is the `notification_id`
         - Query the database using `psycopg2` library for the given notification to retrieve the subject and message
         - Query the database to retrieve a list of attendees (**email** and **first name**)
         - Loop through each attendee and send a personalized subject message
         - After the notification, update the notification status with the total number of attendees notified
2. Publish the Azure Function

### Part 3: Refactor `routes.py`
1. Refactor the post logic in `web/app/routes.py -> notification()` using servicebus `queue_client`:
   - The notification method on POST should save the notification object and queue the notification id for the function to pick it up
2. Re-deploy the web app to publish changes

## Monthly Cost Analysis
Complete a month cost analysis of each Azure resource to give an estimate total cost using the table below:

Azure App Service Basic - Estimated monthly cost $54.75
Azure Service Bus Basic - Estimated monthly cost $0.00
Azure Postgres Database	- Estimated monthly cost $138.47
Azure Storage Standard  - Estimated monthly cost $21.84
Azure Function Consumption - Estimated monthly cost $0.00

## Architecture Explanation
This is a placeholder section where you can provide an explanation and reasoning for your architecture selection for both the Azure Web App and Azure Function.

For the Function App, I choose the consumption plan type, also for Service Bus I choose Basic - they have estimated monthly cost $0.00. In the consumption plan you are charged for resources only when the function is up in running.For App Service I choose Basic because I consider that it includes everything we need to be able to test the application. Combining this two resources you can obtain good cost optimization. In Azure App Service scalability can be managed using a Web App. Azure Postgres was required for this project rubric. Standard plan is enough for storage.Because we don't have to maintain a VM this arhitecture is also profitable.
In existing architecture,the web application is not scalable to manage the task of top users. When the administrator sends notifications, it currently takes a long time because it loops through all participants, resulting in some HTTP expiration exceptions thus the current architecture is not profitable.
In current architecture,Azure Webapp and Azure Function can be easily scale up for certainly period of year and scale down when you don’t need too much resources. By using Service Bus Queue Trigger for sending emails to many recipients  this architecture becomes very cost effective comparing for example with a VM architecture. An advantage of using queues is that the senders and receivers  don't have to send and receive messages at the same time because messages are stored in the queue. Implementation of the backend API using Azure Function increase the speed for front-end app at high load and so the application response is much improved.
