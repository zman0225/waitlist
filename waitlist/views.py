from pyramid.view import view_config

from models import UserModelManager

import logging

@view_config(route_name='home', renderer='templates/index.jinja2')
def my_view(request):
    p = request.POST
    email = p.get('email_input')
    ref = request.params.get('ref')
    error = None
    uuid = None
    referrals = 0

    if request.method=='POST':
        if not UserModelManager.check_email(email):
            error = "INVALID EMAIL"
            logging.warn("invalid email")
        elif not UserModelManager.email_exists(email):
            ref = ref if ref else "root"
            uuid = UserModelManager.add_email(email,ref)
            logging.warn("valid email -- registered")
        else:
            data = UserModelManager.get_info(email)

            uuid = data['uuid']
            referrals = int(data['referrals'])
            logging.warn("already registered"+str(data))

    total_users = UserModelManager.get_total_users()

    return {'ref':ref,'total_users':total_users,'error':error, 'uuid':uuid, 'referrals':referrals}
