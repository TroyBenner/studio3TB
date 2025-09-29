Modal instructions (simple)

1) Install the Modal CLI and Python package: ensure you have `modal` installed and you're logged in.

2) Create a Modal secret named `troy-secret` and set two environment variables inside it:

	- SUPABASE_URL
	- SUPABASE_KEY

	The secret must be named exactly `troy-secret`.

3) Run the modal runner locally (builds the image and runs Streamlit inside Modal):

```bash
python modal_runner.py
```

This will start Streamlit and the app `streamlit_supabase.py` will read
the two env vars from the Modal secret and display the `nfl_rushing_2024_2025` table.

