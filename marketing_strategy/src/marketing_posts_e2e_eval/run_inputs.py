import os
import json
from dotenv import load_dotenv
from marketing_posts_e2e_eval.main import kickoff
from trulens.core import TruSession
from trulens.connectors.snowflake import SnowflakeConnector

load_dotenv()

def run_inputs():
    session = TruSession(
        connector=SnowflakeConnector(
            account="fab02971",
            user=os.getenv("USER"),
            password=os.getenv("SNOWFLAKE_PASSWORD"),
            warehouse=os.getenv("SNOWFLAKE_WAREHOUSE"),
            database=os.getenv("USER"),
            schema="CREWAI",
            role="ENGINEER"
        )
    )
    session.experimental_enable_feature("otel_tracing")

    file_dir = os.path.dirname(os.path.abspath(__file__))
    inputs_file_path = os.path.join(file_dir, "../../run_inputs.json")
    
    with open(inputs_file_path) as fp:
        inputs_file_content = json.load(fp)
        inputs_list = inputs_file_content["inputs_list"]
    
    domain_filter = os.environ.get("domain_filter", None)
    
    domain_filter_lambda = lambda domain: True
    if domain_filter:
        domain_filter_lambda = lambda domain: domain_filter in domain
    
    for inputs in inputs_list:
        domain = inputs["customer_domain"]
        if not domain_filter_lambda(domain):
            continue
        print("#Triggering", inputs)
        kickoff(inputs=inputs)
        print("#Finished")
