from hornets.components.pos.enums import DispenserStatusEnum


class Dispenser:

    def __init__(self, dispenser_id: str):
        self.dispenser_id = dispenser_id
        self.dispenser_status = DispenserStatusEnum.UNKNOWN
