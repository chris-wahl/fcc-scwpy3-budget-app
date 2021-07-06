class Category:
    category: str
    ledger: list

    def __init__(self, category: str):
        self.category = category.title()
        self.ledger = []

    def get_balance(self) -> float:
        return sum([entry['amount'] for entry in self.ledger], 0)

    def check_funds(self, amount: float) -> bool:
        return self.get_balance() >= amount

    def deposit(self, amount: float, description: str = ''):
        self.ledger.append({
            'amount': amount,
            'description': description
        })

    def withdraw(self, amount: float, description: str = '') -> bool:
        if self.check_funds(abs(amount)):
            self.ledger.append({
                'amount': 0 - abs(amount),
                'description': description
            })
            return True
        return False

    def transfer(self, amount, category: 'Category') -> bool:
        if self.withdraw(amount, f'Transfer to {category.category}'):
            category.deposit(amount, f'Transfer from {self.category}')
            return True
        return False

    def __str__(self):
        total = self.get_balance()
        s = self.category.center(30, '*')

        ledger = '\n'.join([
            f"{entry['description'][:23]:<23}{entry['amount']:>7.2f}"
            for entry in self.ledger
        ])

        if ledger:
            s += f'\n{ledger}'
        s += f'\nTotal: {total}'

        return s

def create_spend_chart(categories):
    pass
