import paho.mqtt.client as mqtt

# data lists
subscribtions = []

# Send terminal option
def sendoption( question, options ):
    # for string build
    options_count = len(options)
    #question = "\u001b[33m|\u001b[0m " + question + " ["
    question = "| " + question + " ["
    # build string
    for x in range (options_count):
        question = question + " " + options[x] + " "

    question = question + "] "

    while(True):
        answer = input(question + "\n")
        # check answer
        if ( answer in options ):
            return answer

# Input Data (start at the beginning of the script)
def on_start():
    return input("| BrokerIP: ")

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("| Client connected to broker [" + brokerIP + "]")

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print(" » Incoming Message")
    print(" » Topic: " + msg.topic)
    print(" » Payload: " + str( msg.payload ).replace("'", "").replace("b", "") )
    print(" » End of Message \n")

# The callback for the PUBLISH send
def on_publish(client, userdata, result):
    if result:
        print("| Published: true\n")
    else:
        print("| Published: false\n")
    pass

brokerIP = on_start()

client = mqtt.Client("PythonMqttClient")
client.on_connect = on_connect
client.on_message = on_message
client.on_publish = on_publish
# connect client to broker
client.connect_async(brokerIP, 1883, 60)

client.loop_start()
# main menu
while(True):

    mainmenu = sendoption("Mqtt Client", ["traffic", "stop"])

    if mainmenu == "traffic":

        while(True):
            # start traffic menu
            option = sendoption("Traffic", ["unsubscribe", "subscribe", "publish", "list", "exit"])
            if option == "publish":
                # get some publish options
                topic = input("| Publish topic: ")
                payload = input("| Publish payload: ")
                # send publish
                client.publish(topic, payload)
            elif option == "subscribe":
                # get some subscribe options
                topic = input("| Subscribe topic: ")
                # send publish
                client.subscribe(topic)
                print("| Subscribed: true")
                # add to save
                subscribtions.append(topic)
            elif option == "unsubscribe":
                # get some subscribe options
                topic = input("| Subscribe topic: ")
                # send publish
                client.unsubscribe(topic)
                print("| Subscribed: false")
                # remove from list
                subscribtions.remove(topic)
            elif option == "list":
                # list length
                count = len(subscribtions)
                print("| Subscribed:")
                # printout
                for x in range(count):
                    print("  " + subscribtions[x])
                # end message
                print("\n")
            elif option == "exit":
                break;

    elif mainmenu == "stop":
        print("stopping client...")
        client.disconnect()
        print("stopping programm...")
        exit()