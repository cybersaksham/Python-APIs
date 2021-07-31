# API Help
endpoint = "endpoint"
req = "requests"
get_req = "GET"
post_req = "POST"
desc = "Description"
inp = "Input"
out = "Output"
err = "Errors"

apis = [
    {
        endpoint: "/time",
        desc: "Gives current date & time",
        req: {
            get_req: {
                inp: {None: None},
                out: {"date": "Today's Date", "time": "Current Time"},
            },
        }
    },
    {
        endpoint: "/day",
        desc: "Gives day of week",
        req: {
            get_req: {
                inp: {None: None},
                out: {"day": "Today's Day (Sunday...)"},
            },
            post_req: {
                inp: {"date": "In format yyyy-mm-dd"},
                out: {"day": "Day at Given Date (Sunday...)"},
            },
        }
    },
    {
        endpoint: "/email",
        desc: "Send email to anyone",
        req: {
            post_req: {
                inp: {"from": "Sender's Email", "to": "Receiver's Email",
                      "password": "Sender's Password", "subject": "Email Subject",
                      "message": "Message in Email"},
                out: {"sent": "Is sent or not"},
            },
        }
    },
    {
        endpoint: "/mail_otp",
        desc: "Send otp to anyone by mail",
        req: {
            post_req: {
                inp: {"from": "Sender's Email", "to": "Receiver's Email",
                      "password": "Sender's Password"},
                out: {"sent": "Is sent or not", "otp": "Generated OTP"},
            },
        }
    },
    {
        endpoint: "/py_code",
        desc: "Get output or error of a python code string",
        req: {
            post_req: {
                inp: {"code": "Python Code", "stdin": "Input"},
                out: {"out": "Output or Error"},
            },
        }
    },
    {
        endpoint: "/geo_coordinates",
        desc: "Get latitude & longitude of a given address",
        req: {
            post_req: {
                inp: {"address": "Address of a place"},
                out: {"lat": "Latitude", "long": "Longitude",
                      "address": "Given Address", "complete_address": "Complete Address",
                      "error": "Error if any"},
                err: {"INTERNAL": "Internal Server Error",
                      "TIMEOUT": "Server timeout. Try again.",
                      "NOT_FOUND": "No address found"},
            },
        }
    },
    {
        endpoint: "/geo_address",
        desc: "Get address from given latitude & longitude",
        req: {
            post_req: {
                inp: {"lat": "Latitude", "long": "Longitude"},
                out: {"lat": "Latitude", "long": "Longitude",
                      "address": "Complete Address", "error": "Error if any"},
                err: {"INTERNAL": "Internal Server Error",
                      "TIMEOUT": "Server timeout. Try again.",
                      "NOT_FOUND": "No address found"},
            },
        }
    },
    {
        endpoint: "/geo_distance",
        desc: "Find distance(in kms) between two coordinates on earth.",
        req: {
            post_req: {
                inp: {"lat1": "Latitude 1", "long1": "Longitude 1",
                      "lat2": "Latitude 2", "long2": "Longitude 2"},
                out: {"lat1": "Latitude 1", "long1": "Longitude 1",
                      "lat2": "Latitude 2", "long2": "Longitude 2",
                      "distance": "Distance in kms", "error": "Error if any"},
                err: {"INTERNAL": "Internal Server Error",
                      "TIMEOUT": "Server timeout. Try again.",
                      "NOT_FOUND": "No coordinates found"},
            },
        }
    },
    {
        endpoint: "/mobile_trace",
        desc: "Traces a given mobile no.",
        req: {
            post_req: {
                inp: {"mob": "Mobile No (10 digit)"},
                out: {"response": "Response in json", "error": "Error if any"},
                "Response Json": {
                    "mob_no": "Mobile No",
                    "telecom_circle": "Telecom Circle",
                    "first_network": "First Network",
                    "current_network": "Current Network",
                    "signal": "Service Type",
                    "status": "Connection Status",
                    "owner": "Owner Name",
                    "location": "Live Location",
                    "last_login": "Last Login",
                    "last_live": "Last Live",
                    "telecom_capital": "Telecom Capital",
                    "main_language": "Main Language",
                    "local_time": "Local Time of mobile",
                },
                err: {"INTERNAL": "Internal Server Error",
                      "SERVER": "Server error. Try again."},
            },
        }
    },
]


# /time
def getTime():
    from datetime import datetime
    time_now = datetime.now()
    date_cur = str(time_now).split(" ")[0]
    time_cur = str(time_now).split(" ")[1].split(".")[0]
    return [date_cur, time_cur]


# /day
def getDay(date_cur):
    try:
        from datetime import datetime
        day_name = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        return day_name[datetime.strptime(date_cur, "%Y-%m-%d").weekday()]
    except:
        return None


# /email
def sendEmail(from_email, to_email, password, subject, message):
    try:
        from email.mime.text import MIMEText
        import smtplib
        msg = MIMEText(message, "plain")
        msg["Subject"] = subject
        msg["To"] = to_email
        msg["From"] = from_email
        gmail = smtplib.SMTP("smtp.gmail.com", 587)
        gmail.ehlo()
        gmail.starttls()
        gmail.login(from_email, password)
        gmail.send_message(msg)
        return True
    except:
        return False


# mail_otp
def sendMailOTP(from_email, to_email, password):
    try:
        from random import randint
        otp = randint(100000, 999999)
        response = sendEmail(from_email, to_email, password, "OTP", f"Your otp is {otp}")
        if response:
            return [True, otp]
        else:
            return [False, None]
    except:
        return [False, None]


# py_code
def pyCode(code_str, code_in):
    import sys
    from io import StringIO

    code_out = StringIO()

    sys.stdout = code_out
    sys.stdin = StringIO(code_in)

    try:
        exec(str(code_str))
    except Exception as err:
        print(err)

    sys.stdout = sys.__stdout__
    o = code_out.getvalue()

    code_out.close()

    return o


# geo_coordinates
def geo_coordinates(address):
    try:
        from geopy.geocoders import Nominatim
        from geopy.exc import GeocoderTimedOut
        import unidecode
        try:
            geo_locator = Nominatim(user_agent="http")
            location = geo_locator.geocode(address, timeout=10)
            return [location.latitude, location.longitude,
                    unidecode.unidecode(location.address), None]
        except GeocoderTimedOut as e:
            return [None, None, None, "TIMEOUT"]
        except Exception as e:
            return [None, None, None, "NOT_FOUND"]
    except ImportError as e:
        return [None, None, None, "INTERNAL"]


# geo_address
def geo_address(lat, long):
    try:
        from geopy.geocoders import Nominatim
        from geopy.exc import GeocoderTimedOut
        import unidecode
        try:
            geo_locator = Nominatim(user_agent="http")
            location = geo_locator.reverse(f"{lat}, {long}", timeout=10)
            return [location.latitude, location.longitude,
                    unidecode.unidecode(location.address), None]
        except GeocoderTimedOut as e:
            return [None, None, None, "TIMEOUT"]
        except Exception as e:
            return [None, None, None, "NOT_FOUND"]
    except ImportError as e:
        return [None, None, None, "INTERNAL"]


# geo_distance
def geo_distance(lat1, long1, lat2, long2):
    try:
        from geopy.distance import geodesic
        from geopy.exc import GeocoderTimedOut
        try:
            dist = geodesic((lat1, long1), (lat2, long2)).kilometers
            return [lat1, long1, lat2, long2, dist, None]
        except GeocoderTimedOut as e:
            return [None, None, None, None, None, "TIMEOUT"]
        except Exception as e:
            return [None, None, None, None, None, "NOT_FOUND"]
    except ImportError as e:
        return [None, None, None, None, None, "INTERNAL"]


# mobile_trace
def mob_trace(mob):
    try:
        from bs4 import BeautifulSoup
        import mechanize
        mc = mechanize.Browser()
        mc.set_handle_robots(False)

        try:
            url = 'https://www.findandtrace.com/trace-mobile-number-location'
            mc.open(url)

            mc.select_form(name='trace')
            mc['mobilenumber'] = mob  # Enter a mobile number
            res = mc.submit().read()

            soup = BeautifulSoup(res, 'html.parser')
            tbl = soup.find_all('table', class_='shop_table')

            fin_data = {}

            for j in range(2):
                data = tbl[j].find('tfoot')
                for i in data:
                    th = i.find('th')
                    td = i.find('td')
                    try:
                        fin_data[th.text.strip()] = td.text.strip()
                    except:
                        continue
            stripped_data = dict()
            stripped_data["mob_no"] = fin_data["Mobile Phone:"]
            stripped_data["telecom_circle"] = fin_data["Telecoms Circle / State"]
            stripped_data["first_network"] = fin_data["Original Network: (First Alloted)"]
            stripped_data["current_network"] = fin_data["Current Network"]
            stripped_data["signal"] = fin_data["Service Type / Signal:"]
            stripped_data["status"] = fin_data["Connection Status:"]
            stripped_data["owner"] = fin_data["Owner / Name of the caller:"]
            stripped_data["location"] = fin_data["Address / Current GPS Location:"]
            stripped_data["last_login"] = fin_data["Last Login Location (Facebook / Google Map / Twitter / Instagram )"]
            stripped_data["last_live"] = fin_data["Last Live location"]
            stripped_data["telecom_capital"] = fin_data["Telecom Circle Capital :"]
            stripped_data["main_language"] = fin_data["Main Language in the telecoms circle :"]
            stripped_data["local_time"] = " ".join(fin_data["Local time at phone location :"].split(" ")[:2])

            return [stripped_data, None]
        except:
            return [None, "SERVER"]
    except:
        return [None, "INTERNAL"]
