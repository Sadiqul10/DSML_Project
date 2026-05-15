# DSML 311 Service Requests Project

This DSML project predicts whether a 311 service request will close quickly.

The target is:

```text
fast_close = 1 if Closed Date - Created Date <= 48 hours
fast_close = 0 otherwise
```

The model uses only fields that are available when the request is created, such as agency, complaint type, borough, submission channel, zip code, latitude, longitude, and created-date features.

## Dataset

Main dataset:

```text
C:\Users\Sadiqul Islam\Downloads\NY 311 Service Requests\311-service-requests-from-2010-to-present.csv
```

This file is very large, so the code trains on a configurable number of rows instead of loading everything at once.

## Step 1: Install Requirements

```powershell
& 'C:\Users\Sadiqul Islam\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe' -m pip install -r requirements.txt
```

## Step 2: Explore the Dataset

```powershell
& 'C:\Users\Sadiqul Islam\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe' src\explore_data.py --rows 100000
```

This prints:

- dataset shape
- missing values
- most common complaint types
- borough counts
- resolution-time summary

## Step 3: Train the Model

```powershell
& 'C:\Users\Sadiqul Islam\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe' src\train_model.py --rows 100000 --fast-close-hours 48
```

Outputs:

```text
models\dsml_311_fast_close_model.joblib
reports\classification_report.txt
reports\confusion_matrix.png
```

## Step 4: Try More Data

After the first run works, increase rows:

```powershell
& 'C:\Users\Sadiqul Islam\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe' src\train_model.py --rows 500000 --fast-close-hours 48
```

## Step 5: Predict New Requests

Create a small CSV with the same feature columns, then run:

```powershell
& 'C:\Users\Sadiqul Islam\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe' src\predict.py --input new_requests.csv --output reports\predictions.csv
```

The output adds:

- `fast_close_prediction`
- `fast_close_probability`

## Step 6: Run the API Locally

Start the FastAPI server:

```powershell
& 'C:\Users\Sadiqul Islam\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe' -m uvicorn src.api:app --host 127.0.0.1 --port 8000
```

Open API docs:

```text
http://127.0.0.1:8000/docs
```

Health check:

```text
GET http://127.0.0.1:8000/health
```

Prediction endpoint:

```text
POST http://127.0.0.1:8000/predict
```

Use this JSON body:

```json
{
  "created_date": "2019-12-01T02:04:01.000",
  "agency": "DOT",
  "complaint_type": "Street Condition",
  "descriptor": "Pothole",
  "location_type": "Street",
  "incident_zip": "10001",
  "borough": "MANHATTAN",
  "open_data_channel_type": "ONLINE",
  "latitude": 40.745668482774114,
  "longitude": -73.9877188309367
}
```

Example response:

```json
{
  "fast_close_prediction": 1,
  "fast_close_label": "fast_close",
  "fast_close_probability": 0.977,
  "fast_close_hours": 48.0
}
```

## Step 7: Test in Postman

1. Open Postman.
2. Create a new `POST` request.
3. URL:

```text
http://127.0.0.1:8000/predict
```

4. Go to `Body`.
5. Select `raw`.
6. Select `JSON`.
7. Paste the JSON from `postman_sample_request.json`.
8. Click `Send`.

You should receive `fast_close_prediction`, `fast_close_label`, and `fast_close_probability`.

## Step 8: Deploy on Render

This project includes `render.yaml` and `Procfile`.

Render settings:

```text
Build Command: pip install -r requirements.txt
Start Command: uvicorn src.api:app --host 0.0.0.0 --port $PORT
```

Deploy steps:

1. Push this project to a GitHub repository.
2. Go to Render.
3. Click `New +`.
4. Select `Web Service`.
5. Connect your GitHub repository.
6. Select Python environment.
7. Use the build and start commands above.
8. Click `Deploy Web Service`.

After deploy, test:

```text
https://your-render-app-name.onrender.com/health
https://your-render-app-name.onrender.com/docs
```

Then test this endpoint in Postman:

```text
POST https://your-render-app-name.onrender.com/predict
```

## Project Files

```text
src\config.py          dataset path and column settings
src\explore_data.py    simple EDA script
src\train_model.py     training and evaluation script
src\predict.py         prediction script
src\api.py             DSML FastAPI deployment API
requirements.txt       Python dependencies
models\                saved model output
reports\               reports and charts
```
