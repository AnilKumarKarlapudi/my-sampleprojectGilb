from hornets.models.credit_card.models import CreditCard
from hornets.models.dispenser import Dispenser
from libs.simulators_interface.crindsim import CrindSim


class DispenserWithCrind(Dispenser):

    def __init__(self, dispenser_id: str):
        super().__init__(dispenser_id=dispenser_id)
        self.crindsim = CrindSim(dispenser_id=dispenser_id)

    def fuel_transaction(self, credit_card: CreditCard):
        self.crindsim.outside_sale(credit_card)

    def get_receipt(self):
        return self.crindsim.get_receipt()

    def check_receipt_for(self, receipt: list):
        return self.crindsim.check_receipt_for(receipt)
