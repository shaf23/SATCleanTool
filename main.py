from erasers import Eraser
import pyautogui
import pyperclip
import time

header_annotation = open("HeaderBlock.txt", "r")
continue_annotation = open("ContinueBlock.txt", "r")

heading = Eraser("HeaderImage.png", 0.85, header_annotation.read(), (725, 150))
question = Eraser("QuestionMarking.png", 0.8, None, None)
bottom = Eraser("ContinueImage.png", 0.9, continue_annotation.read(), (725, 1001))

header_annotation.close()
continue_annotation.close()


def erase(is_header_or_bottom, image, confidence, annotation, coordinates):
    if is_header_or_bottom:
        pyperclip.copy(annotation)

        if pyautogui.locateOnScreen("SelectAnnotationButton.png", confidence=0.7) is None:
            pyautogui.click(20, 120)
            time.sleep(0.5)
            pyautogui.click(72, 220)

        pyautogui.hotkey("ctrl", "v")
        pyautogui.moveTo(820, 545, 0.2)
        pyautogui.dragTo(coordinates[0], coordinates[1], 0.5, button="left")
    else:
        x, y = pyautogui.locateCenterOnScreen(image, confidence=confidence)

        if pyautogui.locateOnScreen("InsertLineButton.png", confidence=0.7) is None:
            pyautogui.click(24, 533)
            time.sleep(0.5)

        pyautogui.moveTo((x - 130), (y + 1), 0.3)
        pyautogui.drag(310, None, 0.5, button="left")


is_ready = input('---------------------------------------[SAT Cleaner]---------------------------------------\n'
                 'For full instructions read the README.md file\n'
                 'Configure your shape setting to a white line at 12 px stroke thickness in\nKami '
                 'and set the zoom option to "Fit Page" before proceeding\n'
                 'If for any reason you need the program to stop, drag your mouse to the top right corner\n'
                 'Lastly, make sure to not cover the SAT tab at all\n'
                 'Press [ENTER] to continue')


def format_time(seconds):
    minutes = seconds / 60
    glut_seconds = abs((minutes - round(minutes)) * 60)

    if seconds < 60:
        return str(round(seconds)) + " seconds"
    else:
        return str(round(minutes)) + " minute(s) and " + str(round(glut_seconds)) + " second(s)"


time.sleep(3)
start = time.time()

while (pyautogui.locateOnScreen(heading.image, confidence=heading.confidence) is not None
       or pyautogui.locateOnScreen(question.image, confidence=question.confidence) is not None
       or pyautogui.locateOnScreen(bottom.image, confidence=bottom.confidence) is not None):

    if pyautogui.locateOnScreen(question.image, confidence=question.confidence) is not None:
        while pyautogui.locateOnScreen(question.image, confidence=question.confidence) is not None:
            erase(False, question.image, question.confidence, None, None)
    else:
        erase(True, None, None, heading.notation, heading.coordinates)
        erase(True, None, None, bottom.notation, bottom.coordinates)
        pyautogui.hotkey("right")
        if pyautogui.locateOnScreen(question.image, confidence=question.confidence) is None:
            break
        else:
            continue
    if pyautogui.locateOnScreen(heading.image, confidence=heading.confidence) is not None:
        erase(True, None, None, heading.notation, heading.coordinates)
    if pyautogui.locateOnScreen(bottom.image, confidence=bottom.confidence) is not None:
        erase(True, None, None, bottom.notation, bottom.coordinates)

    pyautogui.hotkey("right")

stop = time.time()
print("\nOperation completed.\n"
      "Time Elapsed: " + format_time(stop-start))
input("Press [ENTER] to close the program")
