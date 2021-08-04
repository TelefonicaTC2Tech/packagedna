
import re
import json
import semver
import urllib.request
from packaging import version as v
from parsel import Selector

from auxiliar_functions.globals import gt
from auxiliar_functions.globals import ge
from auxiliar_functions.globals import lts
from auxiliar_functions.globals import les
from auxiliar_functions.globals import url_cve


def cve_git(packname, language, version):
    report = dict()
    report[version] = dict()
    try:
        sel = Selector(
            text=str(urllib.request.urlopen(
                url_cve + packname.lower() + '+ecosystem%3A' + language)
                     .read()), type='html')

        cant = sel.xpath('//*[@id="js-pjax-container"]/div/div[2]/'
                         'div[2]/div[1]/div[1]/h2').get()
        cant = cant[cant.find('\\n        ') + 10:cant.find(' advisor')]

        urls = list()
        if int(cant) >= 25:
            cant = '25'

        for i in range(0, int(cant)):
            url_adv = sel.xpath(f'//*[@id="js-pjax-container"]/div/div[2]/div'
                                f'[2]/div[1]/div[{str(i + 2)}]/div/div[2]/'
                                f'div/a').get()
            urls.append('https://github.com' + url_adv[url_adv.find(
                'href="') + 6:url_adv.find('" class')])

        for url in urls:
            sel2 = Selector(text=str(
                urllib.request.urlopen(url).read()), type='html')

            cve_affect = []

            j = 1
            while j != 0:

                cve_versions = sel2.xpath('//*[@id="js-pjax-container"]'
                                          '/div/div[2]/div[1]/div[1]/div/div/'
                                          'div[2]/div[' + str(j) + ']').get()

                if cve_versions is not None:
                    cve_versions = cve_versions[
                                   cve_versions.find('ry f4">') + 8:
                                   cve_versions.find('</div>')]
                    cve_versions = cve_versions.split(', ')
                    cve_affect.append(cve_versions)
                    j += 1
                else:
                    j = 0

                """if any([v.parse(version) <= v.parse(tt)
                        for tt in [".".join([y for y in x[0] if y.isnumeric()])
                                   for x in cve_affect]]):"""
                if comp_versions(cve_affect, version) and j != 0:

                    cve_report = sel2.xpath('//*[@id="js-pjax-container"]/div'
                                            '/div[2]/div[2]/div[1]/div').get()
                    cve_report = cve_report[cve_report.find('t-2">') + 5:
                                            cve_report.find('</div>')]
                    cve_name = sel2.xpath(
                        '//*[@id="js-pjax-container"]/div/div[1]/h2').get()
                    cve_name = cve_name[cve_name.find('heading">     ') + 15:
                                        cve_name.find('\\n</h2>')]
                    cve_date = sel2.xpath('//*[@id="js-pjax-container"]/div/'
                                          'div[1]/div/span[2]/'
                                          'relative-time[1]').get()
                    cve_date = cve_date[cve_date.find('time="') + 6:
                                        cve_date.find('T')]
                    cve_severity = sel2.xpath('//*[@id="js-pjax-container"]'
                                              '/div/div[1]/div/span[1]').get()
                    cve_severity = cve_severity[
                                   cve_severity.find('">\\n  ') + 6:
                                   cve_severity.find('\\n</span>')]
                    report[version][cve_report] = dict(name=cve_name,
                                                       date=cve_date,
                                                       severity=cve_severity,
                                                       affected=cve_affect,
                                                       url=url)

        return json.dumps(report)

    except:
        return json.dumps(report)


def comp_versions(cve_affect, version):
    def normalize(v):
        parts = [int(float(x)) for x in re.findall(r'-?\d+\.?d*', v)]
        i = 0
        ver_nor = ''
        if len(parts) >= 3:
            while i <= 2:
                ver_nor = ver_nor + str(parts[i]) + '.'
                i += 1
        else:
            parts.extend([0] * (3 - len(parts)))
            while i <= 2:
                ver_nor = ver_nor + str(parts[i]) + '.'
                i += 1

        return ver_nor.rsplit('.', 1)[0]

    for cves in cve_affect:
        if len(cves) == 1 and cves[0].split('; ')[0] == 'gt' and \
                semver.compare(normalize(version), normalize(cves[0].split(
                '; ')[1])) == 1:
            return True

        elif len(cves) == 1 and cves[0].split('; ')[0] == 'lt' and \
                semver.compare(normalize(version), normalize(cves[0].split(
                    '; ')[1])) == -1:
            return True

        elif len(cves) == 1 and cves[0].split(';= ')[0] == 'gt' and \
                semver.compare(normalize(version), normalize(cves[0].split(
                    ';= ')[1])) >= 0:
            return True

        elif len(cves) == 1 and cves[0].split(';= ')[0] == 'lt' and \
                semver.compare(normalize(version), normalize(cves[0].split(
                    ';= ')[1])) <= 0:
            return True

        elif len(cves) > 1 and cves[0].find(gt) == 0 and cves[1].find(
                lts) == 0 and semver.compare(normalize(version), normalize(
                        cves[0].split('; ')[1])) == 1 and semver.compare(
                    normalize(version), normalize(
                        cves[1].split('; ')[1])) == -1:
            return True

        elif len(cves) > 1 and cves[0].find(gt) == 0 and cves[1].find(
                les) == 0 and semver.compare(normalize(version), normalize(
                        cves[0].split('; ')[1])) == 1 and semver.compare(
                    normalize(version), normalize(
                        cves[1].split(';= ')[1])) <= 0:
            return True

        elif len(cves) > 1 and cves[0].find(ge) == 0 and cves[1].find(
                lts) == 0 and semver.compare(normalize(version), normalize(
                        cves[0].split(';= ')[1])) >= 0 and semver.compare(
                    normalize(version), normalize(
                        cves[1].split('; ')[1])) == -1:
            return True

        elif len(cves) > 1 and cves[0].find(ge) == 0 and cves[1].find(
                les) == 0 and semver.compare(normalize(version), normalize(
                        cves[0].split(';= ')[1])) >= 0 and semver.compare(
                    normalize(version), normalize(
                cves[1].split(';= ')[1])) <= 0:
            return True

        else:
            pass

    return False
