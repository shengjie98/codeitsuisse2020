import logging
import json

from flask import request, jsonify;

from codeitsuisse import app;

logger = logging.getLogger(__name__)

@app.route('/olympiad-of-babylon', methods=['POST'])
def evaluate_baby():
    data = request.get_json()
    logging.info("data sent for evaluation {}".format(data))
    numberOfBooks = data.get("numberOfBooks")
    numberOfDays = data.get("numberOfDays")
    books = data.get("books")
    days = data.get("days")
    max_ = baby(numberOfBooks, numberOfDays, books, days)
    result = {"optimalNumberOfBooks": max_[-1]}
    logging.info("My result :{}".format(result))
    return jsonify(result)

def baby(numberOfBooks, numberOfDays, books, days):
    books.sort()
    days.sort()
    sets = [] # where sets[i] will the set of weights that has i books or less
    weights = set()
    weights.add(tuple(0 for _ in range(numberOfDays + 1)))
    sets.append(weights)
    print(weights)
    for i in range(numberOfBooks):
        new_set = { tuple([bag_weight if k!=j else bag_weight + books[i] for k, bag_weight in enumerate(weight[:-1])] + [weight[-1] + 1]) for j in range(numberOfDays) for weight in sets[i]}
        new_set = {*filter(lambda tupleOfWeights: checkCapacity(tupleOfWeights, days), new_set)}
        sets.append(new_set)
        # print(new_set)
    sets = [*filter(lambda x: x, sets)]
    max_ = max(sets[-1], key=lambda x: x[-1])
    return max_
        


def checkCapacity(tupleOfWeights, days):
    for i in range(len(days)):
        if tupleOfWeights[i] > days[i]:
            return False
    return True

def tuple_subtraction(tuple1, tuple2):
    return (tuple1[i] - tuple2[i] for i in range(len(tuple1) - 1))


# def baby(books_left, time_left_per_day):
#     # return (number of books, book arrangement)
#     # dont put book i in  any day
#     # for each day, put book i in the day and minus the remaining time in the day
#     potential_arrangements = []
#     if len(books_left) == 1:
#         book = books_left[0]
#         for i, time in enumerate(time_left_per_day):
#             if book < time:
#                 potential_arrangements.append([i])
#             else:
#                 break
#         if potential_arrangements:
#             return potential_arrangements
#         return [[-1]]

#     book = books_left.pop(0)
#     # dont put book i in any day
#     no_book_i = [[-1] + potential_arrangement for potential_arrangement in baby(books_left.copy(), time_left_per_day)]
#     potential_arrangements.extend(no_book_i)
    
#     for i, time in enumerate(time_left_per_day):
#         if book < time:
#             with_book_i = [[i] + potential_arrangement for potential_arrangement in baby(books_left.copy(), [time_left if j!= i else time_left - book for j, time_left in enumerate(time_left_per_day)])]
#             potential_arrangements.extend(with_book_i)
#         else: 
#             break
#     if potential_arrangements:
#         max_ = len(max(potential_arrangements, key=lambda potential_arrangement: len([x for x in potential_arrangement if x >=0 ])))
#         potential_arrangements = list(filter(lambda potential_arrangement: len([x for x in potential_arrangement if x >=0 ]) == max_, potential_arrangements))
#         return potential_arrangements
#     else:
#         return []
