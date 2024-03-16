from jsonpickle import json
from datamodel import OrderDepth, TradingState, Order
from typing import List
import numpy as np

TraderData = dict[int, dict[str, float]]


class Trader:
  

    def compute_mid_price(self, order_depth: OrderDepth):
        buys_prices = list(order_depth.buy_orders.keys())
        buys_quantities = list(order_depth.buy_orders.values())

        sell_prices = list(order_depth.sell_orders.keys())
        sell_quantities = list(map(abs, list(order_depth.sell_orders.values())))

        average_buy_price = float(np.average(buys_prices, weights=buys_quantities,))
        average_sell_price = float(np.average(sell_prices, weights=sell_quantities))
        return { 
            "buy" : round(average_buy_price, 3),
            "sell": round(average_sell_price,3)
        }

                
    

      
    def run(self, state: TradingState):

        if state.traderData != None and state.traderData != "":
            trader_data = json.loads(state.traderData)
        else:
            trader_data = {}

        if "n" in trader_data.keys():
            trader_data["n-1"] = trader_data["n"]
        trader_data["n"]= {}
        result = {}
        for product in state.order_depths:
            if product not in state.position:
                state.position[product] = 0

            order_depth: OrderDepth = state.order_depths[product]
            trader_data["n"][product] = self.compute_mid_price(order_depth)
      # Initialize the list of Orders to be sent as an empty list
        orders: List[Order] = []
      # Define a fair value for the PRODUCT. Might be different for each tradable item
      # Note that this value of 10 is just a dummy value, you should likely change it!
        acceptable_price = 10
      # All print statements output will be delivered inside test results

      # Order depth list come already sorted.
      # We can simply pick first item to check first item to get best bid or offer
        if len(order_depth.sell_orders) != 0:
         best_ask, best_ask_amount = list(order_depth.sell_orders.items())[0]
        # if int(best_ask) < acceptable_price:
        # In case the lowest ask is lower than our fair value,
        # This presents an opportunity for us to buy cheaply
        # The code below therefore sends a BUY order at the price level of the ask,
        # with the same quantity
        # We expect this order to trade with the sell order
         ask_amount = 10 - state.position[product]
        # orders.append(Order(product, best_ask, ask_amount))

        if len(order_depth.buy_orders) != 0:
            best_bid, best_bid_amount = list(order_depth.buy_orders.items())[0]
        # if int(best_bid) > acceptable_price:
        # Similar situation with sell orders
            bid_amount = 10 + state.position[product]
        # orders.append(Order(product, best_bid, -bid_amount))

      # result[product] = orders
        

    # String value holding Trader state data required.
    # It will be delivered as TradingState.traderData on next execution.

    # Sample conversion request. Check more details below.
        print(trader_data)
        conversions = 1
        return result, conversions, json.dumps(trader_data)
