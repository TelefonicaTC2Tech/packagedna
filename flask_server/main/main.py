from flask import Blueprint, render_template, request, jsonify
import os
import json
from .data_graphs import get_df_summary, get_df_graph2
from flask import Blueprint, render_template, request, jsonify
main = Blueprint("main", __name__)


@main.before_app_request
def set_variables():
    global data, data_keys, package_name
    SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
    package_language = os.environ.get('PACKAGE_LANGUAGE')
    json_url = os.path.join(SITE_ROOT, os.pardir, "static" + os.sep + "data" +
                            os.sep + package_language + os.sep,
                            os.environ.get('JSON_PACKAGE_NAME').
                            replace('/', '_-_'))

    if os.path.isfile(json_url):
        data = json.load(open(json_url))

    elif os.path.isfile(os.path.join(
            SITE_ROOT, "static" + os.sep + "data" + os.sep + package_language
                       + os.sep, os.environ.get('JSON_PACKAGE_NAME').split("-")[0])):
        json_url = os.path.join(
            SITE_ROOT, "static" + os.sep + "data" + os.sep + package_language
                       + os.sep,
            os.environ.get('JSON_PACKAGE_NAME').split("-")[0])
        data = json.load(open(json_url))

    elif os.path.isfile(os.path.join(
            SITE_ROOT, "static" + os.sep + "data" + os.sep +
                       package_language + os.sep,
            os.environ.get('JSON_PACKAGE_NAME').replace('-', '.'))):
        json_url = os.path.join(SITE_ROOT, "static" + os.sep + "data" +
                                os.sep + package_language + os.sep,
                                os.environ.get(
                                    'JSON_PACKAGE_NAME').replace('-', '.'))
        data = json.load(open(json_url))

    data_keys = sorted(list(data.keys()))[::-1]
    package_name = data[data_keys[0]]['name']

    # Patch Temp - Generar con este item en el original rta.json
    data.update({"changes_pkg": {"name": package_name, "chg_author": "",
                                 "chg_author_email": "", "chg_home_page": "",
                                 "chg_datac_urls": {}, "chg_datac_hash": {},
                                 "chg_datac_ips": {}, "chg_datac_emails":
                                     {}}})


@main.route('/')
def index():
    return render_template('index.html',
                           data=data,
                           data_keys=data_keys,
                           package_name=package_name)


@main.route('/compare_process', methods=["POST"])
def compare_process():
    val_pkg1 = request.form['select_pkg1'].replace('__', '.')
    val_pkg2 = request.form['select_pkg2'].replace('__', '.')
    data_compare = {}
    data_compare.update({"name": package_name})
    # data.update(data_compare)
    if data[val_pkg1]["author"] != data[val_pkg2]["author"]:
        data_compare.update({"chg_author": "1"})
    if data[val_pkg1]["author_email"] != data[val_pkg2]["author_email"]:
        data_compare.update({"chg_author_email": "1"})
    if data[val_pkg1]["home_page"] != data[val_pkg2]["home_page"]:
        data_compare.update({"chg_home_page": "1"})

    diff_fhashs = set(list(data[val_pkg1]["hash_files"].values())) - set(
        list(data[val_pkg2]["hash_files"].values()))
    data_compare["chg_files_hashes"] = {data_diff: "1" for data_diff
                                        in diff_fhashs}

    if len(data[val_pkg1]["data_collected"]["urls"]) >= len(
            data[val_pkg2]["data_collected"]["urls"]):
        val_max_urls = data[val_pkg1]["data_collected"]["urls"]
        val_min_urls = data[val_pkg2]["data_collected"]["urls"]

    else:
        val_min_urls = data[val_pkg1]["data_collected"]["urls"]
        val_max_urls = data[val_pkg2]["data_collected"]["urls"]

    if len(data[val_pkg1]["data_collected"]["hashs"]) >= len(
            data[val_pkg2]["data_collected"]["hashs"]):
        val_max_hashs = data[val_pkg1]["data_collected"]["hashs"]
        val_min_hashs = data[val_pkg2]["data_collected"]["hashs"]

    else:
        val_min_hashs = data[val_pkg1]["data_collected"]["ips"]
        val_max_hashs = data[val_pkg2]["data_collected"]["ips"]

    if len(data[val_pkg1]["data_collected"]["ips"]) >= len(
            data[val_pkg2]["data_collected"]["ips"]):
        val_max_ips = data[val_pkg1]["data_collected"]["ips"]
        val_min_ips = data[val_pkg2]["data_collected"]["ips"]

    else:
        val_min_ips = data[val_pkg1]["data_collected"]["ips"]
        val_max_ips = data[val_pkg2]["data_collected"]["ips"]

    if len(data[val_pkg1]["data_collected"]["emails"]) >= len(
            data[val_pkg2]["data_collected"]["emails"]):
        val_max_emails = data[val_pkg1]["data_collected"]["emails"]
        val_min_emails = data[val_pkg2]["data_collected"]["emails"]

    else:
        val_min_emails = data[val_pkg1]["data_collected"]["emails"]
        val_max_emails = data[val_pkg2]["data_collected"]["emails"]

    diff_datac_urls = set(list(val_max_urls)) - set(list(val_min_urls))
    data_compare["chg_datac_urls"] = {data_diff: "1" for data_diff in
                                      diff_datac_urls}

    diff_datac_hash = set(list(val_max_hashs)) - set(list(val_min_hashs))
    data_compare["chg_datac_hash"] = {data_diff: "1" for data_diff in
                                      diff_datac_hash}

    diff_datac_ips = set(list(val_max_ips)) - set(list(val_min_ips))
    data_compare["chg_datac_ips"] = {data_diff: "1" for data_diff in
                                     diff_datac_ips}

    diff_datac_emails = set(list(val_max_emails)) - set(list(val_min_emails))
    data_compare["chg_datac_emails"] = {data_diff: "1" for data_diff in
                                        diff_datac_emails}

    if data[val_pkg1]['appinspector'] != data[val_pkg2]['appinspector']:
        data_compare.update({"chg_appinspector": "7"})

    data.update({"changes_pkg": data_compare})

    print(json.dumps(data, indent=4))

    rep = {"data": data, "data_keys": data_keys, "package_name": package_name}

    return jsonify(rep)


@main.route('/compare', methods=["GET"])
def compare():
    print(json.dumps(data, indent=4))
    return render_template('compare.html',
                           data=data,
                           data_keys=data_keys,
                           package_name=package_name)


@main.route('/dashboard', methods=["GET"])
def dashboard():
    return render_template('dashboard.html')


@main.route('/get-json', methods=['GET', 'POST'])
def get_json():
    # graph1_data_json = [{"repo": "Pyi", "totalpkgs": 10}, {"repo": "NPM",
# "totalpkgs": 20}, {"repo": "Gems", "totalpkgs": 5}, {"repo": "GoLang",
# "totalpkgs": 17}]
    graph1_data_json = get_df_summary()
    # print(graph1_data_json)
    return jsonify(graph1_data_json)


@main.route('/get-json2', methods=['GET', 'POST'])
def get_json2():
# graph2_data_json = [{"Race":"R1","HTC":270,"Registry":449,"Traffic":34},{"Race":"R2","HTC":202,"Registry":327,"Traffic":34},{"Race":"R3","HTC":120,"Registry":214,"Traffic":34},{"Race":"R4","HTC":114,"Registry":193},{"Race":"R5","HTC":894,"Registry":155,"Traffic":34},{"Race":"R6","HTC":737,"Registry":134,"Traffic":34}]
    graph2_data_json = get_df_graph2()
# graph2_data_json = get_df_graph2()
    return json.dumps(graph2_data_json)


@main.route('/simple-compare')
def simple_compare():
    return render_template('simple-compare.html',
                           data=data,
                           data_keys=data_keys,
                           package_name=package_name)