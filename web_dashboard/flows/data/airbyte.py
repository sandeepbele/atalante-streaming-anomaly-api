from __future__ import annotations

from enum import Enum

from base import DataflowEngine
import requests
import json
from copy import copy
from abc import abstractmethod
from typing import List, Dict, Any, Optional, Union, TypeVar, Tuple, NewType


class ConnectorDefinition:
    pass

class AirbyteConnectorDefinition(ConnectorDefinition):

    descriptions = {
        "Commcare": "A mobile-first platform for digital health workers",
        "Trello": "A project management tool that helps teams organize and track their work",
        "The Guardian API": "An API that provides access to content from The Guardian",
        "Harvest": "A time tracking tool that helps teams track their time and bill their clients",
        "Public APIs": "A directory of public APIs that can be used for a variety of purposes",
        "Coda": "A collaborative workspace that helps teams create and share documents, spreadsheets, and presentations",
        "PrestaShop": "An open-source e-commerce platform",
        "Netsuite": "A cloud-based ERP system",
        "Convex": "A no-code platform that helps businesses build and automate workflows",
        "Recurly": "A subscription billing platform",
        "Appstore": "A digital distribution platform for iOS and macOS apps",
        "Pendo": "A product analytics platform that helps teams understand how users are using their products",
        "Commercetools": "A headless commerce platform",
        "E2E Testing": "A type of software testing that tests the end-to-end functionality of a system",
        "Kyriba": "A treasury management system",
        "Zendesk Chat": "A customer support chat platform",
        "My Hours": "A time tracking tool for freelancers and contractors",
        "Zendesk Sell": "A customer relationship management (CRM) platform",
        "Dremio": "A data lake engine that helps businesses manage and analyze their data",
        "Jenkins": "A continuous integration and continuous delivery (CI/CD) server",
        "Klaviyo": "An email marketing platform",
        "Datadog": "A monitoring platform that helps businesses track and troubleshoot their IT infrastructure",
        "ActiveCampaign": "An email marketing platform",
        "Chargify": "A subscription billing platform",
        "Dockerhub": "A registry for Docker images",
        "Webflow": "A web development platform that helps businesses create and manage their websites",
        "SurveyCTO": "A survey platform that helps businesses collect and analyze data",
        "Newsdata": "A news API that provides access to news articles from a variety of sources",
        "Flexport": "A freight forwarding company",
        "Wikipedia Pageviews": "An API that provides access to data on Wikipedia pageviews",
        "Freshservice": "A help desk software",
        "Railz": "A Rails development tool",
        "Google Directory": "A directory of Google products and services",
        "SmartEngage": "A customer engagement platform",
        "K6 Cloud": "A load testing platform",
        "Postgres": "A relational database management system",
        "Todoist": "A to-do list app",
        "Fauna": "A NoSQL database",
        "Twilio": "A cloud communications platform",
        "Sendgrid": "An email delivery platform",
        "GNews": "A news aggregator from Google",
        "Workable": "A recruiting software",
        "Google Ads": "An online advertising platform from Google",
        "Google Search Console": "A webmaster tool that helps businesses track and improve their website's search engine ranking",
        "CallRail": "A call tracking platform",
        "Strava": "An activity tracking app",
        "Smaily": "An email marketing platform",
        "Kustomer": "A customer relationship management (CRM) platform",
        "Polygon Stock API": "An API that provides access to stock data",
        "Shopify": "An e-commerce platform",
        "Omnisend": "An email marketing platform",
        "MongoDb": "A NoSQL database",
        "Retently": "A customer retention platform",
        "TalkDesk Explore": "A customer service platform",
        "Instagram": "A social media platform",
        "S3": "A cloud storage service from Amazon Web Services",
        "Azure Blob Storage": "A cloud storage service from Microsoft Azure",
        "Close.com": "A sales CRM platform",
        "LinkedIn Pages": "A platform for businesses to create and manage their LinkedIn pages",
        "Zendesk Sunshine": "A customer data platform",
        "Gong": "A sales intelligence platform",
        "Exchange Rates Api": "An API that provides access to exchange rates",
        "WooCommerce": "An e-commerce plugin for WordPress",
        "News API": "An API that provides access to news articles from a variety of sources",
        "Younium": "A social media platform for businesses",
        "MySQL": "A relational database management system",
        "OpenWeather": "An API that provides access to weather data",
        "Whisky Hunter": "A whisky database",
        "TVMaze Schedule": "An API that provides access to TV show schedules",
        "SalesLoft": "A sales CRM platform",
        "Short.io": "A link shortener",
        "Instatus": "A status page platform",
        "EmailOctopus": "An email marketing platform",
        "Tyntec SMS": "An SMS marketing platform",
        "Yandex Metrica": "A web analytics platform",
        "Rocket.chat": "A chat platform",
        "ClickUp": "A project management tool",
        "TMDb": "A movie database",
        "Drift": "A customer chat platform",
        "Toggl": "A time tracking tool",
        "Snapchat Marketing": "A platform for businesses to advertise on Snapchat",
        "Gitlab": "A code hosting platform",
        "SearchMetrics": "A website analytics platform",
        "LaunchDarkly": "A feature flagging platform",
        "Snowflake": "A cloud data warehouse",
        "Auth0": "An identity and access management (IAM) platform",
        "Linnworks": "A cloud-based ERP system",
        "Amazon SQS": "A message queue service from Amazon Web Services",
        "Sonar Cloud": "A code quality platform",
        "Clockify": "A time tracking tool",
        "Marketo": "An inbound marketing platform",
        "Pocket": "A bookmarking app",
        "Customer.io": "A customer engagement platform",
        "Everhour": "A time tracking tool",
        "Smartsheets": "A project management tool",
        "n8n": "A no-code automation platform",
        "NASA": "A space agency",
        "WorkRamp": "A onboarding platform",
        "Iterable": "A customer engagement platform",
        "Orbit": "A customer data platform",
        "TPLcentral": "A directory of open source software",
        "Apify Dataset": "A platform for building and managing data pipelines",
        "Confluence": "A wiki platform",
        "Coin API": "An API that provides access to cryptocurrency data",
        "Orb": "A customer data platform",
        "Sentry": "An error tracking platform",
        "Mailjet Mail": "An email marketing platform",
        "Notion": "A note-taking and productivity app",
        "TrustPilot": "A customer review platform",
        "Hellobaton": "A customer feedback platform",
        "Google Webfonts": "A library of web fonts",
        "PyPI": "A repository of Python packages",
        "Slack": "A chat platform",
        "File (CSV, JSON, Excel, Feather, Parquet)": "A file format",
        "Lokalise": "A localization platform",
        "Opsgenie": "An incident management platform",
        "ZohoCRM": "A customer relationship management (CRM) platform",
        "Stripe": "A payment processing platform",
        "Zapier Supported Storage": "A list of storage services that Zapier supports",
        "Plaid": "A financial data platform",
        "YouTube Analytics": "A platform for businesses to track their YouTube videos",
        "Google Sheets": "A spreadsheet application",
        "Zendesk Talk": "A customer support chat platform",
        "Gridly": "A project management tool",
        "Freshdesk": "A customer support platform",
        "Vitally": "A website monitoring platform",
        "Google Analytics (Universal Analytics)": "A web analytics platform",
        "Asana": "A project management tool",
        "PostHog": "A website analytics platform",
        "Plausible": "A website analytics platform",
        "GetLago": "A project management tool",
        "Microsoft teams": "A collaboration platform",
        "Oura": "A sleep tracking ring",
        "Looker": "A business intelligence platform",
        "Amazon Seller Partner": "A program for Amazon sellers",
        "BigCommerce": "An e-commerce platform",
        "Zenefits": "A human resources platform",
        "IP2Whois": "A service that provides IP address information",
        "Harness": "A cloud management platform",
        "Copper": "A sales CRM platform",
        "Recreation": "A platform for businesses to offer employee benefits",
        "PagerDuty": "An incident management platform",
        "LinkedIn Ads": "A platform for businesses to advertise on LinkedIn",
        "US Census": "A government agency that collects data about the United States population",
        "Kafka": "A distributed streaming platform",
        "Pinterest": "A social media platform for sharing images",
        "SpaceX API": "An API that provides access to data from SpaceX",
        "BambooHR": "A human resources platform",
        "MailerSend": "An email marketing platform",
        "Okta": "An identity and access management (IAM) platform",
        "Mixpanel": "A website analytics platform",
        "RD Station Marketing": "A marketing automation platform",
        "Twitter": "A social media platform",
        "Weatherstack": "An API that provides access to weather data",
        "Zendesk Support": "A customer support platform",
        "SFTP Bulk": "A service that allows businesses to upload files to SFTP servers",
        "Genesys": "A customer service platform",
        "Aha": "A product development platform",
        "Punk API": "An API that provides access to punk music data",
        "Xero": "An accounting software",
        "TikTok Marketing": "A platform for businesses to advertise on TikTok",
        "AWS CloudTrail": "A service that provides logs of AWS API calls",
        "Jira": "A project management tool",
        "Elasticsearch": "A search engine",
        "HubSpot": "A marketing and sales platform",
        "RSS": "A format for syndicating content",
        "SAP Fieldglass": "A workforce management platform",
        "Twilio Taskrouter": "A platform for businesses to build and manage call centers",
        "xkcd": "A webcomic",
        "Zenloop": "A customer experience platform",
        "Ashby": "A project management tool",
        "Tempo": "A time tracking tool",
        "Chargebee": "A subscription billing platform",
        "Wrike": "A project management tool",
        "OneSignal": "A push notification platform",
        "Google Analytics 4 (GA4)": "A web analytics platform",
        "Timely": "A time tracking tool",
        "Mailgun": "An email delivery platform",
        "ConvertKit": "An email marketing platform",
        "Intercom": "A customer engagement platform",
        "RKI Covid": "A website that provides information about the COVID-19 pandemic in Germany",
        "Secoda": "A website security platform",
        "Zoom": "A video conferencing platform",
        "Delighted": "A customer feedback platform",
        "Klarna": "A payment platform",
        "Typeform": "A form builder",
        "Paypal Transaction": "An API that provides access to PayPal transaction data",
        "Lemlist": "A cold email platform",
        "Pexels API": "An API that provides access to photos from Pexels",
        "Firebase Realtime Database": "A database that provides real-time data synchronization",
        "Glassfrog": "A customer feedback platform",
        "Facebook Marketing": "A platform for businesses to advertise on Facebook",
        "Facebook Pages": "A platform for businesses to create and manage their Facebook pages",
        "Recruitee": "A recruiting software",
        "Cockroachdb": "A distributed SQL database",
        "SurveySparrow": "A survey platform",
        "Azure Table Storage": "A cloud storage service from Microsoft Azure",
        "DV 360": "A customer data platform",
        "SurveyMonkey": "A survey platform",
        "PersistIq": "A customer data platform",
        "PartnerStack": "A customer data platform",
        "ConfigCat": "A configuration management platform",
        "Insightly": "A CRM platform",
        "Qonto": "A business banking platform",
        "Cart.com": "An e-commerce platform",
        "Oracle DB": "A relational database management system",
        "Appfollow": "A mobile app analytics platform",
        "Chartmogul": "A subscription billing platform",
        "CoinMarketCap": "A website that tracks cryptocurrency prices",
        "Dixa": "A customer support",
        "Freshcaller": "A cloud-based call center platform",
        "Recharge": "A subscription billing platform",
        "TiDB": "A distributed SQL database",
        "Datascope": "A data visualization platform",
        "Reply.io": "A customer support platform",
        "Zuora": "A subscription billing platform",
        "Metabase": "A business intelligence platform",
        "Bing Ads": "A platform for businesses to advertise on Bing",
        "VictorOps": "An incident management platform",
        "Monday": "A project management tool",
        "Amplitude": "A website analytics platform",
        "Google PageSpeed Insights": "A tool that helps businesses improve their website's loading speed",
        "Waiteraid": "A customer feedback platform",
        "Adjust": "A mobile app analytics platform",
        "Pipedrive": "A CRM platform",
        "Amazon Ads": "A platform for businesses to advertise on Amazon",
        "GoCardless": "A payment platform",
        "Intruder": "A website security platform",
        "Sendinblue": "An email marketing platform",
        "GitHub": "A code hosting platform",
        "Microsoft Dataverse": "A customer data platform",
        "Fastbill": "An accounting software",
        "Visma E-conomic": "An accounting software",
        "Alpha Vantage": "A financial data platform",
        "BigQuery": "A cloud data warehouse",
        "Gutendex": "A customer data platform",
        "Vantage": "A customer data platform",
        "Firebolt": "A cloud data warehouse",
        "Courier": "A customer data platform",
        "Google Workspace Admin Reports": "A tool that helps businesses track the usage of their Google Workspace products",
        "Outreach": "A sales engagement platform",
        "Primetric": "A website analytics platform",
        "Pivotal Tracker": "A project management tool",
        "AlloyDB for PostgreSQL": "A cloud-based PostgreSQL database",
        "PokeAPI": "An API that provides access to Pokémon data",
        "MailerLite": "An email marketing platform",
        "Senseforce": "A customer data platform",
        "Freshsales": "A CRM platform",
        "Hubplanner": "A project management tool",
        "Qualaroo": "A survey platform",
        "Babelforce": "A customer support platform",
        "Square": "A payment platform",
        "Paystack": "A payment platform",
        "Redshift": "A cloud data warehouse",
        "IBM Db2": "A relational database management system",
        "CoinGecko Coins": "A website that tracks cryptocurrency prices",
        "AppsFlyer": "A mobile app analytics platform",
        "DynamoDB": "A NoSQL database",
        "Braintree": "A payment platform",
        "Mailchimp": "An email marketing platform",
        "Airtable": "A database that provides a spreadsheet-like interface",
        "Microsoft SQL Server (MSSQL)": "A relational database management system",
        "Breezometer": "A weather app",
        "QuickBooks": "An accounting software",
        "Salesforce": "A CRM platform",
        "ClickHouse": "A column-oriented database",
        "Postmark App": "An email delivery platform",
        "Sample Data (Faker)": "A tool that generates fake data",
        "Lever Hiring": "A recruiting software",
        "Unleash": "A feature flagging platform",
        "Open Exchange Rates": "A service that provides exchange rates",
        "Pardot": "A marketing automation platform",
        "Braze": "A customer engagement platform",
        "SFTP": "A file transfer protocol",
        "Mailjet SMS": "An SMS marketing platform",
        "GCS": "A cloud storage service from Google Cloud Platform",
        "Statuspage": "A website that provides status information for websites and services",
        "New York Times": "A news website",
        "Greenhouse": "A recruiting software"
    }

    enabled_connectors = []
    preferred_connectors = []
    # ideally we should check 'secret' properties in input_schema returned for each source
    # and keep list within connector definition instance but this will do for now
    secret_input_schema_properties = ['password']

    def __init__(self, kwargs):
        self.properties = kwargs

    @classmethod
    def get_secret_input_schema_properties(self):
        return self.secret_input_schema_properties

    @abstractmethod
    def id(self):
        pass
        
    @property
    def name(self):
        return self.properties.get('name')
    
    @property
    def icon(self):
        return self.properties.get('icon')

    @property
    def description(self):
        return self.descriptions.get(self.properties.get('name'))

    @property
    def isEnabled(self):
        return self.properties.get('name') in self.enabled_connectors()
    
    @property
    def type(self):
        return self.properties.get('dockerRepository').split('/')[1]
    

class AirbyteSourceDefinition(AirbyteConnectorDefinition):
    
    def __init__(self, kwargs):
        super().__init__(kwargs)

    @classmethod
    def enabled_connectors(self):
        return ["Postgres"]  

    @classmethod
    def preferred_connectors(self):
        return ["Postgres"]

    @property
    def id(self):
        return self.properties.get('sourceDefinitionId')


class AirbyteDestinationDefinition(AirbyteConnectorDefinition):

    @classmethod
    def enabled_connectors(self):
        return ["Kafka"]

    @classmethod
    def preferred_connectors(self):
        return ["Kafka"]

    @property
    def id(self):
        return self.properties.get('destinationDefinitionId')


class AirbyteConnectorInstance:

    @abstractmethod
    def id(self) -> str:
        pass

    @abstractmethod
    def definition_id(self) -> str:
        pass

    @property
    def workspace_id(self) -> str:
        return self.properties.get('workspaceId')

    @property
    def name(self)-> str:
        return self.properties.get('name')

    @property
    def connection_configuration(self) -> dict:
        return self.properties.get('connectionConfiguration')

    def has_same_config(self, other) -> bool:
        return isinstance(other,self.__class__) and \
                self.definition_id == other.definition_id and \
                self.workspace_id == other.workspace_id and \
                self.connection_configuration == other.connection_configuration


class AirbyteSourceInstance(AirbyteConnectorInstance):

    def __init__(self, instance:Dict, definition:AirbyteSourceDefinition):
        self.properties = instance

        # mask secrets
        for secret in AirbyteSourceDefinition.get_secret_input_schema_properties():
            if secret in self.properties['connectionConfiguration']:
                self.properties['connectionConfiguration'][secret] = '*'

        self.definition = definition

    @property
    def id(self):
        return self.properties.get('sourceId')

    @property
    def definition_id(self):
        return self.properties.get('sourceDefinitionId')


class AirbyteDestinationInstance(AirbyteConnectorInstance):

    def __init__(self, instance:Dict, definition:AirbyteDestinationDefinition):
        self.properties = instance
        self.definition = definition

    @property
    def id(self):
        return self.properties.get('destinationId')

    @property
    def definition_id(self):
        return self.properties.get('destinationDefinitionId')


class AirbyteSourceCatalog:

    def __init__(self,properties):
        self.properties = properties

    @property
    def id(self):
        return self.properties['catalogId']

    @property
    def streams(self)-> list[AirbyteSourceStream]:
        return [ AirbyteSourceStream(s) for s in self.properties['catalog']['streams']]

    def streams_with_incremental_sync(self) -> list:
        return [s for s in self.streams if "incremental" in s.supported_sync_modes]

    def get_stream_by_name(self, name:str) -> AirbyteSourceStream:
        """
        The next() function takes two arguments: the iterator and a default value to return if the iterator is exhausted.
        the next() function tries to retrieve the next item from the generator expression.
        If there is an item in the self.streams list that has a matching name, it will be returned. If no such item is found, the default value None will be returned instead."""
        return next((s for s in self.streams if s.name == name), None)


class AirbyteSourceStream:

    def __init__(self, properties):
        self.properties = properties['stream']
        self.config = properties['config']

    @property
    def name(self) -> str:
        return self.properties['name']

    @property
    def schema(self) -> dict:
        return self.properties['jsonSchema']['properties']

    @property
    def supported_sync_modes(self)-> List[str]:
        return self.properties["supportedSyncModes"]

    @property
    def namespace(self):
        return self.properties["namespace"]

    def get_fields(self) -> List[Tuple[str,str]]:
        schema = self.properties['jsonSchema']['properties']
        return [ (field,schema[field]["type"]) for field in schema.keys() ]

    def get_datetime_fields(self)-> List[str]:
        schema = self.properties['jsonSchema']['properties']
        return [ field for field in schema.keys() if schema[field].get("airbyte_type","") == "timestamp_with_timezone"]

    def with_cursor_field(self, cursor_field:str) -> AirbyteSourceStream:
        """Returns a copy of the stream with the cursor field set"""
        self.config['cursorField'] = cursor_field
        return copy(self)

    def with_sync_mode(self, sync_mode:SyncMode) -> AirbyteSourceStream:
        """Returns a copy of the stream with the sync mode set"""
        self.config['syncMode'] = sync_mode.value
        return copy(self)

    def with_destination_sync_mode(self, sync_mode:str) -> AirbyteSourceStream:
        """Returns a copy of the stream with the sync mode set"""
        self.config['destinationSyncMode'] = sync_mode
        return copy(self)

    def to_dict(self) -> dict:
        return {
            "stream": self.properties,
            "config": self.config
        }


class AirbyteAPIException(Exception):

    def __init__(self, request, status_code, content):
        super().__init__(content)
        self.request = request
        self.message = content.get("message", content)
        self.status_code = status_code

    def __str__ (self):
        return f"Airbyte API Exception: {self.request} - {self.status_code} - {self.message}"


class AirbyteNotFoundError(LookupError):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)


class AirbyteException(Exception):
    def __int__(self,error):
        super.__init__(error)
        self.error = error

    def __str__(self):
        return f"Airbyte backend error: {self.error}"


class AirbyteConnection():

    def __init__(self, properties:dict):
        self.properties = properties

    @property
    def id(self):
        return self.properties.get('connectionId')

    @property
    def name(self):
        return self.properties.get('name')

    @property
    def source_id(self) -> str:
        return self.properties.get('sourceId')

    @property
    def destination_id(self) -> str:
        return self.properties.get('destinationId')

    @property
    def stream(self) -> AirbyteSourceStream:
        return AirbyteSourceStream(self.properties.get('syncCatalog')['streams'][0])

    def is_active(self) -> str:
        return self.properties.get('status') == 'active'


class SyncMode(Enum):
    FULL_REFRESH = "full_refresh",
    INCREMENTAL = "incremental"


class Schedule:

    class TimeUnit(Enum):
        MINUTES = "minutes"
        HOURS = "hours"
        DAYS = "days"
        WEEKS = "weeks"
        MONTHS = "months"

    def __init__(self, interval: int = 60, time_unit: TimeUnit = TimeUnit.MINUTES):
        self.interval = interval
        self.time_unit = time_unit

    def to_dict(self):
        return {
            "scheduleType": "basic",
            "scheduleData": {
                "basicSchedule": {
                    "units": self.interval,
                    "timeUnit": self.time_unit.value
                }
            }
        }


class AirbyteEngine(DataflowEngine):
    
    def __init__(self, airbyte_base_url, client_id, client_secret, workspace_id, **kwargs):
        self.airbyte_base_url = airbyte_base_url
        self.client_id = client_id
        self.client_secret = client_secret
        self.workspace_id = workspace_id
        
        self.source_definitions: Dict[str,AirbyteSourceDefinition] = self._load_source_definitions()
        self.destination_definitions: Dict[str,AirbyteSourceDefinition] = self._load_destination_definitions()

    def _make_api_request(self, api_endpoint, payload):
        if payload is None or len(payload.keys()) == 0:
            headers = {}
        else:
            headers = {'Content-type': 'application/json'}
        resp = requests.post(self.airbyte_base_url + "/api" + api_endpoint, data=json.dumps(payload), headers=headers,
                             auth=(self.client_id, self.client_secret))
        if resp.status_code > 299:
            print(Exception(str(resp.status_code) + "_" + str(resp.content)))
        return resp

    def _load_source_definitions(self):
        resp = self._make_api_request("/v1/source_definitions/list_for_workspace",
                                   { "workspaceId": self.workspace_id})

        if resp.status_code < 299:
            source_def_map = { x['sourceDefinitionId']: AirbyteSourceDefinition(x) for x in resp.json()['sourceDefinitions']}
            return source_def_map
            #return [source_def_map[x] for x in AirbyteConnectorDefinition.preferred_connectors if x in source_def_map.keys()] + \
            #         [source_def_map[x] for x in source_def_map.keys() if x not in AirbyteConnectorDefinition.preferred_connectors ]
        else:
            raise AirbyteAPIException(resp.request, resp.status_code, resp.content)

    def _load_destination_definitions(self):
        resp = self._make_api_request("/v1/destination_definitions/list_for_workspace",
                                   { "workspaceId": self.workspace_id})

        if resp.status_code < 299:
            dest_def_map = { x['destinationDefinitionId']: AirbyteDestinationDefinition(x) for x in resp.json()['destinationDefinitions']}
            return dest_def_map
            #return [dest_def_map[x] for x in AirbyteConnectorDefinition.preferred_connectors if x in dest_def_map.keys()] + \
            #         [dest_def_map[x] for x in dest_def_map.keys() if x not in AirbyteConnectorDefinition.preferred_connectors ]
        else:
            raise AirbyteAPIException(resp.request, resp.status_code, resp.content)

    def get_source_def(self, src_def_id:str) -> AirbyteSourceDefinition:
        
        if src_def_id in self.source_definitions:
            return self.source_definitions[src_def_id]      
        else:
            raise AirbyteNotFoundError(f"Source definition not found: {src_def_id}")
    
    def get_source_input_schema(self, src_def: Union[str,AirbyteSourceDefinition]) -> Dict:

        if isinstance(src_def, str):
            src_def_id = src_def
        else:
            src_def_id = src_def.id

        resp = self._make_api_request("/v1/source_definition_specifications/get",
                                   {"workspaceId": self.workspace_id ,"sourceDefinitionId": src_def_id})
        if resp.status_code < 299:
            return resp.json()['connectionSpecification']
        else:
            raise AirbyteAPIException(resp.request, resp.status_code, resp.content)

    def test_source_connection(self, src_def: Union[str,AirbyteSourceDefinition], config:Dict) -> Tuple[bool,str]:
        """Test a source connection. Returns a tuple of (status, error)"""

        if isinstance(src_def, str):
            src_def_id = src_def
        else:
            src_def_id = src_def.id

        resp = self._make_api_request("/v1/scheduler/sources/check_connection",
                                   { "workspaceId": self.workspace_id,
                                     "sourceDefinitionId": src_def_id,
                                     "connectionConfiguration": config}
                                   )
        resp_json = resp.json()["jobInfo"]

        status = resp_json.get("succeeded", False)
        error = resp_json.get("failureReason", {}).get("externalMessage", None)

        return status, error

    def create_source_instance(self, name:str, src_def: Union[str,AirbyteSourceDefinition], config:Dict, test_connection:bool = True ) -> AirbyteSourceInstance:
        """ Create source instance from configuration, optionally test connection """

        if isinstance(src_def, str):
            src_def_id = src_def
        else:
            src_def_id = src_def.id

        if test_connection:
            status,error = self.test_source_connection(src_def_id,config)
            if not status:
                raise AirbyteException(f"Attempt to connect to source with name:{name}, def:{src_def_id} failed with error: {error}")

        resp = self._make_api_request( "/v1/sources/create",

                                        {
                                            "name":name,
                                            "workspaceId": self.workspace_id ,
                                            "sourceDefinitionId": src_def_id,
                                            "connectionConfiguration": config
                                        }
                                    )
        if resp.status_code < 299:
            return AirbyteSourceInstance(resp.json(), self.get_source_def(src_def_id))
        else:
            raise AirbyteAPIException(resp.request, resp.status_code, resp.content)

    def list_source_instances(self) -> List[AirbyteSourceInstance]:
        """ Return all source instances within a workspace """

        resp = self._make_api_request("/v1/sources/list", {"workspaceId": self.workspace_id})
        if resp.status_code < 299:
            return [ AirbyteSourceInstance(src, self.get_source_def(src['sourceDefinitionId'])) for src in resp.json()["sources"]]
        else:
            raise AirbyteAPIException(resp.request, resp.status_code, resp.content)

    def get_or_create_source_instance(self, name:str, src_def: Union[str,AirbyteSourceDefinition], config:Dict, test_connection:bool = True ) -> AirbyteSourceInstance:
        """ Get or create source instance from configuration, optionally test connection """

        dummy = AirbyteSourceInstance({ "name": name,
                         "sourceDefinitionId": src_def.id,
                         "workspaceId": self.workspace_id,
                         "connectionConfiguration": config
                        }, src_def)

        if not self.test_source_connection(src_def, config):
            raise AirbyteException(f"Attempt to connect to source with name:{name}, def:{src_def} failed")

        instances = self.list_source_instances()

        for instance in instances:
            if instance.has_same_config(dummy) and instance.name == dummy.name:
                return instance

        return self.create_source_instance(name, src_def, config, test_connection=False)

    def search_source_instances(self, src_def: int| AirbyteSourceDefinition | None= None, instance_name: str | None= None) \
            -> List[AirbyteSourceInstance]:
        """ Search for source instances by source definition or instance name """

        if src_def is None and instance_name is None:
            raise ValueError("Either src_def or instance_name must be specified")

        if src_def is None:
            src_def_id = ""
        else:
            if isinstance(src_def, str):
                src_def_id = src_def
            else:
                src_def_id = src_def.id

        if instance_name is None:
            instance_name = ""

        instances = self.list_source_instances()
        return [x for x in instances if x.definition_id == src_def_id or x.name == instance_name]

    def discover_source_data_catalog(self, source:str|AirbyteSourceInstance):

        if isinstance(source, AirbyteSourceInstance):
            source_id = source.id
        else:
            source_id = source

        resp = self._make_api_request("/v1/sources/discover_schema", {"sourceId": source_id, "disable_cache": True})
        if resp.status_code == 200 and resp.json()["jobInfo"].get("succeeded",False) == True:
            return AirbyteSourceCatalog(resp.json())
        else:
            raise AirbyteAPIException(resp.request, resp.status_code, resp.content)

    def get_destination_def(self, dest_def_id:str) -> AirbyteDestinationDefinition:

        if dest_def_id in self.destination_definitions:
            return self.destination_definitions[dest_def_id]
        else:
            raise AirbyteNotFoundError(f"Destination definition not found: {dest_def_id}")

    def get_destination_input_schema(self, dest_def: Union[str, AirbyteDestinationDefinition]) -> Dict:

        if isinstance(dest_def, str):
            dest_def_id = dest_def
        else:
            dest_def_id = dest_def.id

        resp = self._make_api_request("/v1/destination_definition_specifications/get",
                                      {"workspaceId": self.workspace_id ,"destinationDefinitionId": dest_def_id})
        if resp.status_code < 299:
            return resp.json()['connectionSpecification']
        else:
            raise AirbyteAPIException(resp.request, resp.status_code, resp.content)

    def test_destination_connection(self, dest_def: Union[str,AirbyteDestinationDefinition], config:Dict) -> Tuple[bool,str]:
        """Test a destination connection. Returns a tuple of (status, error)"""

        if isinstance(dest_def, str):
            dest_def_id = dest_def
        else:
            dest_def_id = dest_def.id

        resp = self._make_api_request("/v1/scheduler/destinations/check_connection",
                                   { "workspaceId": self.workspace_id,
                                     "destinationDefinitionId": dest_def_id,
                                     "connectionConfiguration": config}
                                   )
        resp_json = resp.json()["jobInfo"]

        status = resp_json.get("succeeded", False)
        error = resp_json.get("failureReason", {}).get("externalMessage", None)

        return status, error

    def create_destination_instance(self, name:str, dest_def: Union[str,AirbyteDestinationDefinition], config:Dict, test_connection:bool = True ) -> AirbyteDestinationInstance:
        """ Create destination instance from configuration, optionally test connection """

        if isinstance(dest_def, str):
            dest_def_id = dest_def
        else:
            dest_def_id = dest_def.id

        if test_connection:
            status,error = self.test_destination_connection(dest_def_id,config)
            if not status:
                raise AirbyteException(f"Attempt to connect to destination with name:{name}, def:{dest_def_id} failed with error: {error}")

        resp = self._make_api_request( "/v1/destinations/create",

                                        {
                                            "name":name,
                                            "workspaceId": self.workspace_id ,
                                            "destinationDefinitionId": dest_def_id,
                                            "connectionConfiguration": config
                                        }
                                    )
        if resp.status_code < 299:
            return AirbyteDestinationInstance(resp.json(), self.get_destination_def(dest_def_id))
        else:
            raise AirbyteAPIException(resp.request, resp.status_code, resp.content)

    def list_destination_instances(self) -> List[AirbyteDestinationInstance]:
        """ Return all destination instances within a workspace """

        resp = self._make_api_request("/v1/destinations/list", {"workspaceId": self.workspace_id})
        if resp.status_code < 299:
            return [ AirbyteDestinationInstance(dest, self.get_destination_def(dest['destinationDefinitionId'])) for dest in resp.json()["destinations"]]
        else:
            raise AirbyteAPIException(resp.request, resp.status_code, resp.content)

    def get_destination_instance(self, dest_instance_id:str) -> AirbyteDestinationInstance:
        """ Get destination instance by id """

        resp = self._make_api_request("/v1/destinations/get", {"destinationId": dest_instance_id})
        if resp.status_code < 299:
            return AirbyteDestinationInstance(resp.json(), self.get_destination_def(resp.json()['destinationDefinitionId']))
        else:
            raise AirbyteAPIException(resp.request, resp.status_code, resp.content)

    def delete_destination_instance(self, dest_instance_id:str) -> bool:
        """ Delete destination instance by id """

        resp = self._make_api_request("/v1/destinations/delete", {"destinationId": dest_instance_id})
        if resp.status_code < 299:
            return True
        else:
            raise AirbyteAPIException(resp.request, resp.status_code, resp.content)

    def search_destination_instances(self, dest_def_id:str = None, instance_name:str = None) -> List[AirbyteDestinationInstance]:
        """ Search for destination instances by definition id or name """

        instances = self.list_destination_instances()

        if dest_def_id is not None:
            instances = [x for x in instances if x.definition_id == dest_def_id]

        if instance_name is not None:
            instances = [x for x in instances if x.name == instance_name]

        return instances

    def setup_connection(self,
                          name: str,
                          source:Union[str,AirbyteSourceInstance],
                          destination:Union[str,AirbyteDestinationInstance],
                          stream_to_copy: str,
                          cursor_field: str,
                          sync_mode:SyncMode,
                          schedule:Schedule) -> AirbyteConnection:
        """ Create a connection between a source and destination """

        if isinstance(source, str):
            source_id = source
        else:
            source_id = source.id

        if isinstance(destination, str):
            destination_id = destination
        else:
            destination_id = destination.id

        source_catalog = self.discover_source_data_catalog(source_id)
        stream_to_sync = source_catalog.get_stream_by_name(stream_to_copy)
        if stream_to_sync is None:
            raise AirbyteException(f"Stream {stream_to_copy} not found in source {source_id}")

        # check if cursor field is valid, get_fields() returns a list of tuples (name, type)
        cursor_field_from_schema = next((field for field in stream_to_sync.get_fields() if field[0] == cursor_field), None)
        if cursor_field_from_schema is None:
            raise AirbyteException(f"Cursor field {cursor_field} not found in stream {stream_to_copy}")

        stream_to_sync = stream_to_sync \
                        .with_cursor_field(cursor_field) \
                        .with_sync_mode(sync_mode) \
                        .with_destination_sync_mode("append")

        if schedule is None:
            schedule = Schedule(60, Schedule.TimeUnit.MINUTES)

        resp = self._make_api_request("/v1/connections/create",
                                          {
                                              "name": name,
                                              "sourceId": source_id,
                                              "destinationId": destination_id,
                                              "syncMode": sync_mode.value,
                                              "syncCatalog": {"streams": [stream_to_sync.to_dict()]},
                                              "sourceCatalogId":source_catalog.id,
                                              "prefix": "",
                                              "namespaceDefinition": "destination",
                                              "namespaceFormat": "${SOURCE_NAMESPACE}",
                                              "nonBreakingChangesPreference": "ignore",
                                              "geography": "auto",
                                              "operations": [],
                                              "status": "inactive",
                                              **schedule.to_dict()
                                          }
                                      )
        if resp.status_code < 299:
            return AirbyteConnection(resp.json())
        else:
            raise AirbyteAPIException(resp.request, resp.status_code, resp.content)

    def start_dataflow(self,conn: str|AirbyteConnection) -> bool:
        """ Start a connection """

        if isinstance(conn, str):
            conn_id = conn
        else:
            conn_id = conn.id

        resp = self._make_api_request("/v1/connections/update",
                                      {"connectionId": conn_id,
                                       "status": "active"})
        if resp.status_code < 299 and resp.json()['status'] == 'active':
            return AirbyteConnection(resp.json())
        else:
            raise AirbyteAPIException(resp.request, resp.status_code, resp.content)

    def stop_dataflow(self,conn: str|AirbyteConnection) -> bool:
        """ Stop a connection """

        if isinstance(conn, str):
            conn_id = conn
        else:
            conn_id = conn.id

        resp = self._make_api_request("/v1/connections/update",
                                      {"connectionId": conn_id,
                                       "status": "inactive"})
        if resp.status_code < 299 and resp.json()['status'] == 'inactive':
            return AirbyteConnection(resp.json())
        else:
            raise AirbyteAPIException(resp.request, resp.status_code, resp.content)


if __name__ == "__main__":

    # create tests for AirbyteEngine
    engine = AirbyteEngine("http://localhost:8001", "admin", "admin", "default")
    print(engine.source_definitions)
    print(engine.destination_definitions)
    print(engine.get_source_def("a0f198c2-2b1f-4f3e-8d4f-0c5f6a8fd7e7"))
    print(engine.get_source_input_schema("a0f198c2-2b1f-4f3e-8d4f-0c5f6a8fd7e7"))
    print(engine.create_source_instance("a0f198c2-2b1f-4f3e-8d4f-0c5f6a8fd7e7", {"username": "postgres", "password": "postgres", "database": "postgres", "host": "localhost", "port": 5432}))

    # create tests for AirbyteConnectorDefinition
    #print(AirbyteConnectorDefinition.preferred_connectors)
    
    # create tests for AirbyteSourceDefinition
    #print(AirbyteSourceDefinition.preferred_connectors)
    #print(AirbyteSourceDefinition("a0f198c2-2b1f-4f3e-8d4f-0c5f6a8fd7e7"))
    #print(AirbyteSourceDefinition("a0f198c2-2b1f-4f3e-8d4f-0c5f6a8fd7e7").preferred)
    #print(AirbyteSourceDefinition("a0f198c2-2b1f-4f3e-8d4f-0c5f6a8fd7e7").name)
    #print(AirbyteSourceDefinition("a0f198c2-2b1f-4f3e-8d4f-0c5f6a8fd7e7").docker_image)
    #print(AirbyteSourceDefinition("a0f198c2-2b1f-4f3e-8d4f-0c5f6a8fd7e7").documentation_url)
    #print(AirbyteSourceDefinition("a0f198c2-2b1f-4f3e-8d4f-0c5f6a8fd7e7").source_type)
    #print(AirbyteSourceDefinition("a0f198c2-2b1f-4f3e-8d4f-0c5f6a8fd7e7").source_definition_id)
   
    # create tests for AirbyteDestinationDefinition
    #print(AirbyteDestinationDefinition.preferred_connectors)
    #print(AirbyteDestinationDefinition("a0f198c2-2b1f-4f3e-8d4f-0c5f6a8fd7e7"))
    #print(AirbyteDestinationDefinition("a0f198c2-2b1f-4f3e-8d4f-0c5f6a8fd7e7").preferred)
    #print(AirbyteDestinationDefinition("a0f198c2-2b1f-4f3e-8d4f-0c5f6a8fd7e7").name)
    #print(AirbyteDestinationDefinition("a0f198c2-2b1f-4f3e-8d4f-0c5f6a8fd7e7").docker_image)
    #print(AirbyteDestinationDefinition("a0f198c2-2b1f-4f3e-8d4f-0c5f6a8fd7e7").documentation_url)
    #print(AirbyteDestinationDefinition("a0f198c2-2b1f-4f3e-8d4f-0c5f6a8fd7e7").destination_type)
    #print(AirbyteDestinationDefinition("a0f198c2-2b1f-4f3e-8d4f-0c5f6a8fd7e7").destination_definition_id)


    # create tests for AirbyteConnection