# This code is BSD licensed and free for all uses
# Right now the script is a little tedious to use. 
# It requires a manual export from reminders, although you could easily change it to use a sqlite3 lib.
# To do that, use a sqlite3 python lib to open ~/Library/Calendars/Calendar Cache and 
# run something like "select ZSHAREDUID, ztitle,zstatus, znotes, ZTIMEZONE, ZCREATIONDATE, ZDATESTAMP, 
# ZSTARTDATE, ZENDDATE, ZRECURRENCEENDDATE, ZCOMPLETEDDATE from ZICSELEMENT where zshareduid is not null;", 
# but with a where clause to exclude already synchronized items. 
# If you wanted to get really fancy, you could use apple's modification notification framework to re-sync
# automatically on change.


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
