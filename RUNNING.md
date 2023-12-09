## Airline Delays Analysis and Prediction (for running locally)

### Prerequisites:

Please note that our project requires Python version 3.9 or higher to run.

```bash
# Clone repository locally
# HTTPS
git clone https://github.sfu.ca/zqa14/FlightDelay_Analysis.git
# (or) SSH
git clone git@github.sfu.ca:zqa14/FlightDelay_Analysis.git
# CD into folder using terminal
cd FlightDelay_Analysis
# install environment
pip install -r requirements.txt --no-binary :all:
```

### STEP 1:

Build the frontend static file:

```bash
# Starting from the FlightDelay_Analysis folder
# Open Frontend folder 
cd ./client
# install dependency
npm i
# build the static frontend file
npm run build
# back to the FlightDelay_Analysis root
cd ..
```

### STEP 2:

Open a terminal as backend (please ensure that port 5000 is not in use):

```bash
# Starting from the FlightDelay_Analysis folder
# Open backend folder 
cd ./backend
# (for Windows) enter the venv vitural environment
source venv/Scripts/activate
# start the backend server on port "http://127.0.0.1:5000"
python server.py
```

### STEP 3:

Choose a browser and enter "http://localhost:5000" to view the website.
