from fsm import TocMachine
def create_machine():
    machine = TocMachine(
        states=["initial", "search_album_by_song", "intro_album","indtro_album_other_song","recommand_song","recommand_song_by_album","random_collect_song","about_jay"],
        transitions=[
            {
                "trigger": "advance",
                "source": "initial",
                "dest": "search_album_by_song",
                "conditions": "is_going_to_search_album_by_song",
            },
            {
                "trigger": "advance",
                "source": "search_album_by_song",
                "dest": "intro_album",
                "conditions": "is_going_to_intro_album",
            },
            {
                "trigger": "advance",
                "source": "search_album_by_song",
                "dest": "indtro_album_other_song",
                "conditions": "is_going_to_indtro_album_other_song",
            },
            {
                "trigger": "advance",
                "source": "initial",
                "dest": "recommand_song",
                "conditions": "is_going_to_recommand_song",
            },
            {
                "trigger": "advance",
                "source": "recommand_song",
                "dest": "recommand_song_by_album",
                "conditions": "is_going_to_recommand_song_by_album",
            },
            {
                "trigger": "advance",
                "source": "recommand_song",
                "dest": "random_collect_song",
                "conditions": "is_going_to_random_collect_song",
            },
            {
                "trigger": "advance",
                "source": "initial",
                "dest": "about_jay",
                "conditions": "is_going_to_about_jay",
            },
            {"trigger": "advance",
            "source": ["search_album_by_song", "intro_album","indtro_album_other_song","recommand_song","recommand_song_by_album","random_collect_song","about_jay"], 
            "dest": "initial",
            "conditions":"is_going_to_initial"
            }
        ],
        initial="initial",
        auto_transitions=False,
        show_conditions=True,
    )
    return machine