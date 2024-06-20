from typing import Annotated

from fastapi import FastAPI, Path

from lib.jiraConsultor import JiraConsultor
from lib.exportManager import ExportManager

app = FastAPI()

@app.get("/test")
def test_issue_def():

    jira : JiraConsultor = JiraConsultor("default")
    
    jira.login()
    jira.requestIssues()

    return jira.query[0]

@app.get("/test/{profile}")
def test_issue_prof(
    profile: Annotated[str, Path(title="The profile to query")],
):

    jira : JiraConsultor = JiraConsultor(profile)
    
    jira.login()
    jira.requestIssues()

    return jira.query[0]

@app.get("/print")
def print_issue_def():

    jira : JiraConsultor = JiraConsultor("default")
    
    jira.login()
    jira.requestIssues()

    headers = ["key"] + [x.split("/")[-1] for x in jira.domainAtributes["fields"]]
    return jira.findFields(jira.domainAtributes["fields"])

@app.get("/print/{profile}")
def print_issue_prof(
    profile: Annotated[str, Path(title="The profile to query")],
):

    jira : JiraConsultor = JiraConsultor(profile)
    
    jira.login()
    jira.requestIssues()

    headers = ["key"] + [x.split("/")[-1] for x in jira.domainAtributes["fields"]]
    return jira.findFields(jira.domainAtributes["fields"])

@app.get("/excel")
def excel_issue_def():

    jira : JiraConsultor = JiraConsultor("default")
    
    jira.login()
    jira.requestIssues()

    data = jira.findFields(jira.domainAtributes["fields"])
    headers = ["key"] + [x.split("/")[-1] for x in jira.domainAtributes["fields"]]
    expMan = ExportManager()
    expMan.exportToExcel(headers,data)

    return {"status": "done", "output":"/output"}

@app.get("/excel/{profile}")
def excel_issue_prof(
    profile: Annotated[str, Path(title="The profile to query")],
):

    jira : JiraConsultor = JiraConsultor(profile)
    
    jira.login()
    jira.requestIssues()

    data = jira.findFields(jira.domainAtributes["fields"])
    headers = ["key"] + [x.split("/")[-1] for x in jira.domainAtributes["fields"]]
    expMan = ExportManager()
    expMan.exportToExcel(headers,data)

    return {"status": "done", "output":"/output"}