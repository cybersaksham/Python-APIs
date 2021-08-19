from flask import Flask, render_template, jsonify, request
from scripts import apis

app = Flask(__name__)


@app.route('/')
def home():
    return render_template("index.html", apis=apis.apis, len_apis=len(apis.apis))


@app.route('/time', methods=["GET"])
def getTime():
    date_cur, time_cur = apis.getTime()
    return jsonify(date=date_cur, time=time_cur)


@app.route('/day', methods=["GET", "POST"])
def getDay():
    date_cur = ""
    if request.method == "GET":
        date_cur = apis.getTime()[0]
    elif request.method == "POST":
        date_cur = request.args.get("date")
    day_cur = apis.getDay(date_cur)
    return jsonify(day=day_cur)


@app.route('/email', methods=["POST"])
def sendEmail():
    if request.method == "POST":
        from_email = request.args.get("from")
        to_email = request.args.get("to")
        password = request.args.get("password")
        subject = request.args.get("subject")
        message = request.args.get("message")
        response = apis.sendEmail(from_email, to_email, password, subject, message)
        return jsonify(sent=response)


@app.route('/mail_otp', methods=["POST"])
def sendMailOTP():
    if request.method == "POST":
        from_email = request.args.get("from")
        to_email = request.args.get("to")
        password = request.args.get("password")
        response, otp = apis.sendMailOTP(from_email, to_email, password)
        return jsonify(sent=response, otp=otp)


@app.route('/py_code', methods=["POST"])
def pyCode():
    import urllib
    if request.method == "POST":
        fin_url = str(urllib.parse.unquote(request.url)).split("?")[1].split("&")
        if fin_url[0].split("=")[0] == "code":
            code_str = "=".join(fin_url[0].split("=")[1:])
            code_in = "=".join(fin_url[1].split("=")[1:])
        else:
            code_str = "=".join(fin_url[1].split("=")[1:])
            code_in = "=".join(fin_url[0].split("=")[1:])
        out_str = apis.pyCode(code_str, code_in)
        return jsonify(out=out_str)


@app.route('/geo_coordinates', methods=["POST"])
def geo_coordinates():
    if request.method == "POST":
        address = request.args.get("address")
        lat, long, comp_address, e = apis.geo_coordinates(address)
        return jsonify(lat=lat, long=long, address=address, complete_address=comp_address, error=e)


@app.route('/geo_address', methods=["POST"])
def geo_address():
    if request.method == "POST":
        lat = request.args.get("lat")
        long = request.args.get("long")
        lat, long, comp_address, e = apis.geo_address(lat, long)
        return jsonify(lat=lat, long=long, address=comp_address, error=e)


@app.route('/geo_distance', methods=["POST"])
def geo_distance():
    if request.method == "POST":
        lat1_arg = request.args.get("lat1")
        long1_arg = request.args.get("long1")
        lat2_arg = request.args.get("lat2")
        long2_arg = request.args.get("long2")
        lat1, long1, lat2, long2, dist, e = apis.geo_distance(lat1_arg, long1_arg, lat2_arg, long2_arg)
        return jsonify(lat1=lat1, long1=long1, lat2=lat2, long2=long2, distance=dist, error=e)


@app.route('/mobile_trace', methods=["POST"])
def mob_trace():
    if request.method == "POST":
        mob_no = str(request.args.get("mob"))
        response, error = apis.mob_trace(mob_no)
        return jsonify(response=response, error=error)


@app.route('/get_age', methods=["GET"])
def get_age():
    if request.method == "GET":
        try:
            day__ = int(request.args.get("day"))
            month__ = int(request.args.get("month"))
            year__ = int(request.args.get("year"))
            res__, err__ = apis.get_age(day__, month__, year__)
            return jsonify(age=res__, error=err__)
        except ValueError:
            return jsonify(age=None, error="INCORRECT")
        except:
            return jsonify(age=None, error="INTERNAL")


if __name__ == '__main__':
    app.run()
