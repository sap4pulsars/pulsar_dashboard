Simple pulsar_dashboard

1. Enter container
docker run -it -p 127.0.0.1:9998:9998  -e DISPLAY=$DISPLAY -v /tmp/.X11-unix/:/tmp/.X11-unix/ sap4pulsars/pulsar_dashboard:latest

1. Run python simple_dashboard.py (internet connection needed as it query's ATNF pulsar catalogue.). 

3. Start a python webserver (python -m http.server 9998) and navigate to file dashboard.html.


