"""
Planner for Yahtzee
Simplifications:  only allow discard and roll, only score against upper level
"""

# Used to increase the timeout, if necessary
# import codeskulptor
import random

# codeskulptor.set_timeout(20)


def gen_all_sequences(outcomes, length):
    """
    Iterative function that enumerates the set of all sequences of
    outcomes of given length.
    """

    answer_set = set([()])
    for dummy_idx in range(length):
        temp_set = set()
        for partial_sequence in answer_set:
            for item in outcomes:
                new_sequence = list(partial_sequence)
                new_sequence.append(item)
                temp_set.add(tuple(new_sequence))
        answer_set = temp_set
    return answer_set


def score(hand):
    """
    Compute the maximal score for a Yahtzee hand according to the
    upper section of the Yahtzee score card.

    hand: full yahtzee hand

    Returns an integer score
    """

    score_dict = dict()
    for dice_result in hand:
        score_dict.setdefault(dice_result, 0)
        score_dict[dice_result] += dice_result

    return max(score_dict.values())


def expected_value(held_dice, num_die_sides, num_free_dice):
    """
    Compute the expected value based on held_dice given that there
    are num_free_dice to be rolled, each with num_die_sides.

    held_dice: dice that you will hold
    num_die_sides: number of sides on each die
    num_free_dice: number of dice to be rolled

    Returns a floating point expected value
    """

    free_outcomes = gen_all_sequences(range(1, num_die_sides + 1), num_free_dice)
    score_list = list()
    for outcome in free_outcomes:
        hand_outcome = list()
        hand_outcome.extend(held_dice)
        hand_outcome.extend(outcome)
        score_list.append(score(tuple(hand_outcome)))

    return float(sum(score_list) / len(score_list))


def gen_all_holds(hand):
    """
    Generate all possible choices of dice from hand to hold.

    hand: full yahtzee hand

    Returns a set of tuples, where each tuple is dice to hold
    """

    hand_indxs = tuple(range(len(hand)))
    idx_set = set([()])
    for dummy_idx in range(len(hand)):
        temp_set = set()
        for partial_sequence in idx_set:
            for item in hand_indxs:
                if item not in partial_sequence:
                    new_sequence = set(partial_sequence)
                    new_sequence.add(item)
                    temp_set.add(tuple(new_sequence))
        idx_set.update(temp_set)

    answer_set = set()
    for idxs in idx_set:
        hand_tuple = tuple([hand[idx] for idx in idxs])
        answer_set.add(hand_tuple)

    return answer_set


def strategy(hand, num_die_sides):
    """
    Compute the hold that maximizes the expected value when the
    discarded dice are rolled.

    hand: full yahtzee hand
    num_die_sides: number of sides on each die

    Returns a tuple where the first element is the expected score and
    the second element is a tuple of the dice to hold
    """
    hands_to_hold = gen_all_holds(hand)
    hands_expectations = list()
    for hand_to_hold in hands_to_hold:
        num_free_dice = len(hand) - len(hand_to_hold)
        hands_expectations.append(expected_value(hand_to_hold, num_die_sides, num_free_dice))

    max_expectation = max(hands_expectations)
    hands_expectations_dict = dict(zip(hands_to_hold, hands_expectations))
    max_expectation_hands = [key for key, val in hands_expectations_dict.items()
                             if val == max_expectation]

    strategy_hand = random.choice(max_expectation_hands)
    strategy_value = hands_expectations_dict[strategy_hand]
    return tuple([strategy_value, strategy_hand])


def run_example():
    """
    Compute the dice to hold and expected score for an example hand
    """
    num_die_sides = 6
    hand = (1, 1, 1, 5, 6)
    hand_score, hold = strategy(hand, num_die_sides)
    print("Best strategy for hand", hand, "is to hold", hold, "with expected score", hand_score)


run_example()

# import poc_holds_testsuite
# poc_holds_testsuite.run_suite(gen_all_holds)