'''
Created on June 9, 2016

@author: David Moss and Destry Teeter

Email support@peoplepowerco.com if you have questions!
'''

# LESSON 5 - COMBINING TRIGGERS
# This lesson will demonstrate how to create an bot that is triggered from multiple types
# of triggers.
#
# RUNTIME.JSON
# Open up runtime.json.
#
# Our trigger is set to Decimal 15.
#
#     "trigger": 15,
#
# 15 = 1 + 2 + 4 + 8 = schedules + modes + alerts + measurements
# Therefore, this bot will trigger off of schedules, modes, alerts, and measurements from the data sources it specifies
# in the runtime.json file.
#
# We then see the details of each of these triggers down below.
#
# MEASUREMENTS
# Trigger off of Entry Sensors (when the doorStatus parameter is 'true'),
# Water Leak Sensors (when the waterStatus parameter is 'true'),
# and the Virtual Light Switch
#
#    "deviceTypes": [
#      {
#        "id": 10014,
#        "minOccurrence": 0,
#        "trigger": true,
#        "read": true,
#        "control": false,
#        "triggerParamName": "doorStatus",
#        "triggerParamValues": "true",
#        "reason": {
#          "en": "We're going to monitor your doors and windows."
#        }
#      },
#      {
#        "id": 10017,
#        "minOccurrence": 0,
#        "trigger": true,
#        "read": true,
#        "control": false,
#        "triggerParamName": "waterStatus",
#        "triggerParamValues": "true",
#        "reason": {
#          "en": "We're going to monitor your water leak detector."
#        }
#      },
#      {
#        "id": 10072,
#        "minOccurrence": 0,
#        "trigger": true,
#        "read": true,
#        "control": false,
#        "triggerParamName": "ppc.switchStatus",
#        "triggerParamValues": "0,1",
#        "reason": {
#          "en": "We're going to listen for measurements from your virtual light switch."
#        }
#      },
#
#
# ALERTS
# Trigger when a 'motion' alert is generated by an iOS Presence Camera
#
#      {
#        "id": 24,
#        "minOccurrence": 1,
#        "trigger": true,
#        "read": true,
#        "control": false,
#        "triggerAlertType": "motion",
#        "reason": {
#          "en": "Listening for motion recording events"
#        }
#      }
#
#
# MODES
# Trigger when the user sets their mode.
#
# SCHEDULES
# Run every 30 seconds, just to demonstrate it works.
# We recommend you don't run a real bot this fast as it will eat up execution time and increase the cost to run
# your service.
#
#    "schedule": "0/30 * * * * ?",
#
#


# RUNNING THIS BOT
# First, create a user account at http://app.presencepro.com.
#
# This bot will require a device to be connected to your account:
#    Option A:  Buy a Presence Security Pack (http://presencepro.com/store).
#               This is recommended because it will give you a lot more tools
#               to create cool botswith.
#
#    Option B:  Create a virtual light switch locally.
#               Open up another terminal window. In this lesson's directory, run
#
#               $ python lightSwitch.py
#
#               This will register a new 'Virtual Light Switch' into your account,
#               which you can control manually from its command line.
#               It uses the Device API, and from the point of view of the Ensemble
#               software suite server, is a real device.
#
#    You will need to have at least 1 entry sensor OR 1 virtual light switch in your
#    account before you can purchase this bot to run it (see below). Otherwise,
#    this bot will be incompatible with your account.
#
#
# There are several steps needed to run this bot:
#    1. Create a new directory for your bot, with your own unique bundle ID. Copy all the files into it.
#       Note that bundle ID's are always reverse-domain notation (i.e. com.yourname.YourBot) and cannot
#       be deleted or edited once created.
#    2. Create a new --bot on the server with botengine
#    3. Commit your bot to the server with botengine
#    4. Purchase your bot with botengine
#    5. Run your bot locally
#
#
# We've automated this for you with a script, 'runlesson.sh'. Run it from your terminal window:
#
#    $ ./runlesson.sh
#
#
# This script will automatically do the following for you.
# From a terminal window *above* this bot's current directory:
#
# 1. Create a new directory for your bot with your given bundle ID, and copy all the files from this
#    lesson into that new directory.
#
#
# 2. Commit your bot to the server.
#    This will push all the code, version information, marketing information, and icon to the server.
#    The bot will become privately available.
#
#    This will also purchase the bot for you.
#
#    botengine --commit com.yourname.YourBot
#
#
# 3. Run the bot locally.
#
#    botengine --run com.yourname.YourBot
#
#    This will automatically look up your bot instance ID and run the bot, using the real-time streaming data from the server
#    and the code that is on your local computer.
#

import datetime

def run(botengine):
    """
    Starting point of execution
    :param botengine: BotEngine environment - your link to the outside world
    """

    # Initialize
    inputs = botengine.get_inputs()                  # Information input into the bot
    trigger_type = botengine.get_trigger_type()       # What type of trigger caused the bot to execute this time
    triggers = botengine.get_triggers()              # Get a list of triggers for this execution
    measures = botengine.get_measures_block()        # Capture new measurements, if any
    access = botengine.get_access_block()            # Capture info about all things this bot has permission to access
    alerts = botengine.get_alerts_block()            # Capture new alerts, if any

    if trigger_type == botengine.TRIGGER_SCHEDULE:
        print("")
        botengine.get_logger().info("Executing on schedule")

        unix_time_ms = int(inputs['time'])
        unix_time_sec = unix_time_ms / 1000

        botengine.get_logger().info("\t=> Unix timestamp in milliseconds = " + str(unix_time_ms))
        botengine.get_logger().info("\t=> Human readable timestamp: " + datetime.datetime.fromtimestamp(unix_time_sec).strftime('%Y-%m-%d %H:%M:%S'))

    elif trigger_type == botengine.TRIGGER_MODE:
        # There's always only 1 trigger for mode changes, but it's delivered in a list of triggers.
        for trigger in triggers:
            print("")
            botengine.get_logger().info("Executing on a change of mode")
            mode = trigger['location']['event']
            botengine.get_logger().info("Your current mode is " + mode)

    elif trigger_type == botengine.TRIGGER_DEVICE_ALERT:
        # There can be multiple device triggers simultaneously (parent and child), loop through each of them
        for trigger in triggers:
            print("")
            botengine.get_logger().info("Executing on a device alert")
            for focused_alert in alerts:
                alert_type = focused_alert['alertType']
                device_name = trigger['device']['description']

                botengine.get_logger().info("\n\nGot a '" + alert_type + "' alert from your '" + device_name +"'!")

                for parameter in focused_alert['params']:
                    botengine.get_logger().info("\t" + parameter['name'] + " = " + parameter['value'])

    elif trigger_type == botengine.TRIGGER_DEVICE_MEASUREMENT:
        # There can be multiple device triggers simultaneously (parent and child), loop through each of them
        for trigger in triggers:
            print("")
            botengine.get_logger().info("Executing on a new device measurement")

            device_type = trigger['device']['deviceType']
            device_name = trigger['device']['description']

            if device_type == 10014:
                botengine.get_logger().info("\t=> It's an Entry Sensor")
                doorStatus = botengine.get_property(measures, "name", "doorStatus", "value")

                if doorStatus == "true":
                    botengine.get_logger().info("\t=> Your '" + device_name + "' opened")

                    # Timers only promise to execute the app again in the future, at approximately the time you want.
                    # Timers will not execute early, but you can expect them to execute late.
                    # Do not try to set a timer that is faster than 2 seconds.
                    # The usage is:  botengine.start_timer(seconds, function, argument).
                    botengine.start_timer(5, timer_fired, argument=device_name)

                else:
                    botengine.get_logger().info("\t=> Your '" + device_name + "' closed")


            elif device_type == 10017:
                botengine.get_logger().info("\t=> It's a Water Sensor")
                waterLeak = botengine.get_property(measures, "name", "waterLeak", "value")

                if waterLeak == "true":
                    botengine.get_logger().info("\t=> Your '" + device_name + "' got wet")

                else:
                    botengine.get_logger().info("\t=> Your '" + device_name + "' dried up")


            elif device_type == 10072:
                botengine.get_logger().info("\t=> It's a Virtual Light Switch")
                switchStatus = botengine.get_property(measures, "name", "ppc.switchStatus", "value")

                if int(switchStatus) > 0:
                    botengine.get_logger().info("Your '" + device_name + "' switched on")
                    botengine.start_timer(5, timer_fired, argument=device_name)

                else:
                    botengine.get_logger().info("Your '" + device_name + "' switched off")


def timer_fired(botengine, argument):
    """
    Entry point into the bot when your timer fires.
    You can give this function any name you want. But the function has to accept:  (botengine, argument) as its arguments.
    When the timer fires, only its function will execute, not your normal run(botengine) function will not trigger.
    The function cannot be a class method. It has to be a function inside your bot.py as it's an entry point into your bot.
    As you can see in this example, the argument we previously passed in when your door opened is the name of your door.

    :param botengine: Current execution environment
    :param argument: Argument we previously passed in when starting this timer
    """
    botengine.get_logger().info("Your timer fired because your '" + argument + "' opened recently!")
