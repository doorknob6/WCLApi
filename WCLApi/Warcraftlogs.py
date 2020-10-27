"""Module containing the base Api class."""
from urllib3.util.retry import Retry
from requests_toolbelt import sessions
from WCLApi.TimeoutHttpAdapter import TimeoutHttpAdapter
import inspect
import json
import os
import sys

class WCLApi():
    """This class provides the base class for API calls."""

    def __init__(self, api_key,
                 base_url=r'https://classic.warcraftlogs.com:443/v1/',
                 timeout=1):
        """
        Initialize the WCLApi class and optionally attach an authentication token.

        Args:
            api_key (str): Authentication api_key.
            base_url (str, optional): Base URL for calls to the API.
                Defaults to r'https://classic.warcraftlogs.com:443/v1/'
            timeout (float, optional): Default timeout for API calls. Defaults to 1.

        Returns:
            None.

        """
        assert api_key is not None, "Please enter an api_key"
        self.api_key = api_key
        self.http = sessions.BaseUrlSession(base_url)
        self.http.hooks['response'] = [lambda response, *args, **kwargs: response.raise_for_status()]
        retries = Retry(total=6, backoff_factor=1, status_forcelist=[429, 500, 502, 503, 504])
        adapter = TimeoutHttpAdapter(timeout=timeout, max_retries=retries)
        self.http.mount("https://", adapter)
        self.http.mount("http://", adapter)

    def get_guild_reports(self, server, server_region, guild_name, endpoint=r'reports/guild/:guildName/:serverName/:serverRegion'):
        """
        Send a GET /reports/guild request to the API, returns the guild reports.

        Args:
            server (str): server name for the which the guild reports are to be found.
            server_region (str): server region for the which the reports are to be found.
            guild_name (str): guild for which the reports are to be found.
            endpoint (str, optional): endpoint for the request. Defaults to r'reports/guild/:guildName/:serverName/:serverRegion'.

        Raises:
            ConnectionError: Different Connectionerrors based on retrieved ApiErrors.

        Returns:
            dict(JsonApiObject): JsonApi object in the form of a dict.

        """
        try:
            api_key = self.api_key
        except AttributeError:
            raise ValueError("Please initialise the Api class.")

        headers = {}

        endpoint = endpoint.replace(":serverName", server.lower().replace(' ', '-')
                                    ).replace(":serverRegion", server_region
                                              ).replace(":guildName", guild_name)

        params = {}

        params.update({'api_key' : self.api_key})

        resp = self.http.get(endpoint, headers=headers, params=params)

        if resp.status_code == 200:
            cont = resp.json()
            return cont

        if resp.status_code == 401:
            raise ConnectionError("Renew authorization token.")

        raise ConnectionError("Request failed with code {}".format(resp.status_code) +
                              " and message : {}".format(resp.content) +
                              " for endpoint: {}".format(endpoint))

    def get_report_fights(self, report_code, endpoint=r'report/fights/:report_code'):
        """
        Send a GET /report/fights request to the API, returns the report fights.

        Args:
            report_code (str): report code for the which the fights are to be found.
            endpoint (str, optional): endpoint for the request. Defaults to r'report/fights/:report_code'.

        Raises:
            ConnectionError: Different Connectionerrors based on retrieved ApiErrors.

        Returns:
            dict(JsonApiObject): JsonApi object in the form of a dict.
        """
        try:
            api_key = self.api_key
        except AttributeError:
            raise ValueError("Please initialise the Api class.")

        headers = {}

        endpoint = endpoint.replace(":report_code", report_code)

        params = {}

        params.update({'api_key' : self.api_key})

        resp = self.http.get(endpoint, headers=headers, params=params)

        if resp.status_code == 200:
            cont = resp.json()
            return cont

        if resp.status_code == 401:
            raise ConnectionError("Renew authorization token.")

        raise ConnectionError("Request failed with code {}".format(resp.status_code) +
                              " and message : {}".format(resp.content) +
                              " for endpoint: {}".format(endpoint))

    def get_report_events(self, view, report_code,
                          start_time=None,
                          end_time=None,
                          hostility=None,
                          sourceid=None,
                          sourceinstance=None,
                          sourceclass=None,
                          targetid=None,
                          targetinstance=None,
                          targetclass=None,
                          abilityid=None,
                          death=None,
                          options=None,
                          cutoff=None,
                          encounter=None,
                          wipes=None,
                          filter_exp=None,
                          translate=None,
                          endpoint='report/events/:view/:report_code'):
        """
        Send a GET /report/events request to the API, returns the report events.

        Args:
            view (str): view for the which the events are to be found.
            report_code (str): report code for the which the events are to be found.
            start_time (int, optional): A start time. This is a time from the start of the report in milliseconds. If omitted, 0 is assumed. Defaults to None.
            end_time (int, optional): An end time. This is a time from the start of the report in milliseconds. If omitted, 0 is assumed. Defaults to None.
            hostility (int, optional): An optional hostility value of 0 or 1. The default is 0. A value of 0 means to collect data for Friendlies. A value of 1 means to collect data for Enemies. Defaults to None.
            sourceid (int, optional): An optional actor ID to filter to. If set, only events where the ID matches the source (or target for damage-taken) of the event will be returned. The actor's pets will also be included (unless the options field overrides). Defaults to None.
            sourceinstance (int, optional): An optional actor instance ID to filter to. If set, only events where the instance ID matches the source (or target for damage-taken) of the event will be returned. This is useful to look for all events involving NPC N, where N is the actor instance ID. Defaults to None.
            sourceclass (str, optional): An optional actor class to filter to. If set, only events where the source (or target for damage-taken) involves that class (e.g., Mage) will be returned. Defaults to None.
            targetid (int, optional): An optional actor ID to filter to. If set, only events where the ID matches the target (or source for damage-taken) of the event will be returned. This value is not used in the 'deaths', 'survivability', 'resources' and 'resources-gains' views. Defaults to None.
            targetinstance (int, optional): An optional actor instance ID to filter to. If set, only events where the instance ID matches the target (or source for damage-taken) of the event will be returned. This is useful to look for all events involving NPC N, where N is the actor instance ID. This value is not used in the 'deaths', 'survivability', 'resources' and 'resources-gains' views. Defaults to None.
            targetclass (str, optional): An optional actor class to filter to. If set, only events where the target (or source for damage-taken) involves that class (e.g., Mage) will be returned. This value is not used in the 'deaths', 'survivability', 'resources' and 'resources-gains' views. Defaults to None.
            abilityid (int, optional): An optional ability ID to filter to. If set, only events where the ability matches will be returned. Consolidated abilities (WCL only) are represented using a negative number that matches the ability ID that everything is consolidated under. For the 'deaths' view, this represents a specific killing blow. For the resources views, the abilityid is not an ability but a resource type. Valid resource types can be viewed at https://www.warcraftlogs.com/reports/resource_types/ Defaults to None.
            death (int, optional): An optional death to filter to. Only used for the deaths command. Select the Nth death in the time range that matches all the other filters. Defaults to None.
            options (int, optional): A set of options for what to include/exclude. These correspond to options like Include Overkill in the Damage Done pane. Complete list will be forthcoming. If omitted, appropriate defaults that match WCL's default behavior will be chosen. This value is not used in the 'deaths', 'survivability', 'resources' and 'resources-gains' views. Defaults to None.
            cutoff (int, optional): An optional death cutoff. If set, events after that number of deaths have occurred will not be examined. Defaults to None.
            encounter (int, optional): An optional encounter filter. If set to a specific encounter ID, only fights involving a specific encounter will be considered. The encounter IDs match those used in rankings/statistics. Defaults to None.
            wipes (int, optional): An optional wipes filter. If set to 1, only wipes will be considered. Defaults to None.
            filter_exp (str, optional): An optional filter written in WCL's expression language. Events must match the filter to be included. Defaults to None.
            translate (bool, optional): An optional flag indicating that the results should be translated into the language of the host (e.g., cn.warcraftlogs.com would get Chinese results). Defaults to None.onal): An optional flag indicating that the results should be translated into the language of the host (e.g., cn.warcraftlogs.com would get Chinese results). Defaults to None.tional flag indicating that the results should be translated into the language of the host (e.g., cn.warcraftlogs.com would get Chinese results). Defaults to None.
            endpoint (str, optional): endpoint for the request. Defaults to r'report/events/:view/:report_code'.

        Raises:
            ConnectionError: Different Connectionerrors based on retrieved ApiErrors.

        Returns:
            dict(JsonApiObject): JsonApi object in the form of a dict.

        """
        try:
            api_key = self.api_key
        except AttributeError:
            raise ValueError("Please initialise the Api class.")

        argspec = inspect.getargvalues(inspect.currentframe())
        cont = self.load_saved_query('events', argspec)

        if cont is not None:
            return cont

        headers = {}

        endpoint = endpoint.replace(':view', view).replace(":report_code", report_code)

        params = {}

        if start_time is not None: params.update({'start' : start_time})
        if end_time is not None: params.update({'end' : end_time})
        if hostility is not None: params.update({'hostility' : hostility})
        if sourceid is not None: params.update({'sourceid' : sourceid})
        if sourceinstance is not None: params.update({'sourceinstance' : sourceinstance})
        if sourceclass is not None: params.update({'sourceclass' : sourceclass})
        if targetid is not None: params.update({'targetid' : targetid})
        if targetinstance is not None: params.update({'targetinstance' : targetinstance})
        if targetclass is not None: params.update({'targetclass' : targetclass})
        if abilityid is not None: params.update({'abilityid' : abilityid})
        if death is not None: params.update({'death' : death})
        if options is not None: params.update({'options' : options})
        if cutoff is not None: params.update({'cutoff' : cutoff})
        if encounter is not None: params.update({'encounter' : encounter})
        if wipes is not None: params.update({'wipes' : wipes})
        if filter_exp is not None: params.update({'filter' : filter_exp})
        if translate is not None: params.update({'translate' : translate})

        params.update({'api_key' : self.api_key})

        next_timestamp = -1
        resp = ''

        while next_timestamp != 0:

            if next_timestamp > 0:
                params.update({'start' : next_timestamp})

            resp = self.http.get(endpoint, headers=headers, params=params)

            if resp.status_code == 200:
                resp_json = resp.json()
                if cont is not None:
                    cont['events'] += resp_json['events']
                else:
                    cont = resp.json()

                try:
                    next_timestamp = resp_json['nextPageTimestamp']
                except KeyError:
                    next_timestamp = 0
            else:
                break
        
        if resp:
            if resp.status_code == 200:
                self.save_query('events', argspec, cont)
                return cont

            if resp.status_code == 401:
                raise ConnectionError("Renew authorization token.")

        raise ConnectionError("Request failed with code {}".format(resp.status_code) +
                              " and message : {}".format(resp.content) +
                              " for endpoint: {}".format(endpoint))

    def get_report_tables(self, view, report_code,
                          start_time=None,
                          end_time=None,
                          hostility=None,
                          by=None,
                          sourceid=None,
                          sourceinstance=None,
                          sourceclass=None,
                          targetid=None,
                          targetinstance=None,
                          targetclass=None,
                          abilityid=None,
                          options=None,
                          cutoff=None,
                          encounter=None,
                          wipes=None,
                          filter_exp=None,
                          translate=None,
                          endpoint='report/tables/:view/:report_code'):
        """
        Send a GET /report/tables request to the API, returns the report tables.

        Args:
            view (str): view for the which the tables are to be found.
            report_code (str): report code for the which the tables are to be found.
            start_time (int, optional): A start time. This is a time from the start of the report in milliseconds. If omitted, 0 is assumed. Defaults to None.
            end_time (int, optional): An end time. This is a time from the start of the report in milliseconds. If omitted, 0 is assumed. Defaults to None.
            hostility (int, optional): An optional hostility value of 0 or 1. The default is 0. A value of 0 means to collect data for Friendlies. A value of 1 means to collect data for Enemies. Defaults to None.
            by (str, optional): An optional parameter indicating how to group entries. They can be grouped by 'source', by 'target', or by 'ability'. This value matches WCL's default behavior if omitted. For buffs and debuffs, a value of 'source' means auras gained by the source, and a value of 'target' means auras cast by the source. This value is not used in the 'deaths', 'survivability', 'resources' and 'resources-gains' views. Defaults to None.
            sourceid (int, optional): An optional actor ID to filter to. If set, only events where the ID matches the source (or target for damage-taken) of the event will be returned. The actor's pets will also be included (unless the options field overrides). Defaults to None.
            sourceinstance (int, optional): An optional actor instance ID to filter to. If set, only events where the instance ID matches the source (or target for damage-taken) of the event will be returned. This is useful to look for all events involving NPC N, where N is the actor instance ID. Defaults to None.
            sourceclass (str, optional): An optional actor class to filter to. If set, only events where the source (or target for damage-taken) involves that class (e.g., Mage) will be returned. Defaults to None.
            targetid (int, optional): An optional actor ID to filter to. If set, only events where the ID matches the target (or source for damage-taken) of the event will be returned. This value is not used in the 'deaths', 'survivability', 'resources' and 'resources-gains' views. Defaults to None.
            targetinstance (int, optional): An optional actor instance ID to filter to. If set, only events where the instance ID matches the target (or source for damage-taken) of the event will be returned. This is useful to look for all events involving NPC N, where N is the actor instance ID. This value is not used in the 'deaths', 'survivability', 'resources' and 'resources-gains' views. Defaults to None.
            targetclass (str, optional): An optional actor class to filter to. If set, only events where the target (or source for damage-taken) involves that class (e.g., Mage) will be returned. This value is not used in the 'deaths', 'survivability', 'resources' and 'resources-gains' views. Defaults to None.
            abilityid (int, optional): An optional ability ID to filter to. If set, only events where the ability matches will be returned. Consolidated abilities (WCL only) are represented using a negative number that matches the ability ID that everything is consolidated under. For the 'deaths' view, this represents a specific killing blow. For the resources views, the abilityid is not an ability but a resource type. Valid resource types can be viewed at https://www.warcraftlogs.com/reports/resource_types/ Defaults to None.
            options (int, optional): A set of options for what to include/exclude. These correspond to options like Include Overkill in the Damage Done pane. Complete list will be forthcoming. If omitted, appropriate defaults that match WCL's default behavior will be chosen. This value is not used in the 'deaths', 'survivability', 'resources' and 'resources-gains' views. Defaults to None.
            cutoff (int, optional): An optional death cutoff. If set, events after that number of deaths have occurred will not be examined. Defaults to None.
            encounter (int, optional): An optional encounter filter. If set to a specific encounter ID, only fights involving a specific encounter will be considered. The encounter IDs match those used in rankings/statistics. Defaults to None.
            wipes (int, optional): An optional wipes filter. If set to 1, only wipes will be considered. Defaults to None.
            filter_exp (str, optional): An optional filter written in WCL's expression language. Events must match the filter to be included. Defaults to None.
            translate (bool, optional): An optional flag indicating that the results should be translated into the language of the host (e.g., cn.warcraftlogs.com would get Chinese results). Defaults to None.onal): An optional flag indicating that the results should be translated into the language of the host (e.g., cn.warcraftlogs.com would get Chinese results). Defaults to None.tional flag indicating that the results should be translated into the language of the host (e.g., cn.warcraftlogs.com would get Chinese results). Defaults to None.
            endpoint (str, optional): endpoint for the request. Defaults to r'report/tables/:view/:report_code'.

        Raises:
            ConnectionError: Different Connectionerrors based on retrieved ApiErrors.

        Returns:
            dict(JsonApiObject): JsonApi object in the form of a dict.

        """
        try:
            api_key = self.api_key
        except AttributeError:
            raise ValueError("Please initialise the Api class.")

        headers = {}

        endpoint = endpoint.replace(':view', view).replace(":report_code", report_code)

        params = {}

        if start_time is not None: params.update({'start_time' : start_time})
        if end_time is not None: params.update({'end_time' : end_time})
        if hostility is not None: params.update({'hostility' : hostility})
        if by is not None: params.update({'by' : by})
        if sourceid is not None: params.update({'sourceid' : sourceid})
        if sourceinstance is not None: params.update({'sourceinstance' : sourceinstance})
        if sourceclass is not None: params.update({'sourceclass' : sourceclass})
        if targetid is not None: params.update({'targetid' : targetid})
        if targetinstance is not None: params.update({'targetinstance' : targetinstance})
        if targetclass is not None: params.update({'targetclass' : targetclass})
        if abilityid is not None: params.update({'abilityid' : abilityid})
        if options is not None: params.update({'options' : options})
        if cutoff is not None: params.update({'cutoff' : cutoff})
        if encounter is not None: params.update({'encounter' : encounter})
        if wipes is not None: params.update({'wipes' : wipes})
        if filter_exp is not None: params.update({'filter' : filter_exp})
        if translate is not None: params.update({'translate' : translate})

        params.update({'api_key' : self.api_key})

        resp = self.http.get(endpoint, headers=headers, params=params)

        if resp.status_code == 200:
            cont = resp.json()
            return cont

        if resp.status_code == 401:
            raise ConnectionError("Renew authorization token.")

        raise ConnectionError("Request failed with code {}".format(resp.status_code) +
                              " and message : {}".format(resp.content) +
                              " for endpoint: {}".format(endpoint))

    def load_saved_query(self, query, argspec):
        cont = None
        f_name = self.make_file_name(argspec, query)
        f_folder = os.path.join(sys.path[0], 'saved_queries')
        if os.path.isdir(f_folder):
            f_path = os.path.join(f_folder, f_name)
            if os.path.isfile(f_path):
                with open(f_path, 'r') as f:
                    cont = json.load(f)
        return cont

    def save_query(self, query, argspec, cont):
        f_name = self.make_file_name(argspec, query)
        f_folder = os.path.join(sys.path[0], 'saved_queries')
        if not os.path.isdir(f_folder):
            os.mkdir(f_folder)
        f_path = os.path.join(f_folder, f_name)
        with open(f_path, 'w') as f:
            json.dump(cont, f)

    def make_file_name(self, argspec, query):
        arg_str = '_'.join([argspec.locals['report_code']] +
                           [str(argspec.locals[arg])
                            for arg in argspec.args if
                                argspec.locals[arg] is not None and
                                not isinstance(argspec.locals[arg], WCLApi) and
                                arg not in ['endpoint', 'report_code', 'view']] +
                           [argspec.locals['view']])
        return f"wcl_{query}_{arg_str}.json"
