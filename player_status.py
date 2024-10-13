import pymongo


class Player:
    def __init__(self, player_id):
        self.player_id = player_id
        self.connection_string = "mongodb+srv://ddm5093:33LtnACdH0B4HyOG@gamecluster.ykw6s.mongodb.net/?retryWrites=true&w=majority&appName=GameCluster"

        try:
            self.client = pymongo.MongoClient(self.connection_string)
            self.db = self.client["taskDB"]
            self.collection = self.db["players"]

            # Retrieve player data from the database
            player_data = self.collection.find_one({"player_id": self.player_id})
            if player_data:
                self.points = player_data.get("points", 0)
                self.level = player_data.get("level", 1)
            else:
                # Create a new player document if not found
                self.collection.insert_one({"player_id": self.player_id, "points": 0, "level": 1})
                self.points = 0
                self.level = 1
        except pymongo.errors.ConnectionError as e:
            print(f"Error connecting to MongoDB: {e}")
            st.error("Error connecting to the database. Please try again later.")

    def update_points(self, amount):
        self.points += amount

    def update_level(self, amount):
        # Update level in the database with limit
        self.level = min(5, self.level + amount)
        self.collection.update_one(
            {"player_id": self.player_id}, {"$set": {"level": self.level}}
        )

    def save_to_database(self):
        # Update both points and level in the database
        self.collection.update_one(
            {"player_id": self.player_id},
            {"$set": {"points": self.points, "level": self.level}},
        )

    def get_status_info(self):
        return f"Points: {self.points}, Level: {self.level}"