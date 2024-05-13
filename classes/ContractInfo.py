class ContractInfo:
    def __init__(self, contract_id):
        self.contract_id = contract_id

    def set_contract_id(self, contract_id):
        self.contract_id = contract_id

    def get_contract_id(self):
        return self.contract_id

class ContractList:
    def __init__(self):
        self.contracts = []

    def add_contract(self, contract_info):
        self.contracts.append(contract_info)

    def remove_contract(self, contract_info):
        self.contracts.remove(contract_info)

    def get_contracts(self):
        return self.contracts