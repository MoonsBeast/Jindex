import lib.util as util

from atlassian import Jira
import re
import pprint

config = util.retrieveFromYAML("config/config.yml")

class JiraConsultor:

    def __init__(self, pathToConfig: str, domain: str) -> None:

        self.setConfigAndDomain(pathToConfig,domain)

    def setConfigAndDomain(self, pathToConfig: str, domain: str):

        self.setConfigFile(pathToConfig)
        self.setDomain(domain)

    def setConfigFile(self, pathToConfig: str):

        self.config : dict = config["jiraDomains"]

    def setDomain(self, domain: str):

        self.domain : str = domain
        self.domainAtributes : str = self.config[self.domain]

    def login(self) -> Jira:

        self.__jiraConnection = Jira(url = self.domainAtributes["url"], username = self.domainAtributes["user"], password = self.domainAtributes["password"], cloud=True)

    def requestIssues(self) -> dict:

        self.query = self.__jiraConnection.jql(self.domainAtributes["query"])["issues"]

        return self.query
    
    def findFields(self, fields: list) -> list:
        
        result = {}
        for issue in self.query:
            for field in fields:
                
                if issue["key"] not in result.keys():
                    result[issue["key"]] = []

                result[issue["key"]].append(self.__filterByPath(field, issue))

        return result
        
    
    def __filterByPath(self, path: str, subset):
    
        result = None
        data = subset
        
        split = path.split('/')
        step = split[0]
        filterLeft = "/".join(split[1:])

        if step == "*":

            if type(data) == dict:
                data = data.values()

            result = []
            for val in data:

                if len(split) > 1:
                    result.append(self.__filterByPath(filterLeft, val))

                else:
                    return data

        else:

            if re.search("^[-+]?[0-9]+$", step):
                step = int(step)
                
            data = data[step]
            if len(split) > 1:
                result = self.__filterByPath(filterLeft, data)

            else:
                return data
            
        return result