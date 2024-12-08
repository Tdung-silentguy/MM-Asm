from policy import Policy
import numpy as np

class ProdObj:
    def __init__(self, insize, indemand):
        self.size = insize      # list of 2 int
        self.demand = indemand  # int
    def __init__(self, indict): # indict is dict
        self.size = indict["size"]
        self.demand = indict["quantity"]
    def __lt__(self, other):
        return (self.size[0] * self.size[1] < other.size[0] * other.size[1])

class StockObj:
    def __init__(self, instock, original_index): # instock is numpy array
        self.arr = instock
        self.height = np.sum(np.any(instock != -2, axis=0))
        self.width = np.sum(np.any(instock != -2, axis=1))
        self.rmarea = self.height * self.width
        self.used = False
        self.orgidx = original_index
    def __lt__(self, other):
        return (self.rmarea < other.rmarea)

class Policy2210xxx(Policy):
    used_stocks = list()    # used stocks are kept in ascending order
    unused_stocks = list()  # while unused stocks are kept in descending order
    
    first_iteration = True
    def __init__(self):
        # Student code here
        self.used_stocks = list()    # used stocks are kept in ascending order
        self.unused_stocks = list()  # while unused stocks are kept in descending order 
        self.first_iteration = True
    
    def reset(self):
        # Student code here
        self.used_stocks.clear()
        self.unused_stocks.clear()
        self.first_iteration = True
    
    def get_action(self, observation, info):
        # Student code here

        # PREPARING DATA

        # Preparing prods

        list_prods = list() # list of list_objs
        for prod in observation["products"]:    # for (dict) in (tuple of dicts)
            prod_obj = ProdObj(prod)
            list_prods.append(prod_obj)
        list_prods.sort(reverse=True)   # sort the prods in descending order

        prod_size = [0, 0]
        stock_idx = -1
        pos_x, pos_y = 0, 0

        # Preparing stocks
        if self.first_iteration == True:
            self.first_iteration = False
            for i, stock in enumerate(observation["stocks"]):
                stock_obj = StockObj(stock, i)
                self.unused_stocks.append(stock_obj)
            self.unused_stocks.sort(reverse = True) # sort unused stocks in descending order

        # ACTUAL PLACING PRODUCTS INTO STOCKS

        # Ensure product has demand > 0
        for prod in list_prods:
            if prod.demand > 0:
                prod_size = prod.size
                # Iterate through used stocks
                pos_x = None
                pos_y = None
                for stock in self.used_stocks:
                    stock_w = stock.width
                    stock_h = stock.height
                    prod_w, prod_h = prod.size
                    if stock_w >= prod_w and stock_h >= prod_h:
                        pos_x, pos_y = None, None
                        for x in range(stock_w - prod_w + 1):
                            for y in range(stock_h - prod_h + 1):
                                if self._can_place_(stock.arr, (x, y), prod_size):
                                    pos_x, pos_y = x, y
                                    break
                            if pos_x is not None and pos_y is not None:
                                break
                        if pos_x is None and pos_y is None:
                            for x in range(stock_w - prod_h + 1):
                                for y in range(stock_h - prod_w + 1):
                                    if self._can_place_(stock.arr, (x, y), prod_size[::-1]):
                                        prod_size = prod_size[::-1]
                                        pos_x, pos_y = x, y
                                        break
                                if pos_x is not None and pos_y is not None:
                                    break
                        if pos_x is not None and pos_y is not None:
                            stock_idx = stock.orgidx
                            stock.rmarea -= prod_w * prod_h
                            self.used_stocks.sort()
                            break
                if pos_x is not None and pos_y is not None:
                    # if stock is placed, stop
                    break
                else:
                    # if not, use a new stock, place the product into it and update rmarea
                    new_stock = self.unused_stocks.pop(0)
                    stock_idx = new_stock.orgidx
                    pos_x = 0
                    pos_y = 0
                    self.used_stocks.append(new_stock)
                    self.used_stocks.sort()

        return {"stock_idx": stock_idx, "size": prod_size, "position": (pos_x, pos_y)}
    # Student code here
    # You can add more functions if needed
