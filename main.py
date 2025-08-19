# Standard library imports
import calendar
from calendar import monthrange
from datetime import date, datetime, timedelta
from dateutil.relativedelta import relativedelta
from io import BytesIO
import json
import os
import random
import webbrowser
from pathlib import Path

# Kivy imports
from kivy.app import App
from kivy.core.image import Image as CoreImage
from kivy.core.window import Window
from kivy.metrics import dp
from kivy.resources import resource_find
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.scrollview import ScrollView
from kivy.uix.screenmanager import Screen, ScreenManager, SlideTransition
from kivy.uix.spinner import Spinner
from kivy.uix.textinput import TextInput
from kivy.uix.widget import Widget

# Custom imports
from storage import load_user_data, save_user_data  # Your JSON storage handlers

# Force working directory to this script's folder
os.chdir(os.path.dirname(os.path.abspath(__file__)))


IMAGE_FOLDER = "images"

motivational_messages = [
    "One day at a time. You’re doing great.",
    "Each clean day is a new beginning.",
    "You're proof that recovery is possible.",
    "You are stronger than your past.",
    "Healing is happening — trust the process.",
    "Every clean day adds strength to your soul.",
    "Every moment clean is a moment won.",
    "Your journey is inspiring, keep moving forward.",
    "You’ve come too far to go back now. Eyes forward.",
    "You don’t need to be perfect — just show up and keep going.",
    "Every day you stay clean is a middle finger to your past.",
    "It’s not about being clean forever. Just today. Win today.",
    "Some people collect stamps — you collect clean days and life lessons.",
    "Sobriety’s wild… suddenly you remember birthdays, appointments, and where your phone is."
]

def calculate_days_clean(clean_date_str):
    try:
        clean_date = datetime.strptime(clean_date_str, "%Y-%m-%d").date()
        today = datetime.today().date()
        return (today - clean_date).days
    except:
        return 0

def get_random_image():
    if not os.path.exists(IMAGE_FOLDER):
        return None
    images = [f for f in os.listdir(IMAGE_FOLDER) if f.endswith(".png")]
    if not images:
        return None
    return os.path.join(IMAGE_FOLDER, random.choice(images))


class WelcomeScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        layout = FloatLayout()

        # Welcome Message near the top
        welcome_label = Label(
            text=("Welcome!\n\n"
                  "You’ve taken the first step toward healing, and that’s no small thing.\n\n"
                  "Whether this is day one or day one hundred, your commitment to change is a sign of strength — not weakness.\n\n"
                  "This journey isn’t easy, but you’re not alone. Every clean day is a win. Every moment is a victory. "
                  "This app is here to walk with you, one step at a time."),
            halign="center",
            valign="top",
            font_size=24,
            size_hint=(0.9, None),
            height=Window.height * 0.5,
            pos_hint={"center_x": 0.5, "top": 0.95},
            text_size=(Window.width * 0.9, None)
        )
        layout.add_widget(welcome_label)

        # Serenity Prayer around 3/4 down
        serenity_label = Label(
            text=("[i]God, grant me the serenity\n"
                  "to accept the things I cannot change,\n"
                  "courage to change the things I can,\n"
                  "and wisdom to know the difference.[/i]"),
            halign="center",
            valign="middle",
            font_size=22,
            size_hint=(0.9, None),
            height=150,
            pos_hint={"center_x": 0.5, "top": 0.3},
            text_size=(Window.width * 0.9, None),
            markup=True
        )
        layout.add_widget(serenity_label)

        # Transparent Get Started button at the bottom
        get_started_btn = Button(
            text="Get Started",
            size_hint=(0.6, None),
            height=50,
            pos_hint={"center_x": 0.5, "y": 0.05},
            background_normal='',  # This makes the button background transparent
            background_color=(0, 0, 0, 0),  # Fully transparent background
            color=(0.1, 0.5, 0.8, 1),  # Text color (blue-ish)
            font_size=20,
            bold=True,
        )
        get_started_btn.bind(on_press=self.go_to_setup)
        layout.add_widget(get_started_btn)

        self.add_widget(layout)

    def go_to_setup(self, instance):
        self.manager.current = "setup"


class SetupScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.form_layout = BoxLayout(orientation='vertical', padding=30, spacing=20, size_hint=(None, None))
        self.form_layout.width = 400
        self.form_layout.height = 400

        title_label = Label(
            text="Please Enter Your Info:",
            font_size=28,
            size_hint=(None, None),
            size=(280, 50))
        title_anchor = AnchorLayout(anchor_x='center')
        title_anchor.add_widget(title_label)
        self.form_layout.add_widget(title_anchor)

        self.entered_name = ""
        self.name_input = Button(
            text="Enter Your Name", 
            size_hint=(None, None), 
            size=(280, 60), 
            font_size=22)
        self.name_input.bind(on_release=self.open_name_input)
        name_anchor = AnchorLayout(anchor_x='center')
        name_anchor.add_widget(self.name_input)
        self.form_layout.add_widget(name_anchor)

        # Add label above date spinners
        clean_date_label = Label(
            text="Please enter your clean date:",
            font_size=22,
            size_hint=(None, None),
            size=(280, 40))
        clean_date_anchor = AnchorLayout(anchor_x='center')
        clean_date_anchor.add_widget(clean_date_label)
        self.form_layout.add_widget(clean_date_anchor)

        self.year_spinner = Spinner(
            text='Year',
            values=[str(year) for year in range(datetime.now().year, 1979, -1)],
            size_hint=(None, None),
            size=(100, 60),
            font_size=22)
        self.month_spinner = Spinner(
            text='Month',
            values=[str(m) for m in range(1, 13)],
            size_hint=(None, None),
            size=(80, 60),
            font_size=22)
        self.day_spinner = Spinner(
            text='Day',
            values=[str(d) for d in range(1, 32)],
            size_hint=(None, None),
            size=(80, 60),
            font_size=22)

        date_box = BoxLayout(
            orientation='horizontal', 
            spacing=10, 
            size_hint=(None, None), 
            size=(280, 60))
        date_box.add_widget(self.year_spinner)
        date_box.add_widget(self.month_spinner)
        date_box.add_widget(self.day_spinner)

        date_anchor = AnchorLayout(anchor_x='center')
        date_anchor.add_widget(date_box)
        self.form_layout.add_widget(date_anchor)

        self.message_label = Label(size_hint_y=None, height=40, font_size=20, color=(1, 0, 0, 1))
        self.form_layout.add_widget(self.message_label)

        root = FloatLayout()

        form_anchor = AnchorLayout(anchor_x='center', anchor_y='center', size_hint=(1, 1), pos_hint={"center_y": 0.75})
        form_anchor.add_widget(self.form_layout)
        root.add_widget(form_anchor)

        self.save_button = Button(
            text="Save and Continue",
            size_hint=(None, None),
            size=(280, 60),
            font_size=24,
            pos_hint={"center_x": 0.5, "y": 0.05})
        self.save_button.bind(on_press=self.save_data)
        root.add_widget(self.save_button)

        self.add_widget(root)

    def open_name_input(self, instance):
        content = BoxLayout(orientation='vertical', padding=10, spacing=10)
        ti = TextInput(text=self.entered_name, multiline=False, font_size=22, size_hint_y=None, height=60)
        btn = Button(text="OK", size_hint_y=None, height=60, font_size=22)
        content.add_widget(ti)
        content.add_widget(btn)

        popup = Popup(title="Enter Your Name", content=content, size_hint=(0.8, 0.4))

        def on_ok(instance):
            self.entered_name = ti.text.strip()
            self.name_input.text = self.entered_name if self.entered_name else "Enter Your Name"
            popup.dismiss()

        btn.bind(on_press=on_ok)
        popup.open()

    def save_data(self, instance):
        name = self.entered_name.strip()
        year = self.year_spinner.text
        month = self.month_spinner.text
        day = self.day_spinner.text

        if not name:
            self.message_label.text = "X Please enter your name."
            return
        if not (year.isdigit() and month.isdigit() and day.isdigit()):
            self.message_label.text = "X Please select a valid date."
            return
        try:
            clean_date = datetime(int(year), int(month), int(day)).date()
        except ValueError:
            self.message_label.text = "X Invalid date."
            return

        save_user_data(name, clean_date.strftime("%Y-%m-%d"))
        self.manager.transition_to("main")
        self.manager.get_screen("main").update_screen()


class MainScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = FloatLayout()
        self.top_image = Image(size_hint=(0.3, 0.3), pos_hint={"center_x": 0.5, "top": 1})
        self.label = Label(text="", font_size=24, halign="center", valign="middle",
                           size_hint=(0.9, 0.4), pos_hint={"center_x": 0.5, "center_y": 0.5})
        self.label.bind(size=self.label.setter('text_size'))
        self.bottom_image = Image(size_hint=(0.3, 0.3), pos_hint={"center_x": 0.5, "y": 0})
        self.home_button = Button(text="Home", size_hint=(0.15, None), height=60,
                                  background_color=(0, 0, 0, 0), background_normal="",
                                  color=(1, 1, 1, 1), font_size=22, pos_hint={"center_x": 0.83, "y": 0.05})
        self.home_button.bind(on_press=lambda x: self.manager.transition_to("home"))
        self.layout.add_widget(self.top_image)
        self.layout.add_widget(self.label)
        self.layout.add_widget(self.bottom_image)
        self.layout.add_widget(self.home_button)
        self.add_widget(self.layout)

    def on_enter(self):
        self.update_screen()

    def clean_time_message(self, clean_date_str):
        """Return a human-readable string for clean time (years, months, days)."""
        clean_date = date.fromisoformat(clean_date_str)
        today = date.today()
        delta = relativedelta(today, clean_date)

        if delta.years == 0 and delta.months == 0:
            return f"{delta.days} day{'s' if delta.days != 1 else ''}"

        parts = []
        if delta.years > 0:
            parts.append(f"{delta.years} year{'s' if delta.years > 1 else ''}")
        if delta.months > 0:
            parts.append(f"{delta.months} month{'s' if delta.months > 1 else ''}")
        if delta.days > 0:
            parts.append(f"{delta.days} day{'s' if delta.days > 1 else ''}")

        if len(parts) > 1:
            return ", ".join(parts[:-1]) + " and " + parts[-1]
        else:
            return parts[0]

    def update_screen(self):
        data = load_user_data()
        if not data:
            self.label.text = "No user data found."
            return

        try:
            name = data.get("name", "Friend")
            clean_date = data.get("clean_date")
            days = calculate_days_clean(clean_date)
            image_path = get_random_image()

            # Normalize and validate image path
            if image_path:
                image_path = os.path.abspath(os.path.normpath(image_path))

            # Milestone messages
            if days == 30:
                message = "30 days clean! That’s one hell of a month. You’ve just done something most people couldn’t. Respect."
            elif days == 60:
                message = "60 days clean — you're no rookie anymore. Two months of fighting back. Keep killing it."
            elif days == 90:
                message = "90 days! That’s a whole quarter of a year clean. You’re not just surviving — you’re winning."
            elif days == 180:
                message = "Half a freakin’ year clean. That’s strength. That’s growth. That’s you changing your life."
            elif days == 270:
                message = "9 months clean — you've rebuilt more than just habits. You’ve rebuilt *you*."
            elif days == 365:
                message = "1 full year. 365 clean days. A whole revolution around the sun — and you’re still rising. 🎉"
            elif days == 547:
                message = "18 months clean. That’s not luck — that’s you doing the work. Quietly unstoppable."
            elif days >= 730 and days % 365 == 0:
                years = days // 365
                message = f"{years} years clean. You’ve come a long way — and you’re still leveling up."
            else:
                message = random.choice(motivational_messages)

            # Use the new clean_time_message function
            pretty_time = self.clean_time_message(clean_date)
            self.label.text = f"{name}, you have been clean for {pretty_time}!\n\n{message}"

            if image_path and os.path.exists(image_path):
                self.top_image.source = image_path
                self.bottom_image.source = image_path
            else:
                self.top_image.source = ""
                self.bottom_image.source = ""
        except Exception as e:
            self.label.text = "Error loading data."
            print("Exception in update_screen:", e)


DATA_FILE = Path("JSON_files/user_data.json")


class HomeScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        root = FloatLayout()

        top_label = Label(
            text="Home Screen",
            font_size=28,
            size_hint=(None, None),
            size=(400, 60),
            pos_hint={"center_x": 0.5, "top": 0.98})
        root.add_widget(top_label)

        na_button = Button(
            text="Narcotics Anonymous Readings",
            size_hint=(None, None),
            size=(310, 60),
            font_size=20,
            pos_hint={"center_x": 0.5, "center_y": 0.65})
        na_button.bind(on_press=lambda x: self.manager.transition_to("na_readings"))
        root.add_widget(na_button)

        aa_button = Button(
            text="Alcoholics Anonymous Readings",
            size_hint=(None, None),
            size=(310, 60),
            font_size=20,
            pos_hint={"center_x": 0.5, "center_y": 0.53})
        aa_button.bind(on_press=lambda x: self.manager.transition_to("aa_readings"))
        root.add_widget(aa_button)

        bottom_row = BoxLayout(
            orientation='horizontal',
            size_hint=(1, None),
            height=60,
            padding=[30, 0, 30, 20],
            spacing=20,
            pos_hint={"x": 0, "y": 0}
        )

        back_button = Button(
            text="Back to Message",
            size_hint=(None, None),
            size=(200, 50),
            font_size=20)
        back_button.bind(on_press=lambda x: self.manager.transition_to("main"))

        reset_button = Button(
            text="Reset Clean Date",
            size_hint=(None, None),
            size=(200, 50),
            font_size=20)
        reset_button.bind(on_press=self.reset_clean_date)

        bottom_row.add_widget(back_button)
        bottom_row.add_widget(Widget())
        bottom_row.add_widget(reset_button)

        root.add_widget(bottom_row)
        self.add_widget(root)

    def reset_clean_date(self, instance):
        if DATA_FILE.exists():
            DATA_FILE.unlink()
            print("User data reset.")
        else:
            print("No user data file found to reset.")
        self.manager.transition_to("setup")


class NAReadingsMenuScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        layout = FloatLayout()

        # Title label centered at the top
        title = Label(
            text="NA Readings",
            font_size='32sp',
            size_hint=(None, None),
            size=(300, 50),
            pos_hint={"center_x": 0.5, "top": 0.95}
        )
        layout.add_widget(title)

        # Just For Today button
        jft_btn = Button(
            text="Just For Today",
            size_hint=(None, None),
            size=(300, 60),
            pos_hint={"center_x": 0.5, "center_y": 0.58},
            font_size=18
        )
        # Open the JFT website when pressed
        jft_btn.bind(on_press=lambda x: webbrowser.open("https://www.jftna.org/jft/"))
        layout.add_widget(jft_btn)

        # Spiritual Principle-A-Day button (replaces NA Basic Text)
        spad_btn = Button(
            text="Spiritual Principle-A-Day",
            size_hint=(None, None),
            size=(300, 60),
            pos_hint={"center_x": 0.5, "center_y": 0.47},
            font_size=18
        )
        # Open the SPAD website when pressed
        spad_btn.bind(on_press=lambda x: webbrowser.open("https://www.spadna.org"))
        layout.add_widget(spad_btn)

        # Back button bottom right
        back_btn = Button(
            text="Back",
            size_hint=(None, None),
            size=(100, 50),
            pos_hint={"right": 0.98, "y": 0.02},
            font_size=16
        )
        back_btn.bind(on_press=lambda x: setattr(self.manager, 'current', 'home'))
        layout.add_widget(back_btn)

        self.add_widget(layout)


class AAReadingsMenuScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        layout = FloatLayout()

        title = Label(
            text="AA Readings",
            font_size='32sp',
            size_hint=(None, None),
            size=(300, 50),
            pos_hint={"center_x": 0.5, "top": 0.95}
        )
        layout.add_widget(title)

        # Daily Reflections Reading button
        btn1 = Button(
            text="Daily Reflections Reading",
            size_hint=(None, None),
            size=(300, 60),
            pos_hint={"center_x": 0.5, "center_y": 0.58},
            font_size=18
        )
        # Open AA Daily Reflections website
        btn1.bind(on_press=lambda x: webbrowser.open("https://www.aa.org/daily-reflections"))
        layout.add_widget(btn1)

        # 24 Hours a Day button
        btn2 = Button(
            text="24 Hours a Day",
            size_hint=(None, None),
            size=(300, 60),
            pos_hint={"center_x": 0.5, "center_y": 0.47},
            font_size=18
        )
        # Open Hazelden 24 Hours a Day website
        btn2.bind(on_press=lambda x: webbrowser.open("https://www.hazeldenbettyford.org/thought-for-the-day"))
        layout.add_widget(btn2)

        # Back button bottom right
        back_btn = Button(
            text="Back",
            size_hint=(None, None),
            size=(100, 50),
            pos_hint={"right": 0.98, "y": 0.02},
            font_size=16
        )
        back_btn.bind(on_press=lambda x: setattr(self.manager, 'current', 'home'))
        layout.add_widget(back_btn)

        self.add_widget(layout)


class MyScreenManager(ScreenManager):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.add_widget(WelcomeScreen(name="welcome"))
        self.add_widget(SetupScreen(name="setup"))
        self.add_widget(MainScreen(name="main"))
        self.add_widget(HomeScreen(name="home"))
        self.add_widget(NAReadingsMenuScreen(name="na_readings"))
        self.add_widget(AAReadingsMenuScreen(name="aa_readings"))
    

    def transition_to(self, screen_name):
        self.transition = SlideTransition(direction="left")
        self.current = screen_name


class CleanTimeApp(App):
    def build(self):
        self.title = "From Darkness We Climb"  # <-- Add this line

        self.sm = MyScreenManager()
        # Load user data and decide where to go:
        user_data = load_user_data()
        if user_data:
            self.sm.current = "main"
        else:
            self.sm.current = "welcome"
        return self.sm


if __name__ == "__main__":
    CleanTimeApp().run()

