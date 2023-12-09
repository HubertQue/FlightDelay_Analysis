## Airline Delays Analysis and Prediction (for running locally)

### Prerequisites:

```bash
# Clone repository locally
# HTTPS
git clone https://github.sfu.ca/zqa14/FlightDelay_Analysis.git
# (or) SSH
git clone git@github.sfu.ca:zqa14/FlightDelay_Analysis.git
# CD into folder using terminal
cd FlightDelay_Analysis
# install environment
pip install -r requirements.txt
```

### STEP 1:

Using terminal 1 as frontend:

```bash
# Starting from the FlightDelay_Analysis folder
# Open frontend folder 
cd ./client
# install the dependencies in package.json
npm i
# start the frontend server on port "http://127.0.0.1:3000"
npm start
```

### STEP 2:

Using another terminal 2 as backend:

```bash
# Starting from the FlightDelay_Analysis folder
# Open backend folder 
cd ./backend
# (for Windows) enter the venv vitural environment
source venv/Scripts/activate
# start the backend server on port "http://127.0.0.1:5000"
python server_db.py
```

### STEP 3:

Choose a browser and enter "http://localhost:3000" to view the website.
