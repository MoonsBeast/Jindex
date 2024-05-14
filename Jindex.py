import click
import pprint

from lib.jiraConsultor import JiraConsultor
from lib.exportManager import ExportManager

@click.group()
@click.option("-p", "--profile",default="default", type=str)
@click.pass_context
def jindex(ctx,profile):
    jira = JiraConsultor(profile)
    
    jira.login()
    jira.requestIssues()

    ctx.ensure_object(dict)
    ctx.obj["jira"] = jira

@jindex.command()
@click.pass_context 
def test(ctx):

    jira : JiraConsultor = ctx.obj["jira"]

    pprint.pp(jira.query[0])

@jindex.command()
@click.pass_context
def print(ctx):

    jira : JiraConsultor = ctx.obj["jira"]

    headers = ["key"] + [x.split("/")[-1] for x in jira.domainAtributes["fields"]]
    pprint.pp(headers)
    pprint.pp(jira.findFields(jira.domainAtributes["fields"]))

@jindex.command()
@click.pass_context
def excel(ctx):

    jira : JiraConsultor = ctx.obj["jira"]

    data = jira.findFields(jira.domainAtributes["fields"])
    headers = ["key"] + [x.split("/")[-1] for x in jira.domainAtributes["fields"]]
    expMan = ExportManager()
    expMan.exportToExcel(headers,data)

if __name__ == '__main__':
    jindex(obj={})