import sqlite3

class ContractInfo:
    def __init__(self, contract_id):
        self.contract_id = contract_id

    def set_contract_id(self, contract_id):
        self.contract_id = contract_id

    def get_contract_id(self):
        return self.contract_id

class ContractList:
    def __init__(self, db_path='data.db'):
        self.contracts = []  # ініціалізуємо список contracts тут
        self.db_path = db_path
        self.load_contracts_from_db()

    def load_contracts_from_db(self):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT contract_id FROM Archive")
            rows = cursor.fetchall()
            for row in rows:
                contract_id = row[0]
                self.contracts.append(ContractInfo(contract_id))

    def add_contract(self, contract_info):
        if isinstance(contract_info, ContractInfo):  # перевіряємо, чи це об'єкт ContractInfo
            self.contracts.append(contract_info)
            self.save_contract_to_db(contract_info)
        else:
            raise ValueError("Expected a ContractInfo object")

    def save_contract_to_db(self, contract_info):
        if isinstance(contract_info, ContractInfo):  # перевіряємо, чи це об'єкт ContractInfo
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("INSERT INTO Archive (contract_id) VALUES (?)",
                               (contract_info.get_contract_id(),))
                conn.commit()
        else:
            raise ValueError("Expected a ContractInfo object")

    def delete_contract_from_db(self, contract_info):
        if isinstance(contract_info, ContractInfo):  # перевіряємо, чи це об'єкт ContractInfo
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("DELETE FROM Archive WHERE contract_id = ?",
                               (contract_info.get_contract_id(),))
                conn.commit()
        else:
            raise ValueError("Expected a ContractInfo object")

