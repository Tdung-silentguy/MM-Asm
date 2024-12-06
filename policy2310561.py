from policy import Policy

class ProdObj:
    size = [0,0]    # list of 2
    demand = 0      # int
    def __init__(self, insize, indemand):
        self.size = insize
        self.demand = indemand
    def __init__(self, indict): # indict is dict
        self.size = indict["size"]
        self.demand = indict["quantity"]
    def __lt__(self, other):
        return (self.size[0] * self.size[1] < other.size[0] * other.size[1])

class Policy2310561(Policy):
    def __init__(self):
        # Student code here
        pass

    def get_action(self, observation, info):
        # Student code here
        aux_list = observation["products"]  # tuple of dicts
        
        # Sort the products in ascending order by area
        list_prods = list()  # list of ProdObj
        for prod in aux_list:
            #prod is tuple
            prod_obj = ProdObj(prod)
            list_prods.append(prod_obj)
        list_prods.sort(reverse=True)
    
        prod_size = [0, 0]
        stock_idx = -1
        pos_x, pos_y = None, None
    
        # Pick a product that has demand > 0
        for prod in list_prods:
            if prod.demand > 0:
                prod_size = prod.size
    
                # Loop through all stocks (this will be changed to using a StockObj class; the algorithm will try to use ordered_used_stocks before getting a new stock.)
                for i, stock in enumerate(observation["stocks"]):
                    stock_w, stock_h = self._get_stock_size_(stock)
                    prod_w, prod_h = prod_size
    
                    # Check both original and rotated sizes
                    possible_orientations = [(prod_w, prod_h), (prod_h, prod_w)]

                    for orientation in possible_orientations:
                        prod_w, prod_h = orientation #prod_w and _h can now be either orientation
    
                        if stock_w < prod_w or stock_h < prod_h:
                            continue
    
                        pos_x, pos_y = None, None
                        for x in range(stock_w - prod_w + 1):
                            for y in range(stock_h - prod_h + 1):
                                if self._can_place_(stock, (x, y), (prod_w, prod_h)):
                                    #valid position found
                                    pos_x, pos_y = x, y #place in either orientation
                                    stock_idx = i
                                    prod_size = [prod_w, prod_h] #update prod_size
                                    break
                            if pos_x is not None and pos_y is not None:
                                break
    
                        if pos_x is not None and pos_y is not None:
                            break
    
                    if pos_x is not None and pos_y is not None:
                        break
    
            if pos_x is not None and pos_y is not None:
                break
    
        return {"stock_idx": stock_idx, "size": prod_size, "position": (pos_x, pos_y)}



    # Student code here
    # You can add more functions if needed
