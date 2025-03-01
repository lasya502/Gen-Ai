import tkinter as tk
from tkinter import messagebox, simpledialog, ttk
import random

class StudyProApp:
    def __init__(self, root):
        self.root = root
        self.root.title("StudyPro: AI-Powered Study Planner")
        self.root.geometry("900x900")

        # User Management
        self.users = {}
        self.current_user = None
        self.tasks = []
        self.completed_tasks = []
        self.user_preferences = {}
        self.task_schedule = {}
        self.books = []  # List to store books

        # Study Session Variables
        self.study_session_duration = 25 * 60  # Default Pomodoro duration (25 mins)
        self.break_duration = 5 * 60  # Break duration (5 mins)
        self.timer_running = False
        self.elapsed_time = 0  # Time elapsed in the current session
        self.notification_times = 5  # Default time for notifications (in minutes)

        # Progress Tracking
        self.total_study_time = 0  # Total study time in seconds
        self.study_goal_target = 0  # Total study hours from user preferences
        self.study_goal_completion = 0  # Tracks completed hours

        # Motivation Messages
        self.motivational_messages = [
            "Great job! Keep it up!",
            "You're doing fantastic!",
            "Stay focused, you're almost there!",
            "Remember, consistency is key!",
            "Believe in yourself!"
        ]

        # Initialize Notification settings
        self.notifications_enabled = True  # Default notification setting
        self.reminder_interval = 30  # Default reminder interval in minutes

        # User Profile Information
        self.user_info = {
            'name': '',
            'email': '',
            'study_goal': '',
            'study_time': '',
            'study_technique': ''
        }

        # Welcome Frame
        self.welcome_frame = tk.Frame(root, bg="#E0F7FA")
        self.welcome_frame.pack(fill="both", expand=True)

        # Title
        self.app_name_label = tk.Label(self.welcome_frame, text="StudyPro", font=("Arial", 24, "bold"), bg="#E0F7FA", fg="#006064")
        self.app_name_label.pack(pady=(20, 10))

        # Tagline
        self.tagline_label = tk.Label(self.welcome_frame, text="Your personalized study guide, powered by AI.", font=("Arial", 14), bg="#E0F7FA", fg="#00796B")
        self.tagline_label.pack(pady=(0, 10))

        # Centered Button Frame
        button_frame = tk.Frame(self.welcome_frame, bg="#E0F7FA")
        button_frame.pack(expand=True)  # Allow the button_frame to take extra space and center vertically

        self.signup_button = tk.Button(button_frame, text="Sign Up", command=self.show_signup, width=15, height=2, bg="#00796B", fg="white")
        self.signup_button.pack(pady=10)

        self.login_button = tk.Button(button_frame, text="Log In", command=self.show_login, width=15, height=2, bg="#00796B", fg="white")
        self.login_button.pack(pady=10)

        self.guest_button = tk.Button(button_frame, text="Guest Access", command=self.show_guest_access, width=20, height=2, bg="#00796B", fg="white")
        self.guest_button.pack(pady=10)

    def show_signup(self):
        self.clear_frames()
        self.signup_frame = tk.Frame(self.root, bg="#E0F7FA")
        self.signup_frame.pack(fill="both", expand=True)

        tk.Label(self.signup_frame, text="Sign Up", font=("Arial", 24), bg="#E0F7FA", fg="#006064").pack(pady=(20, 10))

        tk.Label(self.signup_frame, text="Username", bg="#E0F7FA", fg="#006064").pack(pady=5)
        self.signup_username_entry = tk.Entry(self.signup_frame)
        self.signup_username_entry.pack(pady=5)

        tk.Label(self.signup_frame, text="Password", bg="#E0F7FA", fg="#006064").pack(pady=5)
        self.signup_password_entry = tk.Entry(self.signup_frame, show='*')
        self.signup_password_entry.pack(pady=5)

        button_frame = tk.Frame(self.signup_frame, bg="#E0F7FA")
        button_frame.pack(pady=20)

        tk.Button(button_frame, text="Create Account", command=self.create_account, bg="#00796B", fg="white").pack(side=tk.LEFT, padx=10)
        tk.Button(button_frame, text="Go Back", command=self.go_back, bg="#00796B", fg="white").pack(side=tk.RIGHT, padx=10)

    def create_account(self):
        username = self.signup_username_entry.get()
        password = self.signup_password_entry.get()
        if username in self.users:
            messagebox.showwarning("Warning", "Username already exists. Please choose another one.")
        else:
            self.users[username] = password
            messagebox.showinfo("Sign Up", f"Account for {username} created successfully!")
            self.show_login()

    def show_login(self):
        self.clear_frames()
        self.login_frame = tk.Frame(self.root, bg="#E0F7FA")
        self.login_frame.pack(fill="both", expand=True)

        tk.Label(self.login_frame, text="Log In", font=("Arial", 24), bg="#E0F7FA", fg="#006064").pack(pady=(20, 10))

        tk.Label(self.login_frame, text="Username", bg="#E0F7FA", fg="#006064").pack(pady=5)
        self.login_username_entry = tk.Entry(self.login_frame)
        self.login_username_entry.pack(pady=5)

        tk.Label(self.login_frame, text="Password", bg="#E0F7FA", fg="#006064").pack(pady=5)
        self.login_password_entry = tk.Entry(self.login_frame, show='*')
        self.login_password_entry.pack(pady=5)

        button_frame = tk.Frame(self.login_frame, bg="#E0F7FA")
        button_frame.pack(pady=20)

        tk.Button(button_frame, text="Log In", command=self.validate_login, bg="#00796B", fg="white").pack(side=tk.LEFT, padx=10)
        tk.Button(button_frame, text="Go Back", command=self.go_back, bg="#00796B", fg="white").pack(side=tk.RIGHT, padx=10)

    def validate_login(self):
        username = self.login_username_entry.get()
        password = self.login_password_entry.get()
        if username in self.users and self.users[username] == password:
            self.current_user = username
            messagebox.showinfo("Login", f"Welcome back, {username}!")
            self.show_onboarding()
        else:
            messagebox.showerror("Error", "Invalid username or password.")

    def show_guest_access(self):
        self.clear_frames()
        self.guest_frame = tk.Frame(self.root, bg="#E0F7FA")
        self.guest_frame.pack(fill="both", expand=True)

        tk.Label(self.guest_frame, text="Welcome, Guest!", font=("Arial", 18), bg="#E0F7FA", fg="#006064").pack(pady=(20, 10))
        tk.Label(self.guest_frame, text="You have limited access to features.", bg="#E0F7FA", fg="#006064").pack(pady=5)
        tk.Label(self.guest_frame, text="Please consider signing up for full access.", bg="#E0F7FA", fg="#006064").pack(pady=5)

        button_frame = tk.Frame(self.guest_frame, bg="#E0F7FA")
        button_frame.pack(expand=True)  # Center the button frame vertically
        
        tk.Button(button_frame, text="Proceed to Onboarding", command=self.show_onboarding, bg="#00796B", fg="white").pack(side=tk.LEFT, padx=10)
        tk.Button(button_frame, text="Go Back", command=self.go_back, bg="#00796B", fg="white").pack(side=tk.RIGHT, padx=10)

    def show_onboarding(self):
        self.clear_frames()
        self.onboarding_step = 1
        self.onboarding_frames = []

        # Step 1: Study Goals
        self.onboarding_frame1 = tk.Frame(self.root, bg="#E0F7FA")
        self.onboarding_frames.append(self.onboarding_frame1)

        tk.Label(self.onboarding_frame1, text="Step 1: Tell us about your study goals.", font=("Arial", 18), bg="#E0F7FA", fg="#006064").pack(pady=(20, 10))
        tk.Label(self.onboarding_frame1, text="What is your main study goal?", bg="#E0F7FA", fg="#006064").pack(pady=5)
        self.study_goal_entry = tk.Entry(self.onboarding_frame1)
        self.study_goal_entry.pack(pady=5)

        tk.Label(self.onboarding_frame1, text="Which subjects are you focusing on?", bg="#E0F7FA", fg="#006064").pack(pady=5)
        self.subjects_entry = tk.Entry(self.onboarding_frame1)
        self.subjects_entry.pack(pady=5)

        tk.Label(self.onboarding_frame1, text="How many hours per day can you dedicate to studying?", bg="#E0F7FA", fg="#006064").pack(pady=5)
        self.hours_entry = tk.Entry(self.onboarding_frame1)
        self.hours_entry.pack(pady=5)

        button_frame = tk.Frame(self.onboarding_frame1, bg="#E0F7FA")
        button_frame.pack(pady=20)

        tk.Button(button_frame, text="Next", command=self.next_onboarding, bg="#00796B", fg="white").pack()

        self.onboarding_frame1.pack(fill="both", expand=True)

    def next_onboarding(self):
        if self.onboarding_step == 1:
            if not self.study_goal_entry.get() or not self.subjects_entry.get() or not self.hours_entry.get():
                messagebox.showwarning("Warning", "Please fill in all fields.")
                return
            
            self.user_preferences['goal'] = self.study_goal_entry.get()
            self.user_preferences['subjects'] = [subject.strip() for subject in self.subjects_entry.get().split(",")]
            self.user_preferences['hours_per_day'] = int(self.hours_entry.get())

            self.onboarding_frame1.pack_forget()

            # Step 2: Preferred Study Times
            self.onboarding_frame2 = tk.Frame(self.root, bg="#E0F7FA")
            self.onboarding_frames.append(self.onboarding_frame2)

            tk.Label(self.onboarding_frame2, text="Step 2: Your preferred study times.", font=("Arial", 18), bg="#E0F7FA", fg="#006064").pack(pady=(20, 10))
            tk.Label(self.onboarding_frame2, text="When are you most productive?", bg="#E0F7FA", fg="#006064").pack(pady=5)
            self.productive_time_entry = tk.StringVar(value="Morning")
            tk.OptionMenu(self.onboarding_frame2, self.productive_time_entry, "Morning", "Afternoon", "Evening").pack(pady=5)

            tk.Label(self.onboarding_frame2, text="What is your typical availability?", bg="#E0F7FA", fg="#006064").pack(pady=5)
            self.availability_entry = tk.Entry(self.onboarding_frame2)
            self.availability_entry.pack(pady=5)

            button_frame = tk.Frame(self.onboarding_frame2, bg="#E0F7FA")
            button_frame.pack(pady=20)

            tk.Button(button_frame, text="Back", command=self.back_onboarding, bg="#00796B", fg="white").pack(side=tk.LEFT, padx=10)
            tk.Button(button_frame, text="Next", command=self.next_onboarding, bg="#00796B", fg="white").pack(side=tk.RIGHT, padx=10)

            self.onboarding_frame2.pack(fill="both", expand=True)
            self.onboarding_step += 1
        elif self.onboarding_step == 2:
            self.user_preferences['productive_time'] = self.productive_time_entry.get()
            self.user_preferences['availability'] = self.availability_entry.get()

            self.onboarding_frame2.pack_forget()

            self.onboarding_frame3 = tk.Frame(self.root, bg="#E0F7FA")
            self.onboarding_frames.append(self.onboarding_frame3)

            tk.Label(self.onboarding_frame3, text="Step 3: Personalize your study style.", font=("Arial", 18), bg="#E0F7FA", fg="#006064").pack(pady=(20, 10))
            self.study_style_var = tk.StringVar(value="Focused Sessions")
            tk.Label(self.onboarding_frame3, text="Do you prefer focused study sessions or short breaks?").pack(pady=5)
            tk.OptionMenu(self.onboarding_frame3, self.study_style_var, "Focused Sessions", "Frequent Breaks").pack(pady=5)

            tk.Label(self.onboarding_frame3, text="Preferred study techniques:").pack(pady=5)
            self.study_technique_var = tk.StringVar(value="Active Recall")
            tk.OptionMenu(self.onboarding_frame3, self.study_technique_var, "Active Recall", "Spaced Repetition", "Other").pack(pady=5)

            button_frame = tk.Frame(self.onboarding_frame3, bg="#E0F7FA")
            button_frame.pack(pady=20)

            tk.Button(button_frame, text="Back", command=self.back_onboarding, bg="#00796B", fg="white").pack(side=tk.LEFT, padx=10)
            tk.Button(button_frame, text="Next", command=self.next_onboarding, bg="#00796B", fg="white").pack(side=tk.RIGHT, padx=10)

            self.onboarding_frame3.pack(fill="both", expand=True)
            self.onboarding_step += 1
        elif self.onboarding_step == 3:
            self.user_preferences['study_style'] = self.study_style_var.get()
            self.user_preferences['study_technique'] = self.study_technique_var.get()

            self.onboarding_frame3.pack_forget()

            self.onboarding_frame4 = tk.Frame(self.root, bg="#E0F7FA")
            self.onboarding_frames.append(self.onboarding_frame4)

            tk.Label(self.onboarding_frame4, text="Step 4: AI Customization.", font=("Arial", 18), bg="#E0F7FA", fg="#006064").pack(pady=(20, 10))
            tk.Label(self.onboarding_frame4, text="Based on the information you provide, StudyPro will generate your tasks.", bg="#E0F7FA", fg="#006064").pack(pady=20)

            tk.Button(self.onboarding_frame4, text="Generate Tasks", command=self.generate_tasks, bg="#00796B", fg="white").pack(pady=20)

            self.onboarding_frame4.pack(fill="both", expand=True)

    def back_onboarding(self):
        if self.onboarding_step == 2:
            self.onboarding_frame2.pack_forget()
            self.onboarding_frame1.pack(fill="both", expand=True)
            self.onboarding_step -= 1
        elif self.onboarding_step == 3:
            self.onboarding_frame3.pack_forget()
            self.onboarding_frame2.pack(fill="both", expand=True)
            self.onboarding_step -= 1
        elif self.onboarding_step == 4:
            self.onboarding_frame4.pack_forget()
            self.onboarding_frame3.pack(fill="both", expand=True)
            self.onboarding_step -= 1

    def generate_tasks(self):
        self.tasks.clear()  # Clear previous tasks
        self.completed_tasks.clear()  # Clear previous completed tasks

        # Generate tasks based on user preferences
        goal = self.user_preferences['goal']
        subjects = self.user_preferences['subjects']
        hours_per_day = self.user_preferences['hours_per_day']

        for subject in subjects:
            for hour in range(hours_per_day):
                task_time = f"{hour + 9}:00"  # Assuming study starts at 9 AM
                task = f"Review {subject} concepts for 1 hour ({task_time})."
                self.tasks.append(task)

        messagebox.showinfo("Task Generation Complete", "Your study tasks have been generated!")
        self.onboarding_frame4.pack_forget()
        
        # Now show the AI-powered study plan screen
        self.show_study_plan()

    def show_study_plan(self):
        self.clear_frames()

        self.study_plan_frame = tk.Frame(self.root, bg="#E0F7FA")
        self.study_plan_frame.pack(fill="both", expand=True)

        tk.Label(self.study_plan_frame, text="Your Study Plan", font=("Arial", 24), bg="#E0F7FA", fg="#006064").pack(pady=(20, 10))

        tk.Label(self.study_plan_frame, text="Generated Plan:", font=("Arial", 20), bg="#E0F7FA", fg="#006064").pack(pady=(10, 5))

        self.study_plan_listbox = tk.Listbox(self.study_plan_frame, selectmode=tk.MULTIPLE, width=60, height=10)
        self.study_plan_listbox.pack(pady=(0, 20))

        for task in self.tasks:
            self.study_plan_listbox.insert(tk.END, task)

        tk.Label(self.study_plan_frame, text="AI Suggestions:", font=("Arial", 20), bg="#E0F7FA", fg="#006064").pack(pady=(10, 5))

        self.ai_suggestions_label = tk.Label(self.study_plan_frame, text="", bg="#E0F7FA")
        self.ai_suggestions_label.pack(pady=5)

        self.generate_ai_suggestions()

        button_frame = tk.Frame(self.study_plan_frame, bg="#E0F7FA")
        button_frame.pack(pady=(20, 10))  # Center button frame
        
        tk.Button(button_frame, text="Start Study Sessions", command=self.start_study_session, bg="#00796B", fg="white").pack(side=tk.LEFT, padx=10)
        tk.Button(button_frame, text="Go Back", command=self.show_onboarding, bg="#00796B", fg="white").pack(side=tk.LEFT, padx=10)
        tk.Button(button_frame, text="Show Progress Tracker", command=self.show_progress_tracker, bg="#00796B", fg="white").pack(side=tk.LEFT, padx=10)
        tk.Button(button_frame, text="Profile & Preferences", command=self.show_user_profile, bg="#00796B", fg="white").pack(side=tk.LEFT, padx=10)
        tk.Button(button_frame, text="Manage Books", command=self.manage_books, bg="#00796B", fg="white").pack(side=tk.LEFT, padx=10)
        tk.Button(button_frame, text="Notification Settings", command=self.show_notification_settings, bg="#00796B", fg="white").pack(side=tk.LEFT, padx=10)

    def generate_ai_suggestions(self):
        preferred_study_technique = self.user_preferences.get('study_technique', 'Active Recall')
        availability = self.user_preferences.get('availability', 'All Day')

        suggestions = f"Based on your preference for {preferred_study_technique}, use it frequently. " \
                      f"Considering your availability of {availability}, try to incorporate short breaks."

        self.ai_suggestions_label.config(text=suggestions)

    def start_study_session(self):
        if self.tasks:
            selected_task_index = self.study_plan_listbox.curselection()
            if selected_task_index:
                task = self.tasks[selected_task_index[0]]  # Start with the selected task
                self.study_session(task)
            else:
                messagebox.showwarning("Warning", "Please select a task to start studying.")
        else:
            messagebox.showwarning("Warning", "No tasks found. Please generate tasks first.")

    def study_session(self, task):
        self.clear_frames()

        self.study_session_frame = tk.Frame(self.root, bg="#E0F7FA")
        self.study_session_frame.pack(fill="both", expand=True)

        tk.Label(self.study_session_frame, text=f"Study Session: {task.split(' ')[2]}", font=("Arial", 24), bg="#E0F7FA", fg="#006064").pack(pady=(20, 10))

        self.timer_label = tk.Label(self.study_session_frame, text=self.format_time(self.study_session_duration), font=("Arial", 48), bg="#E0F7FA", fg="#00796B")
        self.timer_label.pack(pady=(0, 10))

        tk.Label(self.study_session_frame, text="Study Material:", bg="#E0F7FA", fg="#006064").pack(pady=5)
        self.study_resources_entry = tk.Entry(self.study_session_frame, width=60)
        self.study_resources_entry.pack(pady=5)
        self.study_resources_entry.insert(0, "Enter links to study resources or articles...")

        self.progress = ttk.Progressbar(self.study_session_frame, maximum=self.study_session_duration, mode='determinate')
        self.progress.pack(pady=10)

        button_frame = tk.Frame(self.study_session_frame, bg="#E0F7FA")
        button_frame.pack(pady=(20, 10))

        tk.Button(button_frame, text="Take a Break", command=self.take_break, bg="#00796B", fg="white").pack(side=tk.LEFT, padx=10)

        tk.Button(button_frame, text="End Session", command=self.end_study_session, bg="#00796B", fg="white").pack(side=tk.RIGHT, padx=10)

        self.start_timer()

        self.current_task = task  # Store the current task to mark it completed later

        self.check_notifications()

    def start_timer(self):
        self.elapsed_time = 0  # Reset the timer
        self.timer_running = True
        self.update_timer()

    def update_timer(self):
        if self.timer_running and self.elapsed_time < self.study_session_duration:
            self.elapsed_time += 1
            self.progress['value'] = self.elapsed_time

            remaining_time = self.study_session_duration - self.elapsed_time
            self.timer_label.config(text=self.format_time(remaining_time))

            if self.elapsed_time % 1500 == 0:  # 25 minutes
                self.prompt_break()

            self.root.after(1000, self.update_timer)  # Update every second
        else:
            if self.elapsed_time >= self.study_session_duration:
                self.complete_task()  # Mark the task as completed when session ends

    def complete_task(self):
        self.completed_tasks.append(self.current_task)
        self.total_study_time += self.study_session_duration  # Update total study time
        self.study_goal_completion += 1  # Increment completed study hours
        messagebox.showinfo("Session Complete", f"You have completed: {self.current_task}")

        # Send encouragement
        messagebox.showinfo("Encouragement", random.choice(self.motivational_messages))

        self.end_study_session()  # End the study session and return to the study plan

    def prompt_break(self):
        if messagebox.askyesno("Break Time!", "You've been studying for 25 minutes! Do you want to take a break?"):
            self.take_break()  # If user chooses to take a break, call the break function

    def take_break(self):
        self.timer_running = False
        self.break_timer = self.break_duration
        self.break_progress = ttk.Progressbar(self.study_session_frame, maximum=self.break_duration, mode='determinate')
        self.break_progress.pack(pady=10)

        def update_break_timer():
            if self.break_timer > 0:
                self.break_progress['value'] = self.break_duration - self.break_timer
                self.break_timer -= 1
                self.root.after(1000, update_break_timer)
            else:
                self.break_progress.pack_forget()
                self.timer_running = True
                self.start_timer()

        update_break_timer()

    def end_study_session(self):
        self.timer_running = False
        messagebox.showinfo("Session Ended", "You have ended your study session.")
        self.clear_frames()
        self.show_study_plan()

    def check_notifications(self):
        if self.notifications_enabled:
            self.root.after(60000, self.remind_user)

    def remind_user(self):
        if self.elapsed_time // 60 % self.reminder_interval == 0 and self.elapsed_time != 0:
            messagebox.showinfo("Reminder", "Time to hydrate! Don't forget to drink water.")
        
        self.check_notifications()

    def show_notification_settings(self):
        self.clear_frames()
        self.notification_frame = tk.Frame(self.root, bg="#E0F7FA")
        self.notification_frame.pack(fill="both", expand=True)

        tk.Label(self.notification_frame, text="Notification Settings", font=("Arial", 24), bg="#E0F7FA", fg="#006064").pack(pady=(20, 10))

        tk.Label(self.notification_frame, text="Enable Notifications:").pack(pady=5)
        self.notifications_check_var = tk.IntVar(value=1 if self.notifications_enabled else 0)
        tk.Checkbutton(self.notification_frame, variable=self.notifications_check_var, bg="#E0F7FA").pack(pady=5)

        tk.Label(self.notification_frame, text="Reminder Interval (in minutes):").pack(pady=5)
        self.reminder_interval_entry = tk.Entry(self.notification_frame, width=5)
        self.reminder_interval_entry.pack(pady=5)
        self.reminder_interval_entry.insert(0, str(self.reminder_interval // 60))

        button_frame = tk.Frame(self.notification_frame, bg="#E0F7FA")
        button_frame.pack(pady=(20, 10))

        tk.Button(button_frame, text="Save Settings", command=self.save_notification_settings, bg="#00796B", fg="white").pack(side=tk.LEFT, padx=10)
        tk.Button(button_frame, text="Go Back", command=self.show_study_plan, bg="#00796B", fg="white").pack(side=tk.RIGHT, padx=10)

    def save_notification_settings(self):
        self.notifications_enabled = bool(self.notifications_check_var.get())
        self.reminder_interval = int(self.reminder_interval_entry.get()) * 60  # Convert to seconds
        messagebox.showinfo("Settings Saved", "Your notification settings have been saved.")
        self.show_study_plan()

    def show_progress_tracker(self):
        self.clear_frames()

        self.progress_frame = tk.Frame(self.root, bg="#E0F7FA")
        self.progress_frame.pack(fill="both", expand=True)

        tk.Label(self.progress_frame, text="Your Progress", font=("Arial", 24), bg="#E0F7FA", fg="#006064").pack(pady=(20, 10))

        goal_status = (self.study_goal_completion / self.study_goal_target) * 100 if self.study_goal_target else 0
        goal_status_label = f"Study Goal Status: {goal_status:.2f}% completed"
        tk.Label(self.progress_frame, text=goal_status_label, bg="#E0F7FA", fg="#006064").pack(pady=10)

        completed_tasks_label = f"Completed Tasks: {len(self.completed_tasks)} out of {len(self.tasks)}"
        tk.Label(self.progress_frame, text=completed_tasks_label, bg="#E0F7FA", fg="#006064").pack(pady=10)

        daily_statistics = f"Daily Study Time: {self.total_study_time // 60} minutes"  # Convert seconds to minutes
        tk.Label(self.progress_frame, text=daily_statistics, bg="#E0F7FA", fg="#006064").pack(pady=10)

        tk.Label(self.progress_frame, text="Weekly and Monthly statistics are not implemented yet.", bg="#E0F7FA", fg="#006064").pack(pady=10)

        button_frame = tk.Frame(self.progress_frame, bg="#E0F7FA")
        button_frame.pack(pady=(20, 10))

        tk.Button(button_frame, text="Adjust Goals", command=self.adjust_goals, bg="#00796B", fg="white").pack(side=tk.LEFT, padx=10)
        tk.Button(button_frame, text="Go Back", command=self.show_study_plan, bg="#00796B", fg="white").pack(side=tk.RIGHT, padx=10)

    def adjust_goals(self):
        new_goal = simpledialog.askinteger("Adjust Goals", "Set new goal (hours):", minvalue=1)
        if new_goal:
            self.study_goal_target = new_goal
            messagebox.showinfo("Goal Updated", f"New study goal is set to {new_goal} hours.")

    def format_time(self, seconds):
        mins, secs = divmod(seconds, 60)
        return f"{mins:02}:{secs:02}"

    def clear_frames(self):
        """Hide all frames to prevent overlapping."""
        for widget in self.root.winfo_children():
            widget.pack_forget()

    def go_back(self):
        """Return to the welcome screen."""
        self.clear_frames()
        self.welcome_frame.pack(fill="both", expand=True)

    def show_user_profile(self):
        self.clear_frames()
        self.profile_frame = tk.Frame(self.root, bg="#E0F7FA")
        self.profile_frame.pack(fill="both", expand=True)

        tk.Label(self.profile_frame, text="Profile & Preferences", font=("Arial", 24), bg="#E0F7FA", fg="#006064").pack(pady=(20, 10))

        tk.Label(self.profile_frame, text="Name:").pack(pady=5)
        self.name_entry = tk.Entry(self.profile_frame)
        self.name_entry.pack(pady=5)
        self.name_entry.insert(0, self.user_info['name'])

        tk.Label(self.profile_frame, text="Email:").pack(pady=5)
        self.email_entry = tk.Entry(self.profile_frame)
        self.email_entry.pack(pady=5)
        self.email_entry.insert(0, self.user_info['email'])

        tk.Label(self.profile_frame, text="Study Goal:").pack(pady=5)
        self.study_goal_entry = tk.Entry(self.profile_frame)
        self.study_goal_entry.pack(pady=5)
        self.study_goal_entry.insert(0, self.user_info['study_goal'])

        tk.Label(self.profile_frame, text="Preferred Study Time:").pack(pady=5)
        self.study_time_entry = tk.StringVar(value=self.user_info['study_time'])
        tk.OptionMenu(self.profile_frame, self.study_time_entry, "Morning", "Afternoon", "Evening").pack(pady=5)

        tk.Label(self.profile_frame, text="Preferred Study Technique:").pack(pady=5)
        self.study_technique_entry = tk.StringVar(value=self.user_info['study_technique'])
        tk.OptionMenu(self.profile_frame, self.study_technique_entry, "Active Recall", "Spaced Repetition", "Other").pack(pady=5)

        button_frame = tk.Frame(self.profile_frame, bg="#E0F7FA")
        button_frame.pack(pady=20)

        tk.Button(button_frame, text="Save Profile", command=self.save_profile, bg="#00796B", fg="white").pack(side=tk.LEFT, padx=10)
        tk.Button(button_frame, text="Privacy Settings", command=self.show_privacy_settings, bg="#00796B", fg="white").pack(side=tk.RIGHT, padx=10)
        tk.Button(button_frame, text="Go Back", command=self.show_study_plan, bg="#00796B", fg="white").pack(side=tk.RIGHT, padx=10)

    def save_profile(self):
        self.user_info['name'] = self.name_entry.get()
        self.user_info['email'] = self.email_entry.get()
        self.user_info['study_goal'] = self.study_goal_entry.get()
        self.user_info['study_time'] = self.study_time_entry.get()
        self.user_info['study_technique'] = self.study_technique_entry.get()

        messagebox.showinfo("Profile Saved", "Your profile information has been saved.")
        self.show_study_plan()

    def show_privacy_settings(self):
        self.clear_frames()
        self.privacy_frame = tk.Frame(self.root, bg="#E0F7FA")
        self.privacy_frame.pack(fill="both", expand=True)

        tk.Label(self.privacy_frame, text="Privacy Settings", font=("Arial", 24), bg="#E0F7FA", fg="#006064").pack(pady=(20, 10))

        self.data_sharing_var = tk.IntVar(value=0)  # Default to not sharing
        tk.Checkbutton(self.privacy_frame, text="Allow Data Sharing", variable=self.data_sharing_var, bg="#E0F7FA").pack(pady=10)

        button_frame = tk.Frame(self.privacy_frame, bg="#E0F7FA")
        button_frame.pack(pady=20)

        tk.Button(button_frame, text="Save Privacy Settings", command=self.save_privacy_settings, bg="#00796B", fg="white").pack(side=tk.LEFT, padx=10)
        tk.Button(button_frame, text="Go Back", command=self.show_user_profile, bg="#00796B", fg="white").pack(side=tk.RIGHT, padx=10)

    def save_privacy_settings(self):
        allow_data_sharing = bool(self.data_sharing_var.get())
        if allow_data_sharing:
            messagebox.showinfo("Privacy Settings", "You have allowed data sharing.")
        else:
            messagebox.showinfo("Privacy Settings", "You have disabled data sharing.")

        self.show_user_profile()

    def manage_books(self):
        self.clear_frames()
        self.books_frame = tk.Frame(self.root, bg="#E0F7FA")
        self.books_frame.pack(fill="both", expand=True)

        tk.Label(self.books_frame, text="Manage Books", font=("Arial", 24), bg="#E0F7FA", fg="#006064").pack(pady=(20, 10))

        tk.Label(self.books_frame, text="Book Title:").pack(pady=5)
        self.book_title_entry = tk.Entry(self.books_frame)
        self.book_title_entry.pack(pady=5)

        tk.Label(self.books_frame, text="Author:").pack(pady=5)
        self.book_author_entry = tk.Entry(self.books_frame)
        self.book_author_entry.pack(pady=5)

        button_frame = tk.Frame(self.books_frame, bg="#E0F7FA")
        button_frame.pack(pady=20)

        tk.Button(button_frame, text="Add Book", command=self.add_book, bg="#00796B", fg="white").pack(side=tk.LEFT, padx=10)
        tk.Button(button_frame, text="View Books", command=self.view_books, bg="#00796B", fg="white").pack(side=tk.RIGHT, padx=10)
        tk.Button(button_frame, text="Go Back", command=self.show_study_plan, bg="#00796B", fg="white").pack(side=tk.RIGHT, padx=10)

    def add_book(self):
        title = self.book_title_entry.get()
        author = self.book_author_entry.get()

        if title and author:
            self.books.append({"title": title, "author": author})
            messagebox.showinfo("Success", f"Book '{title}' by {author} added successfully!")
            self.book_title_entry.delete(0, tk.END)
            self.book_author_entry.delete(0, tk.END)
        else:
            messagebox.showwarning("Warning", "Please fill in both fields.")

    def view_books(self):
        self.clear_frames()
        self.view_books_frame = tk.Frame(self.root, bg="#E0F7FA")
        self.view_books_frame.pack(fill="both", expand=True)

        tk.Label(self.view_books_frame, text="Your Books", font=("Arial", 24), bg="#E0F7FA", fg="#006064").pack(pady=(20, 10))

        self.books_listbox = tk.Listbox(self.view_books_frame, width=60, height=10)
        self.books_listbox.pack(pady=(0, 20))

        for book in self.books:
            self.books_listbox.insert(tk.END, f"{book['title']} by {book['author']}")

        button_frame = tk.Frame(self.view_books_frame, bg="#E0F7FA")
        button_frame.pack(pady=(10, 0))

        tk.Button(button_frame, text="Remove Selected Book", command=self.remove_book, bg="#00796B", fg="white").pack(side=tk.LEFT, padx=10)
        tk.Button(button_frame, text="Go Back", command=self.manage_books, bg="#00796B", fg="white").pack(side=tk.RIGHT, padx=10)

    def remove_book(self):
        selected_index = self.books_listbox.curselection()
        if selected_index:
            book_to_remove = selected_index[0]
            book_name = self.books[book_to_remove]['title']
            del self.books[book_to_remove]
            messagebox.showinfo("Success", f"Book '{book_name}' has been removed.")
            self.view_books()  # Refresh the list
        else:
            messagebox.showwarning("Warning", "Please select a book to remove.")

if __name__ == "__main__":
    root = tk.Tk()
    app = StudyProApp(root)
    root.mainloop()
