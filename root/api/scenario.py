from root.api.testdriver import retry
from root.api.utils import dotify

from root.api.stages.draft_app import draft_app
from root.api.stages.prescoring import prescoring
from root.api.stages.expertises import expertises
from root.api.stages.sitting import sitting
from root.api.stages.cod import cod
from root.api.stages.deal_preparation import deal_preparation
from root.api.stages.deal import deal

class scenario_tester(draft_app, prescoring, expertises, sitting, cod, deal_preparation, deal):
    def __init__(self, app_number=None) -> None:
        super().__init__()
        self.app_params.app_number = app_number
        print(f'Номер заявки: {app_number}')
