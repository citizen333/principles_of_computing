"""
Cookie Clicker Simulator
"""
from poc.cookies import poc_clicker_provided as provided
import math
import matplotlib.pyplot as plt

# Constants
SIM_TIME = 10000000000.0


class ClickerState:
    """
    Simple class to keep track of the game state.
    """

    def __init__(self):
        self._total_cookies = 0.0
        self._current_cookies = 0.0
        self._current_time = 0.0
        self._current_cps = 1.0
        self._history = [(0.0, None, 0.0, 0.0)]

    def __str__(self):
        """
        Return human readable state
        """

        game_state = [
            "Total cookies baked is " + str(self._total_cookies),
            "Number of cookies currently available is " + str(self._current_cookies),
            "Current time is " + str(self._current_time),
            "Current CPS is " + str(self._current_cps)
        ]
        return "\n" + "\n".join(game_state)

    def get_cookies(self):
        """
        Return current number of cookies
        (not total number of cookies)

        Should return a float
        """
        return float(self._current_cookies)

    def get_cps(self):
        """
        Get current CPS

        Should return a float
        """
        return self._current_cps

    def get_time(self):
        """
        Get current time

        Should return a float
        """
        return float(self._current_time)

    def get_history(self):
        """
        Return history list

        History list should be a list of tuples of the form:
        (time, item, cost of item, total cookies)

        For example: [(0.0, None, 0.0, 0.0)]

        Should return a copy of any internal data structures,
        so that they will not be modified outside of the class.
        """
        return list(self._history)

    def time_until(self, cookies):
        """
        Return time until you have the given number of cookies
        (could be 0.0 if you already have enough cookies)

        Should return a float with no fractional part
        """
        time_until = math.ceil((cookies - self._current_cookies) / self._current_cps)
        return max(0.0, float(time_until))

    def wait(self, time):
        """
        Wait for given amount of time and update state

        Should do nothing if time <= 0.0
        """
        time = float(time)
        if time > 0.0:
            cookies_baked = time * self._current_cps
            self._total_cookies += cookies_baked
            self._current_cookies += cookies_baked
            self._current_time += time

    def buy_item(self, item_name, cost, additional_cps):
        """
        Buy an item and update state

        Should do nothing if you cannot afford the item
        """
        cost = float(cost)
        additional_cps = float(additional_cps)

        if cost < 0.0:
            return
        elif cost <= self._current_cookies:
            self._history.append((self._current_time, item_name, cost, self._total_cookies))
            self._current_cookies -= cost
            self._current_cps += additional_cps


def simulate_clicker(build_info, duration, strategy):
    """
    Function to run a Cookie Clicker game for the given
    duration with the given strategy.  Returns a ClickerState
    object corresponding to the final state of the game.
    """

    builder = build_info.clone()
    game_state = ClickerState()

    while game_state.get_time() <= duration:
        time_left = duration - game_state.get_time()
        strategy_item = strategy(game_state.get_cookies(), game_state.get_cps(),
                                 game_state.get_history(), time_left, builder)

        if strategy_item is None:
            break

        item_cost = builder.get_cost(strategy_item)

        if game_state.time_until(item_cost) > time_left:
            break
        else:
            game_state.wait(game_state.time_until(item_cost))
            game_state.buy_item(strategy_item, builder.get_cost(strategy_item),
                                builder.get_cps(strategy_item))
            builder.update_item(strategy_item)

    game_state.wait(duration - game_state.get_time())
    return game_state


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
    selected_item = build_info.build_items()[0]
    for item in build_info.build_items():
        if build_info.get_cost(item) < build_info.get_cost(selected_item):
            selected_item = item

    if (build_info.get_cost(selected_item) / cps > time_left
            and build_info.get_cost(selected_item) > cookies):
        return None
    else:
        return selected_item


def strategy_expensive(cookies, cps, history, time_left, build_info):
    """
    Always buy the most expensive item you can afford in the time left.
    """
    selected_item_by_time = None
    selected_item_by_cost = None
    for item in build_info.build_items():

        if build_info.get_cost(item) / cps > time_left:
            pass
        elif selected_item_by_time is None:
            selected_item_by_time = item
        elif build_info.get_cost(item) > build_info.get_cost(selected_item_by_time):
            selected_item_by_time = item

        if build_info.get_cost(item) > cookies:
            pass
        elif selected_item_by_cost is None:
            selected_item_by_cost = item
        elif build_info.get_cost(item) > build_info.get_cost(selected_item_by_cost):
            selected_item_by_cost = item

    if selected_item_by_time is None:
        return selected_item_by_cost
    elif selected_item_by_cost is None:
        return selected_item_by_time
    elif build_info.get_cost(selected_item_by_cost) >= build_info.get_cost(selected_item_by_time):
        return selected_item_by_cost
    elif build_info.get_cost(selected_item_by_time) >= build_info.get_cost(selected_item_by_cost):
        return selected_item_by_time


def strategy_best(cookies, cps, history, time_left, build_info):
    """
    The best strategy that you are able to implement.
    """
    metrics_dict = dict()
    for item in build_info.build_items():
        if (build_info.get_cost(item) / cps <= time_left
                or build_info.get_cost(item) >= cookies):
            metrics_dict[item] = ((build_info.get_cost(item)
                                  * math.log(1 + build_info.get_cost(item)))
                                  / build_info.get_cps(item))

    if len(metrics_dict.keys()) == 0:
        return None
    else:
        return min(metrics_dict, key=metrics_dict.get)




def run_strategy(strategy_name, time, strategy):
    """
    Run a simulation for the given time with one strategy.
    """
    state = simulate_clicker(provided.BuildInfo(), time, strategy)
    print(strategy_name, ":", state)

    # Plot total cookies over time

    # Uncomment out the lines below to see a plot of total cookies vs. time
    # Be sure to allow popups, if you do want to see it

    history = state.get_history()
    history = [(math.log(1 + item[0]), math.log(1 + item[3])) for item in history]
    # simpleplot.plot_lines(strategy_name, 1000, 400, 'Time', 'Total Cookies', [history], True)
    assert isinstance(strategy_name, str)
    plt.plot(*zip(*history), label=strategy_name)


def run():
    """
    Run the simulator.
    """
    run_strategy("Cursor", SIM_TIME, strategy_cursor_broken)
    run_strategy("Cheap", SIM_TIME, strategy_cheap)
    run_strategy("Expensive", SIM_TIME, strategy_expensive)
    run_strategy("Best", SIM_TIME, strategy_best)
    plt.xlabel('Time')
    plt.ylabel('Total Cookies')
    plt.title('Cookie Clicker')
    plt.legend()
    plt.show()


# run()
# strategy_expensive(500000.0, 1.0, [(0.0, None, 0.0, 0.0)], 5.0, provided.BuildInfo({'A': [5.0, 1.0], 'C': [50000.0, 3.0], 'B': [500.0, 2.0]}, 1.15))
