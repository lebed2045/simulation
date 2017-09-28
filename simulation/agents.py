from mesa import Agent
import model

class MarketPlayer(Agent):
    """
    An agent with a fixed initial wealth in fiat, with which it must buy into the market.
    The agent may escrow curits in order to issue nomins, and use various strategies in order
    to trade in the marketplace. Its aim is to increase its own wealth.
    """

    def __init__(self, unique_id, model, endowment):
        super().__init__(unique_id, model)
        self.fiat = endowment 
        self.curits = 0
        self.nomins = 0
        self.escrowed_curits = 0
        self.issued_nomins = 0

        self.orders = set()

    def wealth(self) -> float:
        """Return the total wealth of this agent at current fiat prices."""
        return self.fiat + \
               self.model.cur_to_fiat(self.curits + self.escrowed_curits) + \
               self.model.nom_to_fiat(self.nomins - self.issued_nomins)

    def transfer_fiat_to(self, recipient:"MarketPlayer", value:float) -> bool:
        """Transfer a positive value of fiat to the recipient, if balance is sufficient. Return True on success."""
        return self.model.transfer_fiat(self, recipient, value)
    
    def transfer_curits_to(self, recipient:"MarketPlayer", value:float) -> bool:
        """Transfer a positive value of curits to the recipient, if balance is sufficient. Return True on success."""
        return self.model.transfer_curits(self, recipient, value)

    def transfer_nomins_to(self, recipient:"MarketPlayer", value:float) -> bool:
        """Transfer a positive value of nomins to the recipient, if balance is sufficient. Return True on success."""
        return self.model.transfer_nomins(self, recipient, value)
    
    def escrow_curits(self, value:float) -> bool:
        """Escrow a positive value of curits in order to be able to issue nomins against them."""
        if self.curits >= value >= 0:
            self.curits -= value
            self.escrowed_curits += value
            self.model.escrowed_curits += value
            return True
        return False

    def available_escrowed_curits(self) -> float:
        """Return the quantity of escrowed curits which is not locked by issued nomins (may be negative)."""
        return self.escrowed_curits - self.model.nom_to_cur(self.issued_nomins)

    def unavailable_escrowed_curits(self) -> float:
        """Return the quantity of escrowed curits which is locked by having had nomins issued against it (may be greater than total escrowed curits)."""
        return self.model.nom_to_cur(self.issued_nomins)

    def unescrow_curits(self, value:float) -> bool:
        """Unescrow a quantity of curits, if there are not too many issued nomins locking it."""
        if 0 <= value <= available_escrowed_curits(value):
            self.curits += value
            self.escrowed_curits -= value
            return True
        return False

    def max_issuance_rights(self) -> float:
        """The total quantity of nomins this agent has a right to issue."""
        return self.model.cur_to_nom(self.escrowed_curits) * self.model.utilisation_ratio_max

    def issue_nomins(self, value:float) -> bool:
        """Issue a positive value of nomins against currently escrowed curits, up to the utilisation ratio maximum."""
        remaining = self.max_issuance_rights() - self.issued_nomins
        if 0 <= value <= remaining:
            self.issued_nomins += value
            self.nomins += value
            return True
        return False

    def burn_nomins(self, value:float) -> bool:
        """Burn a positive value of issued nomins, which frees up curits."""
        if 0 <= value <= self.nomins and value <= self.issued_nomins:
            self.nomins -= value
            self.issued_nomins -= value
            return True
        return False
    
    def sell_nomins_for_curits(self, quantity):
        price = self.model.nom_cur_market.lowest_ask()
        order = self.model.nom_cur_market.buy(quantity/price, self)
        self.orders.add(order)
        return order
    
    def sell_curits_for_nomins(self, quantity):
        order = self.model.nom_cur_market.sell(quantity, self)
        self.orders.add(order)
        return order

    def sell_fiat_for_curits(self, quantity):
        price = self.model.fiat_cur_market.lowest_ask()
        order = self.model.fiat_cur_market.buy(quantity/price, self)
        self.orders.add(order)
        return order
 
    def sell_curits_for_fiat(self, quantity):
        order = self.model.fiat_cur_market.sell(quantity, self)
        return order
 
    def sell_fiat_for_nomins(self, quantity):
        price = self.model.fiat_nom_market.lowest_ask()
        order = self.model.fiat_nom_market.buy(quantity/price, self)
        self.orders.add(order)
        return order

    def sell_nomins_for_fiat(self, quantity):
        order = self.model.fiat_nom_market.sell(quantity, self)
        self.orders.add(order)
        return order

    def notify_cancelled(self, order):
        pass

    def step(self) -> None:
        pass




"""
class RandomActor(model.MarketPlayer):
    # Actions: 
    #  * Transfer to another agent (fiat, nomins, curits)
    #  * buy/sell on the exchange
    #  * issue nomins
    #  * burn nomins 
    #  * (escrowing and unescrowing curits are just functions of issuing and burning nomins -- might need a state machine here)

    def can_transfer_fiat(self):
        pass

    def can_transfer_curits(self):
        pass
    
    def can_transfer_curits(self):
        pass

class Banker(model.MarketPlayer):
    Wants to buy curits and issue nomins, in order to accrue fees.

    def __init__(self):
        self.fiat_curit_order = self.sell_fiat_for_curits(0)
        self.nomin_curit_order = self.sell_nomins_for_curits(0)

    def step(self):
        if not self.fiat_curit_order.active:

        if self.fiat > 0:
            self.model.cur_fiat_market.sell
"""