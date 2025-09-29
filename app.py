import shlex
import subprocess
from pathlib import Path
import os
from dotenv import load_dotenv
import modal

#Load environment from .env file
load_dotenv()

streamlit_script_local_path = Path(__file__).parent / "streamlit_run.py"
streamlit_script_remote_path = "/root/streamlit_run.py"
image = (
    modal.Image.debian_slim(python_version="3.9")
    .pip_install("streamlit", "supabase", "pandas", "python-dotenv", "plotly")
    .add_local_file(streamlit_script_local_path, streamlit_script_remote_path)
)
app = modal.App(name="supabase-streamlit-app", image=image)

if not streamlit_script_local_path.exists():
    raise RuntimeError(
        "The Streamlit script does not exist. Please ensure `streamlit_run.py` is present."
    )

@app.function(
    allow_concurrent_inputs=100, secrets=[modal.Secret.from_name("troy-secret")]
)
@modal.web_server(8000)
def run():
    target = shlex.quote(streamlit_script_remote_path)
    cmd = f"streamlit run {target} --server.port 8000 --server.enableCORS=false --server.enableXsrfProtection=false"
    
    #Build environment variables
    env_vars = {}
    if os.getenv("SUPABASE_KEY"):
        env_vars["SUPABASE_KEY"] = os.getenv("SUPABASE_KEY")
    if os.getenv("SUPABASE_URL"):
        env_vars["SUPABASE_URL"] = os.getenv("SUPABASE_URL")

    env_vars.update(os.environ)

    subprocess.Popen(cmd, shell=True, env=env_vars)



