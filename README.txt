# WeatherNotif
Follow the steps below to start the project and interact with the bot
To start the project:
-Run the "docker compose up" command to start the project, you can then interact with the Telegram bot
Starting the bot:
-Open Telegram and search for the bot "WeatherNotif"
-Start the bot by selecting the icon and pressing "Start."
Commands:
Once the bot is started, you can use the following commands:
    /help - Show this help message.
    /sub - Use this command specifying the city and your alerts
    /alert - List of possible alerts
    /show_sub -Shows the list of subscriptions made 
To create a subscription, use the /sub command followed by the desired city,rain condition, and maximum and minimum temperatures.
For example: " /sub Catania Rain Tempmax:30 Tempmin:20 "
Rain - alert the user when it's gonna rain
Tempmax:value - alert the user when the temp reaches or surpass the specified value.
Tempmin:value - same logic as before considering a minimum temperature.

PSA: alerts are not case sensitive"
Receiving Notifications
After creating a subscription, wait approximately 3 minutes to receive the notification message related to your request

