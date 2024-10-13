import streamlit as st
from datetime import datetime, timedelta
from player_status import Player

class Game:
    def __init__(self):
        

        # Dark mode colors
        self.enable_dark_mode()

        # Create a Player object
        self.player = Player("player123")

        # Initialize session state
        if 'tasks' not in st.session_state:
            st.session_state.tasks = []  # List of tasks
        if 'points' not in st.session_state:
            st.session_state.points = 0  # Points earned
        if 'level' not in st.session_state:
            st.session_state.level = 1  # Current level
        if 'timers' not in st.session_state:
            st.session_state.timers = {}  # Task timers

        self.show_intro()
        self.add_task_ui()
        self.complete_task_ui()
        self.update_status()

    def enable_dark_mode(self):
        st.markdown(
            """
            <style>
            .reportview-container {
                background: #2E2E2E;
                color: white;
            }
            .stButton>button {
                background-color: #007BFF; 
                color: white; 
                font-size: 18px;
            }
            .stTextInput>div>input {
                background-color: #444444; 
                color: white;
            }
            .stSelectbox>div>select {
                background-color: #444444; 
                color: white;
            }
            </style>
            """,
            unsafe_allow_html=True
        )

    def show_intro(self):
        st.markdown("<h2 style='color: white;'>Welcome to LifeQuest: The Chore Adventure!</h2>", unsafe_allow_html=True)

    def add_task_ui(self):
        st.subheader("Add a Task")
        task_name = st.text_input("Enter a chore you need to do:")
        difficulty = st.selectbox("Select difficulty (1: Easy, 2: Medium, 3: Hard):", options=["1", "2", "3"], index=0)
        
        timer_enabled = st.checkbox("Add timer?")
        time_unit = None
        time_duration = 0
        if timer_enabled:
            time_unit = st.selectbox("Select time unit:", options=["Minutes", "Hours", "Days", "Weeks", "Months"], index=0)
            time_duration = st.slider(f"Set time in {time_unit.lower()}:", 1, 60, 15)

        if st.button("Add Task"):
            self.add_task(task_name, difficulty, time_unit, time_duration)

        st.subheader("Your Tasks:")
        if st.session_state.tasks:
            for task in st.session_state.tasks:
                task_display = f"- {task['name'].capitalize()} (Points: {task['points']}, Difficulty: {task['difficulty']})"
                st.write(task_display)
                st.progress(int(task['difficulty']) / 3)  # Display difficulty progress bar
                # Display countdown timer if a timer was set
                if task["name"] in st.session_state.timers:
                    self.display_timer(task["name"])
        else:
            st.write("No tasks added yet.")

    def display_timer(self, task_name):
        # Get the timer info
        end_time, duration = st.session_state.timers[task_name]
        time_left = end_time - datetime.now()
        
        # If time is left, display it, otherwise warn about expiration
        if time_left.total_seconds() > 0:
            st.info(f"Time left for '{task_name}': {str(time_left).split('.')[0]}")
        else:
            st.warning(f"Time for '{task_name}' has expired!")

    def complete_task_ui(self):
        st.subheader("Complete a Task")
        task_name = st.text_input("Enter task name to complete:")

        if st.button("Complete Task", key="complete_task"):
            self.complete_task(task_name)

    def add_task(self, task_name, difficulty, time_unit, time_duration):
        task_name = task_name.strip()
        self.player.save_to_database()

        if task_name:
            task_points = int(difficulty)  # Assign points based on selected difficulty
            task = {"name": task_name.lower(), "points": task_points, "difficulty": difficulty}
            st.session_state.tasks.append(task)
            st.success(f"Task '{task_name}' added with {task_points} points!")

            # If timer is enabled, calculate the end time based on the selected time unit
            if time_unit and time_duration:
                end_time = self.calculate_end_time(time_unit, time_duration)
                st.session_state.timers[task_name.lower()] = (end_time, time_duration)
                st.success(f"Timer set for {time_duration} {time_unit.lower()} for task '{task_name}'")
        else:
            st.warning("Please enter a task.")

    def calculate_end_time(self, time_unit, time_duration):
        now = datetime.now()

        if time_unit == "Minutes":
            return now + timedelta(minutes=time_duration)
        elif time_unit == "Hours":
            return now + timedelta(hours=time_duration)
        elif time_unit == "Days":
            return now + timedelta(days=time_duration)
        elif time_unit == "Weeks":
            return now + timedelta(weeks=time_duration)
        elif time_unit == "Months":
            return now + timedelta(days=30 * time_duration)  # Approximation for months

    def complete_task_ui(self):
        st.subheader("Complete a Task")

    # Display tasks with checkboxes
    def load_tasks_from_db(player):
        tasks = player.collection.find({"player_id": player.player_id})
        return list(tasks)  # Convert cursor to a list

    if not 'tasks' in st.session_state:
        player = Player()  # Create a Player object
        st.session_state.tasks = load_tasks_from_db(player)

    # Check for completed tasks
    completed_tasks = []
    for task_id in st.session_state.tasks:
        if st.session_state[f"task_{task_id}"]:
            completed_tasks.append(task_id)

    # Process completed tasks
    if completed_tasks:
        for task_id in completed_tasks:
            self.complete_task(task_id)
        st.success("Tasks completed successfully!")
    else:
        st.warning("No tasks selected for completion.")

    def check_level_up(self):
        # Check if points exceed current level * 5 to level up
        if st.session_state.points >= st.session_state.level * 5:
            st.session_state.level += 1
            st.success(f"Congratulations! You've leveled up to Level {st.session_state.level}!")

    def update_status(self):
        st.markdown(f"**Current Points:** {self.player.points}<br>"
                    f"**Current Level:** {self.player.level}<br>"
                    f"**Remaining Tasks:** {len(st.session_state.tasks)}", unsafe_allow_html=True)
    
    def update_level(self, amount):
        self.level = min(5, self.level + amount)
        self.collection.update_one(
        {"player_id": self.player_id}, {"$set": {"level": self.level}}
    )
