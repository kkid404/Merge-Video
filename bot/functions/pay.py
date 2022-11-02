from random import randint

from pyqiwip2p import QiwiP2P

from loader import QIWI
p2p = QiwiP2P(QIWI)

def bill(price, id):
    comment = f"{id}_{randint(10, 100)}"
    bill = p2p.bill(amount=price, comment=comment)
    return bill

def chek_bill(bill_id):
    return str(p2p.check(bill_id=bill_id).status)
