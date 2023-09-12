import requests
import json

from typing import List, Tuple


class SourceDefinition:

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

    enabled_sources = ["Postgres"]
    preferred_sources = ["Postgres"]

    def __init__(self, kwargs):
        self.properties = kwargs

    def getId(self):
        return self.properties.get('sourceDefinitionId')

    def getName(self):
        return self.properties.get('name')

    def getIcon(self):
        return self.properties.get('icon')

    def getDescription(self):
        return self.descriptions.get(self.properties.get('name'))

    def isEnabled(self):
        return self.properties.get('name') in self.enabled_sources

    def getType(self):
        return self.properties.get('dockerRepository').split('/')[1]


class AirbyteHelper:
    def __init__(self, airbyte_base_url, client_id, client_secret):
        self.airbyte_base_url = airbyte_base_url
        self.client_id = client_id
        self.client_secret = client_secret

    def launch_request(self, url_path, data):
        if data is None or len(data.keys()) == 0:
            headers = {}
        else:
            headers = {'Content-type': 'application/json'}
        resp = requests.post(self.airbyte_base_url + "/api" + url_path, data=json.dumps(data), headers=headers,
                             auth=(self.client_id, self.client_secret))
        if resp.status_code > 299:
            print(Exception(str(resp.status_code) + "_" + str(resp.content)))
        return resp

    # ======================================================================
    # Workspaces
    # ======================================================================
    def create_workspace(self, workspace):
        resp = self.launch_request("/v1/workspaces/create", workspace)
        return resp.json()

    def delete_workspace(self, workspace_id):
        self.launch_request("/v1/workspaces/delete", {"workspaceId": workspace_id})
        return True

    def list_workspaces(self):
        resp = self.launch_request("/v1/workspaces/list", {})
        return resp.json()["workspaces"]

    def get_workspace(self, workspace_id):
        resp = self.launch_request("/v1/workspaces/get", {"workspaceId": workspace_id})
        return resp.json()

    def get_workspace_by_slug(self, slug):
        resp = self.launch_request("/v1/workspaces/get_by_slug", {"slug": slug})
        return resp.json()

    def get_first_workspace_id(self):
        return self.list_workspaces()[0]["workspaceId"]

    def get_workspace_by_connection_id(self, connection_id):
        resp = self.launch_request("/v1/workspaces/get_by_connection_id", {"connectionId": connection_id})
        return resp.json()

    def update_workspace(self, workspace):
        resp = self.launch_request("/v1/workspaces/update", workspace)
        return resp.json()

    def update_workspace_name(self, workspace_id, new_name):
        resp = self.launch_request("/v1/workspaces/update", {
            "workspaceId": workspace_id,
            "name": new_name
        })
        return resp.json()

    def update_workspace_tag_feedback_status_as_done(self, workspace_id):
        resp = self.launch_request("/v1/workspaces/tag_feedback_status_as_done", {"workspaceId": workspace_id})
        return resp.json()

    #============================
    # Source Definitions
    #===================================
    def get_source_definitions(self, workspace_id)-> List[SourceDefinition]:
        resp = self.launch_request("/v1/source_definitions/list_for_workspace",
                                   { "workspaceId": workspace_id})

        if resp.status_code == 200:
            source_def_map = { x['name']: SourceDefinition(x) for x in resp.json()['sourceDefinitions']}
            return [source_def_map[x] for x in SourceDefinition.preferred_sources if x in source_def_map.keys()] + \
                     [source_def_map[x] for x in source_def_map.keys() if x not in SourceDefinition.preferred_sources]
        else:
            print(resp.json)
            return []

    def get_source_definition(self, workspace_id, source_definition_id):
        resp = self.launch_request("/v1/source_definitions/get",
                                   {"workspaceId": workspace_id ,"sourceDefinitionId": source_definition_id})
        return resp.json()

    def get_source_specification(self, workspace_id, source_definition_id):
        resp = self.launch_request("/v1/source_definition_specifications/get",
                                   {"workspaceId": workspace_id ,"sourceDefinitionId": source_definition_id})
        return resp.json()['connectionSpecification']

    # Source is not yet created, we are just testing from config if we can connect to source
    def test_source_connection(self,workspace_id, source_definition_id, source_config )-> Tuple[bool,str]:
        resp = self.launch_request("/v1/scheduler/sources/check_connection",
                                   { "workspaceId": workspace_id ,
                                    "sourceDefinitionId": source_definition_id,
                                    "connectionConfiguration": source_config }
                                   )
        resp_json = resp.json()["jobInfo"]

        status = resp_json.get("succeeded", False)
        error =  resp_json.get("failureReason",{}).get("externalMessage",None)

        return (status, error)

    def discover_source_schema(self, source_id):
        resp = self.launch_request("/v1/sources/discover_schema", {"sourceId": source_id, "disable_cache": True })
        return (resp.status_code, resp.json())

    def search_source_instance_by_name(self, workspace_id, source_def_id, source_name):
        instances = self.list_sources(workspace_id)
        return [ x for x in instances if x['sourceDefinitionId'] == source_def_id and x['name'] == source_name ]
    # ======================================================================
    # Sources
    # ======================================================================
    def create_sources(self, source):
        resp = self.launch_request("/v1/sources/create", source)
        return (resp.status_code, resp.json())

    def update_source(self, source):
        resp = self.launch_request("/v1/sources/update", source)
        return resp.json()

    def list_sources(self, workspace_id):
        resp = self.launch_request("/v1/sources/list", {"workspaceId": workspace_id})
        return resp.json()["sources"]

    def get_source(self, source_id):
        resp = self.launch_request("/v1/sources/get", {"sourceId": source_id})
        return resp.json()

    def get_source_most_recent_source_actor_catalog(self, source_id):
        resp = self.launch_request("/v1/sources/get_most_recent_source_actor_catalog", {"sourceId": source_id})
        return resp.json()

    def search_source(self, search_source_body):
        resp = self.launch_request("/v1/sources/search", search_source_body)
        return resp.json()

    def clone_source(self, clone_source_body):
        resp = self.launch_request("/v1/sources/clone", clone_source_body)
        return resp.json()

    def delete_source(self, source_id):
        resp = self.launch_request("/v1/sources/delete", {"sourceId": source_id})
        return resp.json()

    def check_connection_source(self, source_id):
        resp = self.launch_request("/v1/sources/check_connection", {"sourceId": source_id})
        return resp.json()

    def check_connection_for_update_source(self, check_connection_for_update_body):
        resp = self.launch_request("/v1/sources/check_connection_for_update", check_connection_for_update_body)
        return resp.json()

    def discover_schema_source(self, source_id, connection_id, disable_cache, notify_schema_change):
        resp = self.launch_request("/v1/sources/check_connection_for_update", {
            "sourceId": source_id,
            "connectionId": connection_id,
            "disable_cache": disable_cache,
            "notifySchemaChange": notify_schema_change
        })
        return resp.json()

    def write_discover_catalog_result_source(self, write_discover_catalog_result_body):
        resp = self.launch_request("/v1/sources/write_discover_catalog_result", write_discover_catalog_result_body)
        return resp.json()

    # ======================================================================
    # Destinations
    # ======================================================================

    def create_destinations(self, destination):
        resp = self.launch_request("/v1/destinations/create", destination)
        return (resp.status_code, resp.json())

    def update_destinations(self, destination):
        resp = self.launch_request("/v1/destination_definitions/update", destination)
        return resp.json()

    def list_destinations(self, workspace_id):
        resp = self.launch_request("/v1/destinations/list", {"workspaceId": workspace_id})
        return resp.json()["destinations"]

    def get_destination(self, destination_id):
        resp = self.launch_request("/v1/destinations/get", {"destinationId": destination_id})
        return resp.json()

    def delete_destination(self, destination_id):
        self.launch_request("/v1/destinations/delete", {"destinationId": destination_id})
        return True

    def search_destination(self, search_destination_body):
        resp = self.launch_request("/v1/destinations/search", search_destination_body)
        return ( resp.status_code, resp.json() )

    def search_dest_by_definition(self, workspace_id, dest_def_id):
        dests = self.list_destinations(workspace_id)
        return [ dest for dest in dests if dest['destinationDefinitionId'] == dest_def_id]

    def check_connection_destination(self, destination_id):
        resp = self.launch_request("/v1/destinations/check_connection", {"destinationId": destination_id})
        return resp.json()

    def check_connection_for_update_destination(self, check_connection_for_update_body):
        resp = self.launch_request("/v1/destinations/check_connection_for_update", check_connection_for_update_body)
        return resp.json()

    def clone_destination(self, clone_body):
        resp = self.launch_request("/v1/destinations/clone", clone_body)
        return resp.json()

    def delete_all_destinations(self, workspace_id=None):
        if workspace_id is None:
            workspace_id = self.list_workspaces()[0]["workspaceId"]
        print("Workspace ID", workspace_id)
        destinations = self.list_destinations(workspace_id)
        for destination in destinations:
            print("deleting", destination["destinationId"])
            self.delete_destination(destination["destinationId"])

    # ======================================================================
    # Connections
    # ======================================================================

    def create_connection(self, connection):
        resp = self.launch_request("/v1/web_backend/connections/create", connection)
        return (resp.status_code, resp.json())

    def update_connection(self, connection):
        resp = self.launch_request("/v1/connections/update", connection)
        return resp.json()

    def list_connections(self, workspace_id):
        resp = self.launch_request("/v1/connections/list", {"workspaceId": workspace_id})
        return resp.json()

    def list_all_connections(self, workspace_id):
        resp = self.launch_request("/v1/connections/list_all", {"workspaceId": workspace_id})
        return resp.json()

    def get_connection(self, connection_id):
        resp = self.launch_request("/v1/connections/create", {"connectionId": connection_id})
        return resp.json()

    def trigger_connection_sync(self, connection_id):
        resp = self.launch_request("/v1/connections/sync", {"connectionId": connection_id})
        return (resp.status_code,resp.json())

    def delete_connection(self, connection_id):
        self.launch_request("/v1/connections/delete", {"connectionId": connection_id})
        return True

    def search_connections(self, search_connection_body):
        resp = self.launch_request("/v1/connections/search", search_connection_body)
        return resp.json()

    def reset_connection(self, connection_id):
        resp = self.launch_request("/v1/connections/reset", {"connectionId": connection_id})
        return resp.json()

    # ======================================================================
    # Connections
    # ======================================================================
    def get_logs(self):
        resp = self.launch_request("/v1/logs/get", {"logType": "server"})
        return resp.text