from kivy.uix.accordion import StringProperty
import random
import numpy as np
import kivy
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.spinner import Spinner
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup
from kivy.uix.slider import Slider
from kivy.uix.progressbar import ProgressBar
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty, StringProperty

from logic.declension_logic import load_table, TableName, Gender, Case, check_declension

def show_popup(title, message, label_text_y_pos: int = 0.6):
    popup_layout = FloatLayout(size_hint=(1, 1))
    popup_label = Label(text = message, pos_hint = {"x": 0.1, "y": label_text_y_pos}, size_hint = (0.8, 0.4), halign = 'center')
    popup_label.bind(size = lambda s, w: s.setter('text_size')(s, w))
    close_button = Button(text = "Close", size_hint = (1, None), pos_hint = {"x": 0.0, "y": 0.1}, height = 50)
    popup_layout.add_widget(popup_label)
    popup_layout.add_widget(close_button)

    popup = Popup(title = title, content = popup_layout, size_hint = (0.4, 0.4),  title_align = 'center')
    close_button.bind(on_press = popup.dismiss)
    popup.open()


class MyScreenManager(ScreenManager):
    def __init__(self, **kwargs):
        super(MyScreenManager, self).__init__(**kwargs)

    def open_quizz_screen(self):
        # Assume the spinner is called 'table_spinner' and is a child of the current screen
        table_spinner = self.get_screen('main_menu').ids.table_spinner

        # Check if a table is selected (assuming the default text is 'Select Table')
        if table_spinner.text == 'Select Table' or not table_spinner.text:
            # If no table is selected, show a popup warning
            popup = Popup(
                title='Warning',
                size_hint=(0.6, 0.3),
                auto_dismiss=True,
                content=Label(text='Please select a table before proceeding.')
            )
            popup.open()

        else:
            self.current = 'quizz'

    

class MainMenuScreen(Screen):
    pass


class TableChoice(Spinner):
    def __init__(self, **kwargs):
        super(TableChoice, self).__init__(**kwargs)
        self.text = 'Select Table'
        self.values = [table.value for table in TableName]

        # Bind the font_size to the size of the widget
        #self.bind(size=self.update_font_size)
    
    def update_font_size(self, *args):
        # Adjust the font size based on the widget's height (or width, depending on your needs)
        self.font_size = self.height * 0.5  # Example: 50% of the widget's height


class QuizzScreen(Screen):
    answer_input = ObjectProperty(None)  # Reference to the TextInput widget in the kv file
    question_text = StringProperty() # Label text in kv file is bound to self.question_text now

    def __init__(self, **kwargs):
        super(QuizzScreen, self).__init__(**kwargs)
        self.layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        self.add_widget(self.layout)


    def on_enter(self):
        # This method is called whenever the screen is about to be displayed
        self.correct_answers = []
        self.score = None
        self.start_quizz()


    def start_quizz(self):
        table_name = TableName(self.manager.get_screen("main_menu").ids.table_spinner.text)
        # To adapt with a selector
        num_questions = 10

        # Load the selected table
        self.table = load_table(table_name)
        self.table_name = table_name

        # Generate random questions
        self.setup_quiz(self.table, num_questions)
        try:
            # Load the selected table
            self.table = load_table(table_name)
            self.table_name = table_name.value

            # Generate random questions
            self.setup_quiz(self.table, num_questions)
            
        except Exception as e:
            show_popup("Error", str(e))


    def setup_quiz(self, table, num_questions):
        self.table = table
        self.num_questions = num_questions
        self.current_question_index = 0
        self.questions = self.generate_questions(num_questions)

        self.show_question()


    def generate_questions(self, num_questions):
        genders = list(Gender)
        cases = list(Case)
        questions = []

        for _ in range(num_questions):
            gender = random.choice(genders)
            case = random.choice(cases)
            questions.append((gender, case))

        return questions


    def show_question(self):
        if self.current_question_index < len(self.questions):
            self.layout.clear_widgets()
            gender, case = self.questions[self.current_question_index]
            self.question_text = self.generate_question_text(gender, case)

        else:
            self.finish_quizz()


    def generate_question_text(self, gender, case):
        return f"What is the correct form of the {self.table_name} for a {gender.value} noun in the {case.value} case?"


    def check_answer(self):
        gender, case = self.questions[self.current_question_index]
        #user_answer = self.answer_input.text
        user_answer = self.ids.answer_input.text

        is_correct = check_declension(self.table, gender, case, user_answer)
        self.correct_answers.append(is_correct)
        if is_correct:
            show_popup("Correct", f"Correct!\n The {case.value} form of the {self.table_name}" 
                    + f" for a {gender.value} noun in the {case.value} case is {user_answer}.")
        else:
            correct_answer = self.table.loc[case.value, gender.value]
            show_popup("Incorrect", f"Incorrect.\n The correct answer was {correct_answer}.")

        self.current_question_index += 1
        #Clear answer field
        self.ids.answer_input.text = ""
        self.show_question()


    def compute_score(self):
        accuracy = np.mean(self.correct_answers)
        return accuracy
    

    def finish_quizz(self):
        text_label = 'Coming back to main menu'
        score = self.compute_score()

        if not np.isnan(score):
            text_label = 'You got a {:.2%} accuracy at this Quizz! '.format(score) + text_label 

        popup = Popup(
                title = 'End of Quizz',
                size_hint = (0.6, 0.2),
                auto_dismiss = True,
                content = Label(text = text_label ),
                on_dismiss = self.return_to_main_menu
            )
        popup.open()

  
    def return_to_main_menu(self, instance):
        self.manager.current = "main_menu"

class GermanLearnerApp(App):
    def build(self):
        self.title = "German Declension Trainer"

        # Screen Manager
        self.screen_manager = MyScreenManager()
        return self.screen_manager
    

if __name__ == "__main__":
    app = GermanLearnerApp()
    app.run()

