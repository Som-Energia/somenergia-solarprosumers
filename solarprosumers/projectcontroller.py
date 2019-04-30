from yamlns import namespace as ns


class ProjectController:

    _allowed = [
        'status',
        'log',
        'is_paid',
        'preregistration_date',
        'registration_date',
        'date_sent_data',
        'date_prereport',
        'is_valid_prereport',
        'discarded_type',
        'date_technical_visit',
        'date_report',
        'is_valid_report'
    ]

    def _checkAttribute(self, name):
        if name not in self._allowed:
            raise AttributeError(name)

    def __init__(self, **kwds):
        self._changes = ns()
        self._values = ns(kwds)
        for name in kwds:
            self._checkAttribute(name)

    def __setattr__(self, name, value):
        if not name.startswith('_'):
            self._checkAttribute(name)
            self._changes[name]=value
            self._values[name]=value
        return super(
            ProjectController, self).__setattr__(name, value)

    def __getattr__(self, name):
        self._checkAttribute(name)
        return self._values[name]

    def changes(self):
        return self._changes

    def addlog(self, **kwds):
        self.log.append(ns(kwds))

    def preregister(self,
            current_date,
            member_id,
            contract_id,
            campaign_id,
            ):
        self.status = 'preregistered'
        self.is_paid = False
        self.preregistration_date = current_date

    def register(self,
            date_payment,
            register_receipt,
            is_paid,
            member_id,
            contract_id,
            campaign_id,
            ):
        self.status = 'registered'
        self.registration_date = date_payment

    def sent_data(self,
            date_sent_data,
            member_id,
            contract_id,
            campaign_id,
            ):
        self.status = 'data sent'

    def prereport(self,
            date_upload_prereport,
            member_id,
            contract_id,
            campaign_id,
            is_valid_prereport,
            ):
        self.date_prereport = date_upload_prereport
        self.is_valid_prereport = is_valid_prereport
        if not is_valid_prereport:
            self.status = 'prereport_review'
        else:
            self.status = 'technical_visit'

    def prereport_review(self,
            date_prereport_review,
            member_id,
            contract_id,
            campaign_id,
            is_valid_prereport,
            ):
        self.is_valid_prereport = is_valid_prereport
        self.date_prereport = date_prereport_review
        if not is_valid_prereport:
            self.status = 'discarded'
            self.discarded_type = 'technical'
        else:
            self.status = 'prereport'

    def set_technical_visit(self,
            date_set_technical_visit,
            member_id,
            contract_id,
            campaign_id,
            ):
        self.status = 'technical_visit'
        self.date_technical_visit = date_set_technical_visit


# vim: et ts=4 sw=4
