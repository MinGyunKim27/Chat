# utils.py

class ChatRoomManager:
    rooms = {}

    @classmethod
    def add_room(cls, room_name):
        if room_name not in cls.rooms:
            cls.rooms[room_name] = set()

    @classmethod
    def remove_room(cls, room_name):
        if room_name in cls.rooms:
            del cls.rooms[room_name]

    @classmethod
    def add_user(cls, room_name, user_id):
        cls.rooms[room_name].add(user_id)

    @classmethod
    def remove_user(cls, room_name, user_id):
        if room_name in cls.rooms and user_id in cls.rooms[room_name]:
            cls.rooms[room_name].remove(user_id)

    @classmethod
    def get_users(cls, room_name):
        return list(cls.rooms.get(room_name, set()))
