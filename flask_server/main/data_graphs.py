import pandas as pd
import os

path_data = ".." + os.sep + "static" + os.sep + "data" + os.sep


def get_df_summary():
    total_py_pkgs = 0
    total_npm_pkgs = 0
    total_go_pkgs = 0
    total_rb_pkgs = 0
    graph1_data = []

    for root, directories, files in os.walk('..'):
        for nm in files:
            if not nm.startswith('.'):
                df = pd.read_json(os.path.join(root, nm))
                if 'python' in root:
                    total_py_pkgs += len(df.columns)

                if 'npm' in root:
                    total_npm_pkgs += len(df.columns)

                if 'go' in root:
                    total_go_pkgs += len(df.columns)

                if 'ruby' in root:
                    total_rb_pkgs += len(df.columns)

    if total_py_pkgs > 0:
        graph1_data.append({"repo": "PyPi", "totalpkgs": total_py_pkgs})
    if total_npm_pkgs > 0:
        graph1_data.append({"repo": "NPM", "totalpkgs": total_npm_pkgs})
    if total_rb_pkgs > 0:
        graph1_data.append({"repo": "Gems", "totalpkgs": total_rb_pkgs})
    if total_go_pkgs > 0:
        graph1_data.append({"repo": "GoLang", "totalpkgs": total_go_pkgs})

    print(graph1_data)

    return graph1_data


def get_df_graph2():
    total_py_files = 0
    total_py_typos = 0
    total_py_urls = 0
    total_py_ips = 0
    total_py_emails = 0
    total_py_vulns = 0
    total_py_vt = 0

    total_npm_files = 0
    total_npm_typos = 0
    total_npm_urls = 0
    total_npm_ips = 0
    total_npm_emails = 0
    total_npm_vulns = 0
    total_npm_vt = 0

    total_go_files = 0
    total_go_typos = 0
    total_go_urls = 0
    total_go_ips = 0
    total_go_emails = 0
    total_go_vulns = 0
    total_go_vt = 0

    total_rb_files = 0
    total_rb_typos = 0
    total_rb_urls = 0
    total_rb_ips = 0
    total_rb_emails = 0
    total_rb_vulns = 0
    total_rb_vt = 0

    graph2_data = []

    for root, directories, files in os.walk('..'):
        for nm in files:
            if not nm.startswith('.'):
                df = pd.read_json(os.path.join(root, nm), orient='index')
                if 'python' in root:
                    if "hash_files" in df.columns:
                        total_py_files += df["hash_files"][0].\
                                              values().__len__() - 1
                    if "typo_urls" in df.columns:
                        total_py_typos += df["typo_urls"][0].values().__len__()
                    if "data_collected" in df.columns:
                        total_py_urls += df["data_collected"][0][
                            "urls"].__len__()
                        total_py_ips += df["data_collected"][0][
                            "ips"].__len__()
                        total_py_emails += df["data_collected"][0][
                            "emails"].__len__()
                    if "appinspector" in df.columns and (
                            df["appinspector"][0].values() ==
                            "Called Process Error" or df[
                                "appinspector"][0].__len__() > 0):
                         total_py_vulns += df["appinspector"][0].\
                             values().__len__()
                    if "bandit" in df.columns and (df["bandit"][0] != ""):
                        total_py_vulns += df["bandit"][0]["results"].\
                            values().__len__()
                    if "virustotal" in df.columns and \
                            df["virustotal"][0] != "":
                        total_py_vt += df["virustotal"].__len__()

                if 'npm' in root:
                    if "hash_files" in df.columns:
                        total_npm_files += df["hash_files"][0].\
                                               values().__len__() - 1
                    if "typo_urls" in df.columns:
                        total_npm_typos += df["typo_urls"][0].\
                            values().__len__()
                    if "data_collected" in df.columns:
                        total_npm_urls += df["data_collected"][0][
                            "urls"].__len__()
                        total_npm_ips += df["data_collected"][0][
                            "ips"].__len__()
                        total_npm_emails += df["data_collected"][0][
                            "emails"].__len__()
                    if "appinspector" in df.columns and \
                            (df["appinspector"][0].values() ==
                             "Called Process Error" or df[
                                 "appinspector"][0].__len__() > 0):
                        total_npm_vulns += df["appinspector"][0].values()\
                            .__len__()
                    if "virustotal" in df.columns and \
                            df["virustotal"][0] != "":
                        total_npm_vt += df["virustotal"].__len__()

                if 'go' in root:
                    if "hash_files" in df.columns:
                        total_go_files += df["hash_files"][0].\
                                              values().__len__() - 1
                    if "typo_urls" in df.columns:
                        total_go_typos += df["typo_urls"][0].\
                            values().__len__()
                    if "data_collected" in df.columns:
                        total_go_urls += df["data_collected"][0][
                            "urls"].__len__()
                        total_go_ips += df["data_collected"][0][
                            "ips"].__len__()
                        total_go_emails += df["data_collected"][0][
                            "emails"].__len__()
                    if "appinspector" in df.columns and \
                            (df["appinspector"][0].values() ==
                             "Called Process Error" or df[
                                 "appinspector"][0].__len__() > 0):
                         total_go_vulns += df["appinspector"][0].\
                             values().__len__()
                    if "virustotal" in df.columns and \
                            df["virustotal"][0] != "":
                        total_go_vt += df["virustotal"].__len__()

                if 'ruby' in root:
                    if "hash_files" in df.columns:
                        total_rb_files += df["hash_files"][0].values().__len__() - 1
                    if "typo_urls" in df.columns:
                        total_rb_typos += df["typo_urls"][0].values().__len__()
                    if "data_collected" in df.columns:
                        total_rb_urls += df["data_collected"][0][
                            "urls"].__len__()
                        total_rb_ips += df["data_collected"][0][
                            "ips"].__len__()
                        total_rb_emails += df["data_collected"][0][
                            "emails"].__len__()
                    if "appinspector" in df.columns and \
                            (df["appinspector"][0].values() ==
                             "Called Process Error" or
                             df["appinspector"][0].__len__() > 0):
                        total_rb_vulns += df["appinspector"][0].\
                            values().__len__()
                    if "virustotal" in df.columns and \
                            df["virustotal"][0] != "":
                        total_rb_vt += df["virustotal"].__len__()

    graph2_data.append({"Repo": "PyPi", "Typos": total_py_typos,
                        "#Files": total_py_files, "IPs": total_py_urls,
                        "URLs": total_py_urls, "Emails": total_py_emails,
                        "Issues": total_py_vulns, "VirusTotal": total_py_vt})
    graph2_data.append({"Repo": "NPM", "Typos": total_npm_typos,
                        "#Files": total_npm_files, "IPs": total_npm_urls,
                        "URLs": total_npm_urls, "Emails": total_npm_emails,
                        "Issues": total_npm_vulns, "VirusTotal": total_npm_vt})
    graph2_data.append({"Repo": "Ruby", "Typos": total_rb_typos,
                        "#Files": total_rb_files, "IPs": total_rb_urls,
                        "URLs": total_rb_urls,  "Emails": total_rb_emails,
                        "Issues": total_rb_vulns, "VirusTotal": total_rb_vt})
    graph2_data.append({"Repo": "Go", "Typos": total_go_typos,
                        "#Files": total_go_files, "IPs": total_go_urls,
                        "URLs": total_go_urls, "Emails": total_go_emails,
                        "Issues": total_go_vulns, "VirusTotal": total_go_vt})

    print(graph2_data)

    return graph2_data
