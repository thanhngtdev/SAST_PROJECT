from celery import shared_task
from django.conf import settings
import json
import os
import shutil
import subprocess
import time
from datetime import datetime
import os
from bs4 import BeautifulSoup

from os.path import normpath, join, dirname, exists

from CheckmarxPythonSDK.CxRestAPISDK import TeamAPI
from CheckmarxPythonSDK.CxRestAPISDK import ProjectsAPI
from CheckmarxPythonSDK.CxRestAPISDK import ScansAPI
from CheckmarxPythonSDK.config import config

@shared_task(name='dependency_check_tool')
def dependency_check_tool(src_folder):
    os.system('./tool/dependency-check/bin/dependency-check.sh --scan ' + src_folder + ' -f=JSON')
    with open('dependency-check-report.json', 'r') as js:
        json_load = json.load(js)
        # check_tool_dependency(data_report_dependency)
        # @shared_task(name='process-tool')
        # def check_tool_dependency(json_load):
        list_cve = []
        appDict1 = {}
        count_dependencies = len(json_load['dependencies'])
        for i in range(0, count_dependencies):
            length = len(json_load['dependencies'][i])
            if length > 8:
                package = json_load['dependencies'][i]['packages'][0]['id']
                if 'vulnerabilities' in str(json_load['dependencies'][i]):
                    count_vulnerabilities = len(json_load['dependencies'][i]['vulnerabilities'])
                    for j in range(0, count_vulnerabilities):
                        length2 = len(json_load['dependencies'][i]['vulnerabilities'][j])
                        if length2 == 10:
                            name = json_load['dependencies'][i]['vulnerabilities'][j]['name']
                            severity = json_load['dependencies'][i]['vulnerabilities'][j]['severity']
                            score = json_load['dependencies'][i]['vulnerabilities'][j]['cvssv3']['baseScore']
                            cwe = json_load['dependencies'][i]['vulnerabilities'][j]['cwes'][0]
                            appDict = {'Tools': 'Dependency', 'CVE': name, 'CWE': cwe, 'cvssScore': [score],
                                       'packageName': package, 'severity': severity}
                            list_cve += [name]

                            appDict1.update({name: appDict})
        with open('./result/final_report.json', 'a', encoding='utf-8') as output:
            json.dump(appDict1, output, indent=4)
    return list_cve


@shared_task(name='check_tool_snyk')
def check_tool_snyk(src_folder):
    os.system('cd ' + src_folder + ';snyk test --json > raw_report_snyk.json')
    shutil.copy2(src_folder + '//raw_report_snyk.json', './')
    with open('raw_report_snyk.json', 'r', encoding="utf8") as js:
        data_report = json.load(js)
        len_vulnerabilities = len(data_report['vulnerabilities'])  # len(data['vulnerabilities'][0])
        list_cve = []
        report_snyk = {}
        for i in range(0, len_vulnerabilities):
            cve = data_report['vulnerabilities'][i]['identifiers']['CVE']
            cwe = data_report['vulnerabilities'][i]['identifiers']['CWE']
            package = data_report['vulnerabilities'][i]['packageName']
            score = data_report['vulnerabilities'][i]['cvssScore']
            severity = data_report['vulnerabilities'][i]['severity']
            appDict = {'Tools': 'Snyk', 'CVE': cve, 'CWE': cwe, 'cvssScore': score, 'packageName': package,
                       'severity': severity}

            len_cve = len(data_report['vulnerabilities'][i]['identifiers']['CVE'])
            if (len_cve > 0):
                for j in range(0, len_cve):
                    cve_m = data_report['vulnerabilities'][i]['identifiers']['CVE'][j]
                    list_cve.append(cve_m)

                    report_snyk.update({cve_m: appDict})
        with open('./result/final_report.json', 'a', encoding='utf-8') as output:
            json.dump(report_snyk, output, indent=4)
    return list_cve


@shared_task(name='check_tool_semgrep')
def check_tool_semgrep(src_folder):
    CONFIG = "p/owasp-top-ten"
    args = ['semgrep', f'--config={CONFIG}', src_folder, '--json', '--no-git-ignore']
    run = subprocess.run(args=args, capture_output=True, text=True)
    raw_data = json.loads(run.stdout)
    print(raw_data)
    # Chuẩn hóa kết quả, kết quả sau khi chuẩn hóa nằm trong list standardized_data
    standardized_data = []
    for p in raw_data['results']:

        if 'cwe' in p['extra']['metadata']:
            cweId = p['extra']['metadata']['cwe']
            cweId = cweId.split(":")[0]
            cweId = int(cweId.split("-")[1])

        temp = {}
        temp['cweId'] = cweId if cweId else 'None'
        temp['Path'] = p['path']
        temp['Line'] = p['start']['line']
        temp['CWE'] = p['extra']['metadata']['cwe'] if 'cwe' in p['extra']['metadata'] else "None"
        temp['OWASP'] = p['extra']['metadata']['owasp'] if 'owasp' in p['extra']['metadata'] else "None"
        temp['Description'] = p['extra']['message']
        temp['severity'] = p['extra']['severity']
        standardized_data.append(temp)
        with open('./result/final_report.json', 'a', encoding='utf-8') as output:
            json.dump(standardized_data, output, indent=4)

    return standardized_data
@shared_task(name='check_tool_checkmarx')
def check_tool_checkmarx(team_full_name, project_name, report_type, zip_file_path, report_folder=None):

    if not report_folder or not exists(report_folder):
        report_folder = dirname(__file__)

    if not exists(zip_file_path):
        print("zip file not found. \n abort scan.")
        return

    print(("team_full_name: {}, \n"
           "project_name: {}, \n"
           "report_type: {}, \n"
           "zip_file_path: {}, \n"
           "report_folder: {}").format(team_full_name, project_name, report_type,
                                       zip_file_path, report_folder))

    team_api = TeamAPI()
    projects_api = ProjectsAPI()
    scan_api = ScansAPI()

    # 2. get team id
    print("2. get team id")
    team_id = team_api.get_team_id_by_team_full_name(team_full_name)
    if not team_id:
        print("team: {} not exist".format(team_full_name))
        return

    project_id = projects_api.get_project_id_by_project_name_and_team_full_name(project_name=project_name,
                                                                                team_full_name=team_full_name)

    # 3. create project with default configuration, will get project id
    print("3. create project with default configuration, will get project id")
    if not project_id:
        project = projects_api.create_project_with_default_configuration(project_name=project_name, team_id=team_id)
        project_id = project.id
    print("project_id: {}".format(project_id))

    # 4. upload source code zip file
    print("4. upload source code zip file")
    projects_api.upload_source_code_zip_file(project_id, str(zip_file_path))

    # 6. set data retention settings by project id
    print("6. set data retention settings by project id")
    projects_api.set_data_retention_settings_by_project_id(project_id=project_id, scans_to_keep=3)

    # 7. define SAST scan settings
    print("7. define SAST scan settings")
    preset_id = projects_api.get_preset_id_by_name()
    print("preset id: {}".format(preset_id))
    scan_api.define_sast_scan_settings(project_id=project_id, preset_id=preset_id)

    projects_api.set_project_exclude_settings_by_project_id(project_id, exclude_folders_pattern="",
                                                            exclude_files_pattern="")

    # 8. create new scan, will get a scan id
    print("8. create new scan, will get a scan id")
    scan = scan_api.create_new_scan(project_id=project_id)
    scan_id = scan.id
    print("scan_id : {}".format(scan_id))

    # 9. get scan details by scan id
    print("9. get scan details by scan id")
    while True:
        scan_detail = scan_api.get_sast_scan_details_by_scan_id(scan_id=scan_id)
        scan_status = scan_detail.status.name
        print("scan_status: {}".format(scan_status))
        if scan_status == "Finished":
            break
        elif scan_status == "Failed":
            return
        time.sleep(10)

    # 11[optional]. get statistics results by scan id
    print("11[optional]. get statistics results by scan id")
    statistics = scan_api.get_statistics_results_by_scan_id(scan_id=scan_id)
    if statistics:
        print(statistics)

    # 12. register scan report
    print("12. register scan report")
    report = scan_api.register_scan_report(scan_id=scan_id, report_type=report_type)
    report_id = report.report_id
    print("report_id : {}".format(report_id))

    # 13. get report status by id
    print("13. get report status by id")
    while not scan_api.is_report_generation_finished(report_id):
        time.sleep(10)

    # 14. get report by id
    print("14. get report by id")
    report_content = scan_api.get_report_by_id(report_id)

    time_stamp = datetime.now().strftime('_%Y_%m_%d_%H_%M_%S')
    file_name = normpath(join(report_folder, project_name + time_stamp + "." + report_type))
    with open(str(file_name), "wb") as f_out:
        f_out.write(report_content)
    with open(str(file_name), "rb") as f:
        Bs_data= BeautifulSoup(f, "xml")
        queries = Bs_data.find_all('Query')
        list_result = []
        
        if queries:
            for i in queries:
                data = {
                    'name': i.get('name'),
                    'FileName': i.find('Result').get('FileName'),
                    'Severity': i.get('Severity'),
                    'Language': i.get('Language'),
                    'cweId': int(i.get('cweId')),
                    'category': i.get('category'),
                    'details': []
                }
                for j in i.find_all('PathNode'):
                    d = {
                        'line': j.find('Line').text,
                    }

                    if j.find('Code'):
                        d['code'] = j.find('Code').text.strip()

                    if len(data['details']) == 0:
                        data['details'].append(d)
                    else:
                        if d not in data['details']:
                            data['details'].append(d)
                list_result.append(data)
                # print(list_result)
                with open('./result/final_report.json', 'a', encoding='utf-8') as output:
                    json.dump(list_result, output, indent=4)
                
