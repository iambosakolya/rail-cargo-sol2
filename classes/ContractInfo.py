class ContractInfo:
    def __init__(self, contract_id):
        self.contract_id = contract_id

    def set_contract_id(self, contract_id):
        self.contract_id = contract_id

    def get_contract_id(self):
        return self.contract_id


class ContractList:
    contracts = []

    def __init__(self):
        self.contract_info = ContractInfo(None)