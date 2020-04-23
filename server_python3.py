from socket import *
import _thread
import urllib.parse
import json
import datetime
import requests

serverPort = 8080

serverSocket = socket(AF_INET, SOCK_STREAM)

serverSocket.bind(("", serverPort))

serverSocket.listen(5)
print('The server is running')


def download_pictures(name, ip, file_name):
    name = name.split()
    save_file = name[0] + "_" + name[1] + "_" + file_name
    pic = requests.get(ip + file_name)
    with open(save_file, "wb") as file:
        file.write(pic.content)
    return save_file


def add_status(status):
    j_obj = get_json("status.json")
    t_stamp = datetime.datetime.now()
    new_update = {"timestamp": t_stamp.strftime("%d-%b-%Y %H:%M:%S.%f"), "status": status, "likes": []}
    j_obj["updates"].append(new_update)
    save_json("status.json", j_obj)


def parse_filename_request(filename):
    if "?" in filename:
        filename = filename.split("?")
        if "&" in filename[1]:
            command_list = filename[1].split("&")
        else:
            command_list = [filename[1]]
    elif "&" in filename:
        command_list = filename.split("&")
    else:
        command_list = [filename]

    command_dictionary = {}

    for item in command_list:
        elements = item.split("=")
        command_dictionary[elements[0]] = elements[1]
    return command_dictionary


def get_json(filename):
    with open(filename, "r") as file:
        j_obj = json.load(file)
    return j_obj


def save_json(filename, json_obj):
    with open(filename, "w") as file:
        file.write(json.dumps(json_obj, indent=2))


def create_feed_json():
    # open local lists of friends
    dic_friends = get_json("friends.json")
    # create a dictionary
    feed_update = {"friends_updates": []}
    # iterate through the list of friends downloading portraits and adding their latest update
    for friend in dic_friends["friends"]:
        r = requests.get(friend["ip_address"] + "status.json")
        file_name = download_pictures(friend["name"], friend["ip_address"], "portrait.png")
        # print("request return", r.content)
        status = r.json()
        recent_status = status["updates"][-1]
        name = friend["name"]
        likes = len(recent_status["likes"])
        date, feed_id = recent_status["timestamp"].split()
        feed_update["friends_updates"].append({"picture": file_name, "name": name,
                                               "timestamp": date,
                                               "status": recent_status["status"],
                                               "likes": likes, "feed_id": feed_id})
    return feed_update


def check_fof(ip):
    friends_list = get_json("friends.json")

    for friend in friends_list["friends"]:
        stripped_addr = friend["ip_address"][7:16]
        if stripped_addr == ip:
            return True
    return False


def process_get(m_split, addr):
    filename = m_split[0]
    friend_or_foe = check_fof(addr)
    # print(friend_or_foe)
    if "?" in filename:
        # print("im in the question")
        request_dict = parse_filename_request(filename[1:])
        # print(request_dict)
        response = b"HTTP/1.1 200 OK\r\n\r\n"

        if "update_feed" in request_dict:
            if request_dict["update_feed"] == "true":
                feed_response = create_feed_json()
                json_feed = json.dumps(feed_response, indent=2)
                response += str.encode(json_feed)
        # print(response)
        response += b"\r\n"
        return response

    else:
        if filename == "/status.json" and not friend_or_foe:
            return b"HTTP/1.1 404 FILE NOT FOUND\r\n\r\n"
        with open(filename[1:], "br") as f:
            output_data = f.read()
        response = b"HTTP/1.1 200 OK\r\n\r\n"
        # Send the content of the requested file to the connection socket
        response += output_data
        response += b"\r\n"

    return response


def process_put(m_split, addr):
    filename = m_split[0]
    filename = filename[1:]
    # # print(filename)
    request_dict = parse_filename_request(filename)
    # # print(request_dict)
    if "updatestatus" in request_dict:
        toSave = request_dict["updatestatus"]
        toSave = urllib.parse.unquote(toSave)
        add_status(toSave)

    if "updatelikes" in request_dict:
        if request_dict["updatelikes"] == "req":
            my_status_feed = get_json("status.json")
            complete_ip = addr[0]
            for status in my_status_feed["updates"]:
                feed_id = status["timestamp"].split()[1]
                print("local feed_id", feed_id)
                print("incoming feed_id", request_dict["feed_id"])
                if request_dict["feed_id"] == feed_id:
                    if complete_ip not in status["likes"]:
                        status["likes"].append(complete_ip)
            save_json("status.json", my_status_feed)
        else:
            my_friends = get_json("friends.json")
            print(request_dict)
            for friend in my_friends["friends"]:
                print("checking my friends")
                curr_friend = urllib.parse.unquote(request_dict["friend_name"])
                if friend["name"] == curr_friend:
                    print("I have a friend")
                    requests.put(friend["ip_address"]+"?updatelikes=req&feed_id=" + request_dict["feed_id"])

    response = b"HTTP/1.1 200 OK\r\n\r\n"
    return response


def process(connectionSocket, address):
    try:
        # Receives the request message from the client
        message = connectionSocket.recv(1024)
        m_split = message.decode(encoding='UTF-8').split()
        print(m_split)
        response = ""
        method = m_split[0]
        if method == "GET":
            response = process_get(m_split[1:], address[0])
        elif method == "PUT":
            response = process_put(m_split[1:], address)
        connectionSocket.send(response)
        connectionSocket.close()

    except (IOError, IndexError):  # Send HTTP response message for file not found
        response = "HTTP/1.1 404 Not Found\r\n\r\n"
        response += "<html><head></head><body><h1>404 Not Found</h1></body></html>\r\n"
        connectionSocket.send(response.encode())
        connectionSocket.close()


while True:
    # Set up a new connection from the client
    connectionSocket, addr = serverSocket.accept()
    # Clients timeout after 60 seconds of inactivity and must reconnect.
    connectionSocket.settimeout(60)
    # start new thread to handle incoming request
    _thread.start_new_thread(process, (connectionSocket, addr,))

serverSocket.close()
