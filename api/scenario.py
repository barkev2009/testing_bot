from api.testdriver import retry
from api.utils import dotify

from api.stages.draft_app import draft_app
from api.stages.prescoring import prescoring
from api.stages.expertises import expertises
from api.stages.sitting import sitting
from api.stages.cod import cod
from api.stages.deal_preparation import deal_preparation
from api.stages.deal import deal

class scenario_tester(draft_app, prescoring, expertises, sitting, cod, deal_preparation, deal):
    def __init__(self, app_number=None) -> None:
        super().__init__()
        self.app_params.app_number = app_number
        print(f'Номер заявки: {app_number}')
