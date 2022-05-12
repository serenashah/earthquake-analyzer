# Global Earthquake Analyzer - Magnitudes and Errors

This application outputs data for earthquakes that have been sensed and recorded all around the globe, including magnitude, location, time, etc. The application does this by collecting data from a CSV file and making it easier for a user to read all details associated with a particular earthquake or find data based on a specific factor such as magnitude of a certain size.   

## Files
##### ```/src```: Source Scripts
- ```app.py```: this Flask application that uses CRUD operations and allows users to submit jobs to output information about the ISS 
- ```jobs.py```: this Python script creates a job from the Flask API and adds it to a HotQueue queue, and updates its status.
- ```worker.py```: this Python script reads the queue and executes a mapping and plotting analysis.
##### Container files
- ```Dockerfile.api```: creates a Docker image needed to containerize the Flask application
- ```Dockerfile.wrk```: creates a Docker image needed to containerize the worker
- ```Makefile```: automation tool that serves as a tool to clean, build, and run the containers
- ```requirements.txt```: captures the required libraries and packages for the application in Dockerfiles
##### ```/test```: Test Suite
- ```test_app.py```: Pytest suite for the Flask application routes
##### ```/kubernetes/prod```: Kubernetes yaml Files
- ```app-prod-api-deployment.yml```: pulls earthquake api container from Dockerhub and deploys it.
- ```app-prod-api-service.yml```: provides an IP for the user to curl for their routes.
- ```app-prod-db-deployment.yml```: pulls Redis image from DockerHub and deploys the database.
- ```app-prod-db-service.yml```: provides a Redis IP so that the deployments can access the dataset's database.
- ```app-prod-db-pvc.yml```: make a request for storage to the Kubernetes admin for the database.
- ```app-prod-wrk-deployment.yml```: pulls worker container from DockerHub and deploys it in two replicas so that two workers can be working on the queue concurrently.

##### CSV file to be used as data:
Features of the data include: time, magnitude, depth, number of stations, and place of earthquake.
- ```all_month.csv```: a CSV with global earthquake data set that describes various features of the recorded earthquake

### Obtaining Dataset
The CSV file above comes from the United State government's official website found [here](https://earthquake.usgs.gov/earthquakes/feed/v1.0/csv.php).

### Get files

##### Clone the contents of this repository by entering what follows the $ into a terminal or SCP client:

```
$ git clone https://github.com/serenashah/earthquake-analyzer.git
```

(other methods for cloning a repository are described [here](https://docs.github.com/en/repositories/creating-and-managing-repositories/cloning-a-repository))

#### CSV file download
- Required data files: `all_month.csv` 
- Download the data [here](https://earthquake.usgs.gov/earthquakes/feed/v1.0/csv.php)
    - ```all_month.csv```: "All Earthquakes"

##### Download the files by entering what follows the $ into a terminal or SCP client:
```
$ https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_month.csv
```

## Build Containerized App on Local Machine

The images may built by using either the Dockerfiles or Makefile in this repository.
Replace `<username>` and `<tag>` with your own username and tag.
You may replace `<your port number>` with 5028 or another port not in use

### Using Makefile
####  Enter the following to build and run new image
```
$ make all
```
This stops, builds, and runs the API image, worker image, and Redis image.
Create a directory ```data``` with root privileges to mount the data before running this command.
Alter the ```NAME```, ```GID```, and ```UID``` at the top of the Makefile with the appropriate values for your local machine.

The containers will run in the background and you can curl routes provided by the Flask API once you have posted data to the application.

## Deploying Containers in Kubernetes
Once you're in your Kuberenetes namespace, enter a Python debug pod to be able to access the API's HTTP routes. The deployments for the api, its service, the database, its service and volume claim, and the worker have been deployed. 
Enter the pod with the following command:
```
$ kubectl exec -it <python debug pod> -- /bin/bash
#
```
If you wish to create your own API, worker, and database pods use the command below for each of the yaml files to deploy. Be sure to configure your db pods first so that the API and worker can find the IP of the DB.
```
$ kubectl apply -f <app-prod-yamlfile>
```

You can now curl routes from the API using the already-deployed Flask service IP: 10.110.200.217 with the port 5000 through both terminal and browser (for routes receiving data). When interacting through browser, use the public URL: https://isp-proxy.tacc.utexas.edu/s_shah-1/.

## How to Interact with the Application
This section details how to interact with the application and interpret the results.

The following is a template of how to interact with the application with by ```curl```ing routes.

```
$ curl <ip_address>:<port_number>/<route>
```
In the Kubernetes namespace, use the IP '10.110.200.217' with port '5000'.
In your local machine, use the IP 'localhost' with port '5028'.
The routes are listed below.

#### `/help` - shows list of routes

```
$ curl localhost:<your port number>/help
```
 
Output below explains how to download the data and lists of the routes:

```
FIRST LOAD DATA USING THE FOLLOWING PATH: /data -X POST\n
    IF THERE ARE ERROR LOAD THE DATA ONCE MORE
    
    Use the following routes to access the data:
      1.  /help
          #explains navigation of the app
      2.  /data
          #retrieves data usable in a JSON format, GET returns it
      3.  /feature/<feat_string>
          #posts data for a specific column in the csv
      4.  /earthquake/<id_num>
          #posts data from all columns for one earthquake
      5.  /magnitude/<mag>
          #all the earthquakes for a given magnitude
      6.  /delete/<id_num>
          #deletes an entry on the list based on id, or use 'all' to delete all jobs
      7.  /update/<id_num>/<feature_string>/<new_value>
          #changes the value of a feature for an earthquake
      8.  /jobs
          #uses a JSON to create a job
      9.  /jobs/delete/<job_uuid>
          #deletes one of the jobs that has been created
      10.  /jobs/<job_uuid>
          #API route for checking on the status of a submitted job
      11.  /download_map/<job_uuid>
          #plots map of earthquake magnitudes and downloads as png
      12.  /download_plot/<job_uuid>
          #plots graph of earthquake magnitudes and downloads to local machine 
```

#### `/data` - loads data from CSV files and returns it
To load the data:
```
$ curl <ip_address><port_number>/data -X POST
```
 
Output below is confirmation that the functions in app.py can now use the CSV data:

```
Data has been loaded.
```

The following output is an error message that appears when the correct verb is accidentally omitted or wrongly appended.

```
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 3.2 Final//EN">
<title>405 Method Not Allowed</title>
<h1>Method Not Allowed</h1>
<p>The method is not allowed for the requested URL.</p>
````
To return the data:
```
$ curl <ip_address><port_number>/data
```
Sample output:
```
...
 {
    "time": "2022-04-07T16:06:22.696Z",
    "latitude": "38.1741",
    "longitude": "-117.8659",
    "depth": "7",
    "mag": "1.2",
    "magType": "ml",
    "nst": "9",
    "gap": "178.82",
    "dmin": "0.082",
    "rms": "0.0963",
    "net": "nn",
    "id": "nn00836839",
    "updated": "2022-04-29T21:01:48.065Z",
    "place": "32 km SE of Mina, Nevada",
    "type": "earthquake",
    "horizontalError": "",
    "depthError": "2.3",
    "magError": "0.49",
    "magNst": "4",
    "status": "reviewed",
    "locationSource": "nn",
    "magSource": "nn"
  },
  {
    "time": "2022-04-10T21:32:27.950Z",
    "latitude": "44.2876667",
    "longitude": "-115.1273333",
    "depth": "17.59",
    "mag": "1.63",
    "magType": "ml",
    "nst": "9",
    "gap": "107",
    "dmin": "0.787",
    "rms": "0.12",
    "net": "mb",
    "id": "mb80542779",
    "updated": "2022-04-11T15:20:26.150Z",
    "place": "16 km WNW of Stanley, Idaho",
    "type": "earthquake",
...
```

#### `/feature/<feat_string>` - lists a given feature for all earthquakes

```
$ curl <ip_address><port_number>/feature/<feat_string>
```
 
Sample output of earthquakes feature:

```
...
"[ID hv72995457]: 5 km SSW of P\u0101hala, Hawaii",
 "[ID hv72981557]: 4 km E of P\u0101hala, Hawaii",
 "[ID ak0224to2szd]: 40 km SSW of Skwentna, Alaska",
 "[ID ok2022ilmh]: 7 km E of El Reno, Oklahoma",
 "[ID se60149643]: 8 km NNW of Taylors, South Carolina",
 "[ID nc73717615]: 13km ENE of Cloverdale, CA",
 "[ID hv72993307]: 4 km SSW of P\u0101hala, Hawaii",
 "[ID nn00837136]: 28 km NNE of Indian Springs, Nevada",
 "[ID ci40248280]: 11km SSW of Idyllwild, CA",
 "[ID nc73718245]: 2km NNW of The Geysers, CA",
 "[ID nc73718301]: 7km W of Cobb, CA",
 "[ID ak0224vjldy4]: 34 km SW of Dry Creek, Alaska",
 "[ID av91055253]: 23 km WSW of Dutch Harbor, Alaska",
 "[ID uu60489427]: 45 km SE of Mammoth, Wyoming",
 "[ID nn00836634]: 29 km SSE of Mina, Nevada",
 "[ID nc73725656]: 7km NW of The Geysers, CA",
...
```

The lists above may be much longer and is only an excerpt marked with breaks `...`.

#### `/earthquake/<id_num>` data for specific earthquake

```
$ curl <ip_address><port_number>/earthquake/<id_num>
```
Example:

```
$ curl <ip_address><port_number>/earthquake/us7000h0yj
```

Output below is the data associated with one earthquake:

```
Earthquake us7000h0yj
{
 "time": "2022-04-09T20:52:37.344Z",
 "latitude": "-16.3181",
 "longitude": "166.8507",
 "depth": "14",
 "mag": "6.3",
 "magType": "mww",
 "nst": "",
 "gap": "33",
 "dmin": "0.93",
 "rms": "0.88",
 "net": "us",
 "id": "us7000h0yj",
 "updated": "2022-04-10T20:57:42.406Z",
 "place": "64 km WSW of Norsup, Vanuatu",
 "type": "earthquake",
 "horizontalError": "5.6",
 "depthError": "1.7",
 "magError": "0.038",
 "magNst": "68",
 "status": "reviewed",
 "locationSource": "us",
 "magSource": "us"
}
```
#### `/magnitude/<mag>` - lists all countries

```
$ curl <ip_address><port_number>/magnitude/<mag>
```
 
This route outputs a list of all earthquakes in the last 30 days that have had a magnitude above the inputted number.

```
Magnitudes above 6
[
 "[ID us7000h0yj]: 6.3",
 "[ID us6000hf49]: 6",
 "[ID us6000hf75]: 6.7",
 "[ID us7000h373]: 6.1",
 "[ID us7000h5mc]: 6",
 "[ID usd000h551]: 6"
]
```
In the example above, a magnitude of 6 was inputted.


#### `/delete/<id_num>` - delete an earthquake from the dataset

```
$ curl <ip_address><port_number>/delete/<id> -X DELETE
```

Example:
```
$ curl <ip_address><port_number>/delete/us7000h373 -X DELETE
```
Output:
```
Earthquake us7000h373 DELETED.
```

#### `/update/<id_num>/<feature_string>/<new_value>` - update an earthquake's feature
```
$ curl <ip_address><port_number>/update/<id_num>/<feature_string>/<new_value> -X PUT
```

Example:
```
$ curl <ip_address><port_number>/update/us7000h0yj/mag/3 -X PUT
```
 
Output:
```
Earthquake us7000h0yj-> mag UPDATED to 3.
```
Check that your CRUD operations have been effective by checking the route of the specific earthquake with its id.

#### `/jobs` - post and return a job to a queue
To check your jobs:
```
$ curl <ip_address><port_number>/jobs 
``` 
Output:
```
[
 {
  "id": "09c3445a-4a96-4813-916e-9c0f1c9e28b7",
  "datetime": "2022-05-12 05:45:07.950146",
  "status": "complete",
  "mag": "2.0"
 },
 {
  "id": "ed7e3439-c2ca-48ac-837e-00e49015ef2e",
  "datetime": "2022-05-12 05:55:23.908958",
  "status": "complete",
  "mag": "2.0"
 },
 {
  "id": "0652c635-8645-407b-a93f-6f55a77a2a27",
  "datetime": "2022-05-12 05:34:33.971769",
  "status": "complete",
  "mag": "2.0"
 }
]

  To submit a job, do the following:
        curl <ip_address>:<flask_port>/jobs -X POST -d '{"mag":<mag_num>}' -H "Content-Type: application/json"
```
To post a route, as shown above:
```
$ curl <ip_address>:<port_number>/jobs -X POST -d '{"mag":4.0}' -H "Content-Type: application/json"
```
Output:
```
{
  "id": "31f9b6ea-acc9-4960-8fde-655ba093af77",
  "datetime": "2022-05-12 08:12:51.063950",
  "status": "submitted",
  "mag": 4.0
}
```

#### `/jobs/delete/<job_uuid>` - delete a specific job or all jobs

```
$ curl <ip_address><port_number>/jobs/delete/<job_uuid> -X DELETE
```

Example:
```
$ curl <ip_address><port_number>/jobs/delete/all -X DELETE
``` 
Output is for deleting all jobs. If specific job desired, use its ID.
```
All jobs deleted.
```
#### `/jobs/<job_uuid>` - returns update for a specific job

```
$ curl <ip_address><port_number>/jobs/<job_uuid> 
```

Example:
```
$ curl <ip_address><port_number>/jobs/7987e80f-b1f4-4983-bf53-2cfc33d0ffff
```
Output:

```
{
"id": "7987e80f-b1f4-4983-bf53-2cfc33d0ffff",
"datetime": "2022-05-12 08:18:13.961522",
"status": "complete",
"mag": "4.0"
}
```
#### `/download_map/<job_uuid>` - returns map plotted by workers of earthquakes above the magnitude

```
$ curl <ip_address><port_number>/download_map/<job_uuid>
```

Example:
```
$ curl <ip_address><port_number>/download_map/7987e80f-b1f4-4983-bf53-2cfc33d0ffff > map.png
```
Note that this command needs to be piped into a file with the `>` operator if used in terminal. In browser, it will download into a file and pop up on its own.
Output:
```
 % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed  0     0    0     0    0     0      0      0 --:--:-- --:--:-- --:--:--     100 1034k  100 1034k    0     0  47.5M      0 --:--:-- --:--:-- --:--:-- 48.0M
```

#### `/download_plot/<job_uuid>` - returns plot created by worker of error versus sensors for a given magnitude of earthquakes

```
$ curl <ip_address><port_number>/download_plot/<job_uuid>
```

Example:
```
$ curl <ip_address><port_number>/download_plot/7987e80f-b1f4-4983-bf53-2cfc33d0ffff > plot.png
```
Note that this command needs to be piped into a file with the `>` operator if used in terminal. In browser, it will download into a file and pop up on its own.
Output:
```
 % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed  0     0    0     0    0     0      0      0 --:--:-- --:--:-- --:--:--     100 1034k  100 1034k    0     0  47.5M      0 --:--:-- --:--:-- --:--:-- 48.0M
```

### Testing the interface
To ensure that the API is creating jobs and returning routes as expected, use the test suite in the ```/test``` folder, under ```test_app.py```. This test provides 6 tests for the jobs, API, and worker. To run this test, simply run the following command below. This should not be run in the Kubernetes namespace.
```
$ pytest test/test_app.py
```
Output:
```
collected 6 items

test/test_app.py ......                                                                                                                                              [100%]

============================================================================ 6 passed in 39.56s ============================================================================
```
### Happy analyzing and querying!
