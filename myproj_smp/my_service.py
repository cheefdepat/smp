import win32serviceutil
import win32service
import win32event
import servicemanager
import os
import sys
from waitress import serve
from myproj_smp.wsgi import application

class MyService(win32serviceutil.ServiceFramework):
    _svc_name_ = "MyDjangoService"
    _svc_display_name_ = "My Django Service"
    _svc_description_ = "This service runs my Django application."

    def __init__(self, args):
        win32serviceutil.ServiceFramework.__init__(self, args)
        self.stop_event = win32event.CreateEvent(None, 0, 0, None)
        self.running = True

    def SvcStop(self):
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        win32event.SetEvent(self.stop_event)
        self.running = False

    def SvcRun(self):
        servicemanager.LogMsg(servicemanager.EVENTLOG_INFORMATION_TYPE,
                              servicemanager.PYS_SERVICE_STARTED,
                              (self._svc_name_, ''))
        serve(application, host='0.0.0.0', port=8000)

if __name__ == '__main__':
    win32serviceutil.HandleCommandLine(MyService)
