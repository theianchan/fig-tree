import os
from dotenv import load_dotenv

load_dotenv()

ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY")

base_dir = os.path.abspath(os.path.dirname(__file__))
project_root = os.path.dirname(base_dir)
template_dir = os.path.join(project_root, "templates")
static_dir = os.path.join(project_root, "static")
