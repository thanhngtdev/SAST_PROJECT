# # import os
# # import re
# # import time
# # import RestAPI
# from requests_toolbelt import MultipartEncoder
# # cx = RestAPI.CxRestAPI()

# # def check_tool_checkmarx(src):
# #     global project_name, team_id
# #     #print("* Welcome to use this scripts! *")
# #     #flag = input("- Do you want to create a new project?(Y/N)")
# #     # if flag.upper() == "Y":
# #     teams = cx.get_all_teams().json()
# #     num = 0
# #     team_id = teams[num].get("id")
# #     project_name = os.path.splitext(os.path.basename(src))[0]
# #     project_id = cx.create_project_with_default_configuration(name=project_name, owning_team=team_id).json().get("id")
# #     zip_path = "/home/thuan/Downloads/JavaSpringBootExample-master.zip"
# #     report_types = "XML"
# #     report_code = 0
# #     # for type in report_types:
# #     #     print("\t[{}]".format(report_code), type)
# #     #     report_code += 1
# #     # report_code = int(input("- Choose a report type:"))
# #     cx.upload_source_code_zip_file(project_id=project_id, zip_path=zip_path)
# #     # print("* Creating a new scan...")
# #     scan = cx.create_new_scan(project_id)
# #     scan_id = scan.json().get("id")
# #     while True:
# #         scan_status = cx.get_sast_scan_details_by_scan_id(id=scan_id).json().get("status").get("name")
# #         if scan_status == "Finished":
# #             print()
# #             break
# #         # print("Re-Check after 10s ...")
# #         time.sleep(10)
# #     report_type = report_types[report_code].lower()
# #     report = cx.register_scan_report(report_type=report_type, scan_id=scan_idY
# # )
# #     report_id = report.json().get("reportId")
# #     while True:
# #         report_status = cx.get_report_status_by_id(report_id).json().get("status").get("value")
# #         if report_status == "Created":
# #             print()
# #             break
# #         # print("Re-Check after 5s ...")
# #         time.sleep(5)
# #     report_name = project_name + "." + report_type
# #     reports = cx.get_reports_by_id(report_id, report_type).content
# #     with open(os.path.expanduser(report_name), 'wb') as f:
# #         f.write(reports)
# #     # print("* Successful! Thanks for use. *")
# # src= "/home/thuan/Downloads/JavaSpringBootExample-master.zip"
# # check_tool_checkmarx(src)

# import RestAPI
# import time
# import os

# cx = RestAPI.CxRestAPI()


# def choose_a_project():
#     num = 0
#     project_list = cx.get_all_project_details()
#     for project in project_list:
#         print("\t[{}] ".format(num), project.get("name"))
#         num += 1
#     num = int(input("- Choose a project:"))
#     return project_list[num].get("id"), project_list[num].get("name")


# def main():
#     global project_name, team_id
#     print("* Welcome to use this scripts! *")
#     flag = input("- Do you want to create a new project?(Y/N)")
#     if flag.upper() == "Y":
#         teams = cx.get_all_teams().json()
#         num = 0
#         for team in teams:
#             print("\t[{}] ".format(num), team.get("fullName"))
#             num += 1
#         num = int(input("- Choose a team to create project:"))
#         team_id = teams[num].get("id")
#         project_name = input("- Set your project name:")
#         project_id = cx.create_project_with_default_configuration(name=project_name, owning_team=team_id).json().get("id")
#     else:
#         project_id, project_name = choose_a_project()
#     zip_path = input("- Set the zip file path:")
#     report_types = ["PDF", "RTF", "CSV", "XML"]
#     report_code = 0
#     for type in report_types:
#         print("\t[{}]".format(report_code), type)
#         report_code += 1
#     report_code = int(input("- Choose a report type:"))
#     cx.upload_source_code_zip_file(project_id=project_id, zip_path=zip_path)
#     print("* Creating a new scan...")
#     scan = cx.create_new_scan(project_id)
#     scan_id = scan.json().get("id")
#     while True:
#         scan_status = cx.get_sast_scan_details_by_scan_id(id=scan_id).json().get("status").get("name")
#         print("\tScan status：[", scan_status, "]", end=" ")
#         if scan_status == "Finished":
#             print()
#             break
#         print("Re-Check after 10s ...")
#         time.sleep(10)
#     print("* Creating report...")
#     report_type = report_types[report_code].lower()
#     report = cx.register_scan_report(report_type=report_type, scan_id=scan_id)
#     report_id = report.json().get("reportId")
#     while True:
#         report_status = cx.get_report_status_by_id(report_id).json().get("status").get("value")
#         print("\tReport status：[", report_status, "]", end=" ")
#         if report_status == "Created":
#             print()
#             break
#         print("Re-Check after 5s ...")
#         time.sleep(5)
#     report_name = project_name + "." + report_type
#     reports = cx.get_reports_by_id(report_id, report_type).content
#     with open(os.path.expanduser(report_name), 'wb') as f:
#         f.write(reports)
#     print("* Successful! Thanks for use. *")


# if __name__ == '__main__':
#     main()

# # file = open('/home/thuan/Downloads/JavaSpringBootExample-master.zip', 'rb').read()
# # print(file)
# # import os

# # def upload_source_code_zip_file(zip_path):
# #     file_name = os.path.basename(zip_path)
# #     files = MultipartEncoder(fields={"zippedSource": (file_name, open(zip_path, 'rb'), "application/zip")})
# #     print(files)

# # upload_source_code_zip_file("/home/thuan/Downloads/JavaSpringBootExample-master.zip")

import time
from datetime import datetime
import os
from bs4 import BeautifulSoup

from os.path import normpath, join, dirname, exists

from CheckmarxPythonSDK.CxRestAPISDK import TeamAPI
from CheckmarxPythonSDK.CxRestAPISDK import ProjectsAPI
from CheckmarxPythonSDK.CxRestAPISDK import ScansAPI
from CheckmarxPythonSDK.config import config

def scan_from_local(team_full_name, project_name, report_type, zip_file_path, report_folder=None):
    """

    Args:
        team_full_name (str):
        project_name (str):
        report_type (str):
        zip_file_path (str)
        report_folder (str):

    Returns:

    """

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
                print(list_result)
if __name__ == "__main__":
    zip_file_path = "/home/thuan/SASTool_worker/media/documents/2022/04/13/JavaSpringBootExample-master.zip"
    scan_from_local(team_full_name="/CxServer",
                    # # project_name="jvl_local",
                    # project_name=os.path.splitext(os.path.basename("/home/thuan/SASTool_worker/media/documents/2022/04/13/JavaSpringBootExample-master.zip"))[0] + datetime.now().strftime('_%Y_%m_%d_%H_%M_%S'),
                    # report_type="XML",
                    # # zip_file_path=normpath(join(os.path.dirname(__file__), "JavaVulnerableLab-master.zip")),
                    # zip_file_path="/home/thuan/SASTool_worker/media/documents/2022/04/13/JavaSpringBootExample-master.zip",
                    # report_folder=config.get("report_folder"))
                    # # report_folder="./result")
                    project_name = os.path.splitext(os.path.basename(zip_file_path))[0] + datetime.now().strftime('_%Y_%m_%d_%H_%M_%S'),
                    report_type = "XML",
                    zip_file_path = zip_file_path,
                    report_folder = config.get("report_folder"))
