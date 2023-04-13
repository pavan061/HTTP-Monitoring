# HTTP-Monitoring


<p>This Python script checks the availability of a list of endpoints and logs the percentage of successful responses. It uses the requests library to send HTTP requests and the pyyaml library to read the endpoint configuration from a YAML file.</p>
<h2>Steps</h2>
<ol>
  <li>Install Python 3.6 or later on your machine if it is not already installed. You can download Python from the official website: <a href="https://www.python.org/downloads/">https://www.python.org/downloads/</a></li>
  <li>Install the required packages using pip by running the following command in your terminal or command prompt:</li>
</ol>
<b>pip install requests pyyaml</b>
<ol start="3">
  <li>Run the script with the following command:</li>
</ol>
<b>python main.py input.yaml</b>
<br></br>
<br><p>The script will run indefinitely, testing each endpoint every 15 seconds and logging the availability percentage for each domain. Press Ctrl + C to stop the script.</p></br>
