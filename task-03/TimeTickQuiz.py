# time_tick_quiz.py

import requests
import html
import random
import threading
import time

CATEGORY_URL = "https://opentdb.com/api_category.php"
QUESTION_URL = "https://opentdb.com/api.php"
TIME_LIMIT = 15  # seconds per question




# ------------------ api functionss ------------------

def fetch_categories():
    """
    fetches trivia categories from the API.
    """

    response = requests.get(CATEGORY_URL)
    data = response.json()
    categories = data['trivia_categories']
    for category in categories:
        print(f"ID:{category['id']} , Name:{category['name']}")

    pass

def fetch_questions(selected_category,selected_difficulty,selected_question_type,amount=10):
    params = {'amount':amount,'category':selected_category,'difficulty':selected_difficulty,'type':selected_question_type}
    response = requests.get(QUESTION_URL,params=params)
    questions = response.json()
    return questions

    """
    fetches the questions based on given filters.
    """
    pass

# ------------------ user input selection ------------------

def select_category():
    selected_category = input("Enter the category id:")
    return selected_category

    """
    prompts user to select a category from the list.
    """
    pass

def select_difficulty():
    selected_difficulty = input('Enter the difficulty(easy,medium,hard):')
    return selected_difficulty
    """
    prompst user to select question difficulty.
    """
    pass

def select_question_type():
    selected_question_type = input('Enter the question type(multiple/boolean):')
    return selected_question_type
    """
    prompts the user to select type of questions (multiple/boolean).
    """
    pass

# ------------------ quiz logicc ------------------

def ask_question(quest):
    
    print("\n Question:",html.unescape(quest['question']))     
    
    

    """
    presents a question to the user with a countdown timer.
    """
    pass

def select_quiz_options(quest):

    
    
    correct = html.unescape(quest['correct_answer'])
    incorrect  = []
    for ans in quest['incorrect_answers']:
        incorrect.append(html.unescape(ans))
    options = [correct] + incorrect
    
    random.shuffle(options)

    for idx,opt in enumerate(options,1):
        print(f"{idx}.{opt}")

    stop_timer_flag = [False]

    def countdown():
        for i in range(TIME_LIMIT, 0, -1):
            if stop_timer_flag[0]:
                break
            # print(f"Time left: {i} seconds", end="\r")
            time.sleep(1)
        if not stop_timer_flag[0]:
            print("\nTime's up!")

    timer_thread = threading.Thread(target=countdown)
    timer_thread.start()
    

    try:
        start_time = time.time()
        user_inp= input("Your answer(option number):")
        end_time = time.time()
        stop_timer_flag[0] = True

        if end_time - start_time >TIME_LIMIT:
            print("Sorry, time's up!!")
            timer_thread.join()
            return False
        
        inp_idx = int(user_inp) - 1
        if options[inp_idx] == correct:
            print("Correct! Moving to the next question...")
            timer_thread.join()
            return True
        else:
            print(f"Wrong! The correct answer was:{correct}")
            timer_thread.join()
            return False
    except (ValueError, IndexError):
        stop_timer_flag[0] = True
        print("Invalid input or time's up!!")
        timer_thread.join()
        return False




   
    
    """
    gathers all the quiz options and fetch questions accordingly.
    """
    pass

# ------------------ main fucntion ------------------

def main():
    score = 0
    print(". . . W E L C O M E   T O   T H E   T I M E   T I C K   Q U I Z . . .")
    time.sleep(3)
    fetch_categories()
    selected_category = select_category()
    selected_difficulty = select_difficulty()
    selected_question_type = select_question_type()
    questions = fetch_questions(selected_category,selected_difficulty,selected_question_type)
    for quest in questions['results']:
        ask_question(quest)
        if select_quiz_options(quest):
            score+=1

    print('-'*50)
    print(f"Final score:{score} out of 10")
       
    """
    Entry point for the TimeTickQuiz game.
    """
    pass

if __name__ == "__main__":
    main()

