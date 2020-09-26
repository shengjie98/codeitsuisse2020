import logging
import json

from flask import request, jsonify;

from codeitsuisse import app;

logger = logging.getLogger(__name__)

@app.route('/olympiad-of-babylon', methods=['POST'])
def evaluate_baby():
    data = request.get_json()
    logging.info("data sent for evaluation {}".format(data))
    books = data.get("books")
    days = data.get("days")
    books.sort()
    days.sort(reverse = True)
    
    potential = baby(books, days)
    numBooks = len([x for x in potential[0] if x>=0])
    result = {"optimalNumberOfBooks": numBooks}
    logging.info("My result :{}".format(result))
    return jsonify(result)

def baby(books_left, time_left_per_day):
    # return (number of books, book arrangement)
    # dont put book i in  any day
    # for each day, put book i in the day and minus the remaining time in the day
    potential_arrangements = []
    if len(books_left) == 1:
        book = books_left[0]
        for i, time in enumerate(time_left_per_day):
            if book < time:
                potential_arrangements.append([i])
            else:
                break
        if potential_arrangements:
            return potential_arrangements
        return [[-1]]

    book = books_left.pop(0)
    # dont put book i in any day
    no_book_i = [[-1] + potential_arrangement for potential_arrangement in baby(books_left.copy(), time_left_per_day)]
    potential_arrangements.extend(no_book_i)
    
    for i, time in enumerate(time_left_per_day):
        if book < time:
            with_book_i = [[i] + potential_arrangement for potential_arrangement in baby(books_left.copy(), [time_left if j!= i else time_left - book for j, time_left in enumerate(time_left_per_day)])]
            potential_arrangements.extend(with_book_i)
        else: 
            break
    if potential_arrangements:
        max_ = len(max(potential_arrangements, key=lambda potential_arrangement: len([x for x in potential_arrangement if x >=0 ])))
        potential_arrangements = list(filter(lambda potential_arrangement: len([x for x in potential_arrangement if x >=0 ]) == max_, potential_arrangements))
        return potential_arrangements
    else:
        return []
