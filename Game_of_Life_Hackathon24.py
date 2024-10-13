import streamlit as st
from datetime import datetime, timedelta

class Game:
    def __init__(self):
        st.title("Game of Life : The Chore Adventure")

        # Dark mode colors
        self.enable_dark_mode()

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
        st.markdown("<h2 style='color: white;'>Welcome to Game of Life: The Chore Adventure!</h2>", unsafe_allow_html=True)

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
        task_name = task_name.strip()  # Remove extra spaces

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

    def complete_task(self, task_name):
        task_name = task_name.strip().lower()  # Remove extra spaces and convert to lowercase

        # Find the task in the list and complete it
        task_found = False
        updated_tasks = []
        for task in st.session_state.tasks:
            if task["name"] == task_name:  # Match with stored lowercase name
                points_earned = task["points"]  # Use the assigned points for the task
                st.session_state.points += points_earned
                st.success(f"Great job! You completed '{task_name}' and earned {points_earned} points!")
                task_found = True
                if task_name in st.session_state.timers:
                    del st.session_state.timers[task_name]  # Remove timer for completed task
            else:
                updated_tasks.append(task)  # Keep other tasks

        if task_found:
            st.session_state.tasks = updated_tasks  # Update task list to remove the completed task
            self.update_status()  # Update status immediately after completing task
            self.check_level_up()
        else:
            st.warning(f"No task named '{task_name}' found.")

    def check_level_up(self):
        # Check if points exceed current level * 5 to level up
        if st.session_state.points >= st.session_state.level * 5:
            st.session_state.level += 1
            st.success(f"Congratulations! You've leveled up to Level {st.session_state.level}!")

    def update_status(self):
        st.markdown(f"**Current Points:** {st.session_state.points}<br>"
                    f"**Current Level:** {st.session_state.level}<br>"
                    f"**Remaining Tasks:** {len(st.session_state.tasks)}", unsafe_allow_html=True)


if __name__ == "__main__":
    Game()
