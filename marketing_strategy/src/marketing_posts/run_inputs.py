import os
import json
from crewai import Crew
from dotenv import load_dotenv
from marketing_posts.crew import MarketingPostsCrew

load_dotenv()

def _run_inputs_file(crew: Crew):
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
        crew.kickoff(inputs=inputs)
        print("#Finished")

def run_inputs():
    return _run_inputs_file(crew=MarketingPostsCrew().crew())
