# This code is BSD licensed and free for all uses

from icalendar import Calendar, Event
import httplib, urllib, base64

cal = Calendar.from_ical(open('/path/to/ics/file.ics','rb').read())

api_key = 'api_key_goes_here'
workspace_id = 'worksspace_id_goes_here'
# to get project id curl -u apikeygoeshere: https://app.asana.com/api/1.0/projects
project_id = 'project_id_goes_here'
base64string = base64.encodestring('%s:%s' % (api_key, '')).replace('\n', '')

for component in cal.walk():
    print component.get('summary')
    print component.get('status')
    if component.get('status') == 'COMPLETED':
        status = 'true'
    else:
        status = 'false'
    conn = httplib.HTTPSConnection('app.asana.com', 443, strict = True)
    params = urllib.urlencode({'completed': status, 'name': component.get('summary'), 'workspace': workspace_id, 'assignee': 'me'})
    headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain", 'Authorization': "Basic %s" % base64string}
    conn.request("POST", "/api/1.0/tasks", params, headers)
    response = conn.getresponse()
    print response.status, response.reason
    data = response.read()
    print data
    conn.close()
