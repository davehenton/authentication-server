import os
import logging
import user_management.models as db

from pyramid.events import subscriber

log = logging.getLogger(__name__)


class HealthCheckEvent(object):
    """ Pyramid_health health check event """

    def __init__(self):
        self.checks = []

    def report(self, name, status, message=None):
        """ Report the result of an application check

        Args:
            name (str): Name of the application check
            status (str): Check status. Must be either "OK" or "ERROR"
            message (str): Optional detail about the check result
        """
        self.checks.append({
            'name': name,
            'status': status,
            'message': message
            })

    @property
    def status(self):
        """ Return 'OK' if all checks are OK and if no checks were reported """
        # all([]) is True
        if all([check['status'] == 'OK' for check in self.checks]):
            return dict(status='OK')
        else:
            return dict(status='ERROR')


def includeme(config):
    settings = config.registry.settings
    url = settings.get('healthcheck.url', '/status')
    disablefile = settings.get('healthcheck.disablefile', False)
    maintenance_code = int(settings.get('healthcheck.maintenance_code', 299))
    failure_code = int(settings.get('healthcheck.failure_code', 503))

    def health(request):
        if disablefile and os.path.exists(disablefile):
            log.info("Health response: MAINTENANCE")
            request.response.status_code = maintenance_code
            return dict(status='MAINTENANCE')

        event = HealthCheckEvent()
        request.registry.notify(event)

        if event.status == 'ERROR':
            log.error("Health response: ERROR (%s)", event.checks)
            request.response.status_code = failure_code

        return {check.get('name'):{'status':check.get('status'), 'message':check.get('message')} for check in event.checks}

    config.add_route('healthcheck', url)
    config.add_view(health, route_name='healthcheck', renderer='json')


@subscriber(HealthCheckEvent)
def db_health_check_event(event):
    try:
        db_health_check()
    except:
        event.report(name='db', status='ERROR', message='ping failed')
    else:
        event.report(name='db', status='OK')


def db_health_check():
    db.DBSession.execute('SELECT 1')