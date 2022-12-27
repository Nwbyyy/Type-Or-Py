from PIL import ImageGrab #To take a screenshot to get question
import pytesseract #To interpret text on screen
import csv #To import csv dictionary
import pyautogui #To type in the answer
import pydirectinput #To submit the answer
from pynput import keyboard #To detect keypress
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe' #To locat pytesseract

def create_csv_dict(file_name):
    with open(file_name, mode='r') as infile:
        reader = csv.reader(infile)
        answers_dict = {rows[0]:rows[1] for rows in reader}
    return answers_dict


def get_question():
    question_image = ImageGrab.grab(bbox=(562,31,1356,100))
    question_text = pytesseract.image_to_string(question_image)
    return question_text[0:(len(question_text) - 1)]


def type_answer(answer):
    print(answer)
    pyautogui.write(answer, 0.05)
    pydirectinput.press('enter')

def get_answer():  
    answers_dict = create_csv_dict('q&a.csv')
    question = get_question()
    if question in answers_dict or (question[0:7] in "NAME A " and question[7:] in answers_dict):
        if question[0:7] in "NAME A " and question[7:] in answers_dict:
            type_answer(answers_dict[question[7:]])
        else:
            type_answer(answers_dict[question])
    else:
        print("No answer for the question: " + question )
        with open('missing_questions.txt', 'a') as file:
            file.write(question + "\n")
        print(question + " has been added to the list of missing questions.")


def on_press(key):
    if key == keyboard.Key.esc:
        return False  
    try:
        k = key.char 
    except:
        k = key.name  
    if k in ['f8']: 
        print("Getting answer...")
        get_answer()

listener = keyboard.Listener(on_press)
listener.start()
listener.join()