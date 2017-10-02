"""
Cookie Clicker Simulator
"""

import simpleplot
import math
# Used to increase the timeout, if necessary
import codeskulptor
codeskulptor.set_timeout(20)

import poc_clicker_provided as provided

# Constants
SIM_TIME = 10000000000.0
#SIM_TIME = 20

class ClickerState:
    """
    Simple class to keep track of the game state.
    """
    
    def __init__(self):
        self._total_cookies = 0.0
        self._curr_cookies = 0.0
        self._curr_time = 0.0
        self._curr_cps = 1.0

        self._history = [(0.0, None, 0.0, 0.0)]
        
    def __str__(self):
        """
        Return human readable state
        """
        return "Total time: " + str(self.get_time()) + "Total cookies: " + str(self._total_cookies) + "Current amount of cookies: " + str(self._curr_cookies) + "Current CPS: " + str(self._curr_cps)
        
    def get_cookies(self):
        """
        Return current number of cookies 
        (not total number of cookies)
        
        Should return a float
        """
        return self._curr_cookies
    
    def get_cps(self):
        """
        Get current CPS

        Should return a float
        """
        return self._curr_cps
    
    def get_time(self):
        """
        Get current time

        Should return a float
        """
        return self._curr_time
    
    def get_history(self):
        """
        Return history list

        History list should be a list of tuples of the form:
        (time, item, cost of item, total cookies)

        For example: [(0.0, None, 0.0, 0.0)]

        Should return a copy of any internal data structures,
        so that they will not be modified outside of the class.
        """
        return self._history[:]

    def time_until(self, cookies):
        """
        Return time until you have the given number of cookies
        (could be 0.0 if you already have enough cookies)

        Should return a float with no fractional part
        """
        return max(0.0, float(math.ceil((cookies-self._curr_cookies)/self._curr_cps)))
    
    def wait(self, time):
        """
        Wait for given amount of time and update state

        Should do nothing if time <= 0.0
        """
        if time <= 0:
            return
        self._curr_cookies += (self._curr_cps * time)
        self._total_cookies += (self._curr_cps * time)
        self._curr_time += time
    
    def buy_item(self, item_name, cost, additional_cps):
        """
        Buy an item and update state

        Should do nothing if you cannot afford the item
        """
        if self._curr_cookies >= cost:
            self._curr_cookies -= cost
            self._history.append((self.get_time(), item_name, cost, self._total_cookies))
            self._curr_cps += additional_cps
    
def simulate_clicker(build_info, duration, strategy):
    """
    Function to run a Cookie Clicker game for the given
    duration with the given strategy.  Returns a ClickerState
    object corresponding to the final state of the game.
    """
    build_info_new = build_info.clone()
    clicker_state = ClickerState()
    
    while True:
        time_left = duration - clicker_state.get_time()
        if time_left < 0:
            break
        item = strategy(clicker_state.get_cookies(), clicker_state.get_cps(), clicker_state.get_history(), time_left, build_info_new)
        if not item:
            # "You can't buy an item."
            clicker_state.wait(time_left)
            break
        cost = build_info_new.get_cost(item)
        # "You can buy an item"
        wait_time = clicker_state.time_until(cost)
        # "You have to wait."
        if wait_time > time_left:
            clicker_state.wait(time_left)
            # "No time left to buy things."
            break
        clicker_state.wait(wait_time)
        add_cps = build_info_new.get_cps(item)
        clicker_state.buy_item(item, cost, add_cps)
        build_info_new.update_item(item)
    return clicker_state

def strategy_cursor_broken(cookies, cps, history, time_left, build_info):
    """
    Always pick Cursor!

    Note that this simplistic (and broken) strategy does not properly
    check whether it can actually buy a Cursor in the time left.  Your
    simulate_clicker function must be able to deal with such broken
    strategies.  Further, your strategy functions must correctly check
    if you can buy the item in the time left and return None if you
    can't.
    """
    return "Cursor"

def strategy_none(cookies, cps, history, time_left, build_info):
    """
    Always return None

    This is a pointless strategy that will never buy anything, but
    that you can use to help debug your simulate_clicker function.
    """
    return None

def strategy_cheap(cookies, cps, history, time_left, build_info):
    """
    Always buy the cheapest item you can afford in the time left.
    """
    items = build_info.build_items()
    future_cookies = cookies + cps * time_left
    costs = [build_info.get_cost(dummy_item) for dummy_item in items]
    items_sort = sorted(zip(costs, items))
    for dummy_item in items_sort:
        if future_cookies >= dummy_item[0]:
            return dummy_item[1]
    return None

def strategy_expensive(cookies, cps, history, time_left, build_info):
    """
    Always buy the most expensive item you can afford in the time left.
    """
    items = build_info.build_items()
    future_cookies = cookies + cps * time_left
    costs = [build_info.get_cost(dummy_item) for dummy_item in items]
    items_sort = sorted(zip(costs, items), reverse=True)
    for dummy_item in items_sort:
        if future_cookies >= dummy_item[0]:
            return dummy_item[1]
    return None

 
def strategy_best(cookies, cps, history, time_left, build_info):
    """
    The best strategy that you are able to implement.
    """
    items = build_info.build_items()
    future_cookies = cookies + cps * time_left
    costs = [build_info.get_cost(dummy_item) for dummy_item in items]
    cps_list = [build_info.get_cps(dummy_item) for dummy_item in items]
    cps_rate = [cps_list[dummy_i]/costs[dummy_i] for dummy_i in range(len(items))]
    sorted_items = sorted(zip(cps_rate, items, costs), reverse=True)
    for dummy_item in sorted_items:
        if future_cookies >= dummy_item[2]:
            return dummy_item[1]
    return None
    
    
def run_strategy(strategy_name, time, strategy):
    """
    Run a simulation for the given time with one strategy.
    """
    state = simulate_clicker(provided.BuildInfo(), time, strategy)
    print strategy_name, ":", state

    # Plot total cookies over time

    # Uncomment out the lines below to see a plot of total cookies vs. time
    # Be sure to allow popups, if you do want to see it

    history = state.get_history()
    history = [(item[0], item[3]) for item in history]
    simpleplot.plot_lines(strategy_name, 1000, 400, 'Time', 'Total Cookies', [history], True)

def run():
    """
    Run the simulator.
    """    
    run_strategy("Cursor", SIM_TIME, strategy_cursor_broken)

    # Add calls to run_strategy to run additional strategies
    run_strategy("Cheap", SIM_TIME, strategy_cheap)
    run_strategy("Expensive", SIM_TIME, strategy_expensive)
    run_strategy("Best", SIM_TIME, strategy_best)
    
run()
    

