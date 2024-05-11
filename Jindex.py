import click
import pprint

from lib.jiraConsultor import JiraConsultor

@click.group()
@click.option("-p", "--profile",default="default", type=str)
@click.pass_context
def jindex(ctx,profile):
    jira = JiraConsultor("./config/options.yml",profile)

    jira.login()
    jira.requestIssues()

    ctx.ensure_object(dict)
    ctx.obj["jira"] = jira

@jindex.command()
@click.pass_context 
def test(ctx):

    jira : JiraConsultor = ctx.obj["jira"]

    pprint.pp(jira.requestIssues()[0])

@jindex.command()
@click.pass_context
def print(ctx):

    jira : JiraConsultor = ctx.obj["jira"]

    for path in jira.domainAtributes["fields"]:
        pprint.pp(jira.filterFields(path))

if __name__ == '__main__':
    jindex(obj={})