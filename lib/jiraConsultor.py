import lib.util as util

from atlassian import Jira
import re

class JiraConsultor:

    def __init__(self, pathToConfig: str, domain: str) -> None:

        self.setConfigAndDomain(pathToConfig,domain)

    def setConfigAndDomain(self, pathToConfig: str, domain: str):

        self.setConfigFile(pathToConfig)
        self.setDomain(domain)

    def setConfigFile(self, pathToConfig: str):

        self.config : dict = util.retrieveFromYAML(pathToConfig)["jiraDomains"]

    def setDomain(self, domain: str):

        self.domain : str = domain
        self.domainAtributes : str = self.config[self.domain]

    def login(self) -> Jira:

        self.__jiraConnection = Jira(url = self.domainAtributes["url"], username = self.domainAtributes["user"], password = self.domainAtributes["password"], cloud=True)

    def requestIssues(self) -> dict:

        self.query = self.__jiraConnection.jql(self.domainAtributes["query"])["issues"]

        return self.query
    
    def filterFields(self, filter: str, subset = None) -> list:
        
        result = None
        data = self.query if subset == None else subset

        split = filter.split('/')
        step = split[0]
        filterLeft = "/".join(split[1:])

        if step == "*":

            if type(data) == dict:
                data = data.values()

            result = []
            for val in data:

                if len(split) > 1:
                    result.append(self.filterFields(filterLeft, val))

                else:
                    return data

        else:

            if re.search("^[-+]?[0-9]+$", step):
                step = int(step)

            data = data[step]
            if len(split) > 1:
                result = self.filterFields(filterLeft, data)

            else:
                return data
            
        return result