# playing-with-fastapi
Sample project with FastAPI (Python)

## Data
The data was adapted from https://energydata.info/dataset/installed-electricity-capacity-by-country-area-mw-by-country
and stored in `data/` as `world_eletric_cap.db` (an `sqlite3` database).

It consists of a single table `eleccap` with columns "country" (text),	"tech" (text), "grid_conn_type" (text with two values, "On-grid" and "Off-grid"),	"year" (integer), and	"capacity" (float, given in MW and normalized on country area if I understood the original data source well). To go from original data to the sqlite3 DB, just download the excell from https://energydata.info/dataset/installed-electricity-capacity-by-country-area-mw-by-country, save as CSV (and remove the header row), then check out `one_time_scripts/excel2sqlite.ipynb`.

We could have separate tables for countries, technology and grid connection type since those are categorical values that are repeated many times, but we put everything in a single table since the focus here is not DB conception or normalization.