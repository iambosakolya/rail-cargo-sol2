import sqlite3
from database import cursor, conn

class ContractInfo:
    def __init__(self, contract_id):
        self.contract_id = contract_id

    def set_contract_id(self, contract_id):
        self.contract_id = contract_id

    def get_contract_id(self):
        return self.contract_id

class ContractList:
    def __init__(self, db_path='data.db'):
        self.contracts = []
        self.db_path = db_path
        self.load_contracts_from_db()

    def load_contracts_from_db(self):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT contract_id FROM contracts")
            rows = cursor.fetchall()
            for row in rows:
                contract_id = row[0]
                self.contracts.append(ContractInfo(contract_id))

    def add_contract(self, contract_info):
        self.contracts.append(contract_info)
        self.save_contract_to_db(contract_info)

    def save_contract_to_db(self, contract_info):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO contracts (contract_id) VALUES (?)",
                           (contract_info.get_contract_id(),))
            conn.commit()

    def find_by_id(self, contract_id):
        for contract in self.contracts:
            if contract.get_contract_id() == contract_id:
                return contract
        return None

    def remove_contract(self, contract_info):
        self.contracts.remove(contract_info)
        self.delete_contract_from_db(contract_info)

    def delete_contract_from_db(self, contract_info):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM contracts WHERE contract_id = ?",
                           (contract_info.get_contract_id(),))
            conn.commit()

    def get_contracts(self):
        return self.contracts