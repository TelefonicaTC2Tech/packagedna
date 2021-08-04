
import json
import urllib.request


def npm_library(url, libraries, specific_version=None):
    try:
        npm_json = json.loads(
            urllib.request.urlopen(url).read().decode('utf-8'))
        if specific_version:
            return json.dumps({
                npm_json['versions'][specific_version]['name']: {
                    npm_json['versions'][specific_version]['version']: [
                        npm_json['versions'][specific_version][
                            'dist']['tarball'],
                        npm_json['versions'][specific_version][
                            'dist']['shasum']]
                }})
        libraries[npm_json['name']] = {}
        for version in npm_json['versions'].keys():
            libraries[
                npm_json['name']][version] = [
                npm_json['versions'][version]['dist']['tarball'],
                npm_json['versions'][version]['dist']['shasum']]
    except:
        libraries['error'] = 'error'
        libraries = json.dumps(libraries)
        return libraries

    libraries = json.dumps(libraries)
    return libraries
