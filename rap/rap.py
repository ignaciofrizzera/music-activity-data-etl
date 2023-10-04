from typing import List, Tuple, Dict
from summarizer.SummarizedTrack import SummarizedTrack
import json

"""
    hand-picked similar rap songs (according to me).
"""

track_ids: List[Tuple[str, str]] = [
    # Circus Maximus. Travis Scott - Black Skinhead. Kanye West
    ("4GL9GMX9t7Qkprvf1YighZ", "722tgOgdIbNe3BEyLnejw4"),
    # 7am. Lil Uzi Vert - OMG. YoungManny
    ("4v1P7JCjehbg5TmLQo2mFy","1ykGZL7hd9Vkzqe65JzK9d"),
    # Isis. Joyner Lucas, Logic - Icon. Jaden
    ("4h7qcXBtaOJnmrapxoWxGf", "22nyEAEM29tcBRhukR089b"),
    # Hold That Heat. Southside, Future, Travis Scott - 100it Racks. Future, 2 Chainz, Drake 
    ("6OrTKLtcF7EBayOV2QqkSK", "1XWcdNQvGrX32fH09CwuWI"),
    # Benzo. $NOT - Crazy Story. King Von
    ("6zBo3unZdPNthEENHgjVko", "1BNvadXnbiSf3ZofMMdDYK"),
    # Blow the Whistle. Too $hort - For Free. Drake, DJ Khaled
    ("2lMg3lCMOGistaWBNGjuT3", "20bLudc6r1NChyZcrjRd7T"),
    # First Off. Future, Travis Scott - Lil Baby. Young Thug
    ("3WRIaWsws011vHMd9uzPjG", "1MGWgLxUXDodD8Tw8TFppN"),
    # I Try. Trippie Redd - I Try / ++Luv $ick. Kid Buu
    ("4LM5AgiA94oHVtalcwaTRm", "1AezbMAFwI45ay9eLTcBWS"),
    # Dead Roses. Kid Buu - H0. LO VOLF, HAIF HAIF, CHANGMO, DUSTYY HAN
    ("5CDbBUBP3NLNwaBrVrGuTQ", "3W9asoLajjNjw60uASPCfn"),
    # Magic. Lil Skies - 21. DaBaby
    ("5NqOsPI4rA9Bl6LcCftzI2", "1AdXchAT6hBUm5d6y4nKjI"),
    # Magic. Lil Skies - Butterfly Effect. Travis Scott
    ("5NqOsPI4rA9Bl6LcCftzI2", "2cYqizR4lgvp4Qu6IQ3qGN"),
    # Holy Moly. Blueface, NLE Choppa - Vibes. Blueface
    ("3wapLdXDMiCZV9dWNg55Jh", "1uejyk6mEg70MhFQaUphJu"),
    # Shotta Flow. NLE Choppa - Rangos. Pekeño 77
    ("4dAMdQ6g4kGmnc1MDHsg77", "0ZeQFWUwICisBLXNFtlsAY"),
    # Sanguine Paradise. Lil Uzi Vert - Do It. Mykko Montana, K CAMP
    ("3XiNC94b4Tq1xwv70sQJGN", "7yORNsKrSxLIV7qqRFySXl"),
    # Butterfly Effect. Travis Scott - Souvenir. Eno
    ("2cYqizR4lgvp4Qu6IQ3qGN", "5A2GDu00u74QrfSP3ca5s7"),
    # No Way. Kynda Gray - rockstar. Post Malone, 21 Savage 
    ("5hM4s6Q03mLtsWXYR52foJ", "0e7ipj03S05BNilyu5bRzt"),
    # False Prophets. J. Cole - Coffee Bean. Travis Scott
    ("0eneujAc4PxkdjP25Gsue1", "6vnfObZ4Ys70SBAtti1xZ9"),
    # Look At Me!. XXXTENTACION - The Plan. G-Eazy 
    ("7floNISpH8VF4z4459Qo18", "7fOPVfABNLg3sxtgXBhBdp"),
    # Take A Step Back. XXXTENTACION, Ski Mask The Slump God - Buba. 6ix9ine
    ("2gQYziDV5cSTRSqr6akzi5", "0ZWvo02qugJAKf2HjdD4fT"),
    # Side To Side. Three 6 Mafia - Powerglide. Rae Sremmurd, Swa Lee, Slim Jxmmi, Juicy J
    ("1GkVc70dOVg9Ihon17Wm4A", "1BuZAIO8WZpavWVbbq3Lci"),
    # Plain Jane. A$AP Ferg - Slob On My Knob. Tear Da Club Up Thugs 
    ("4dVpf9jZjcORqGTLUaeYj9", "60TbmViml7n1jUZksLR7Mq"),
    # U.E.N.O. Rick Ross, Future, Rocko - U.E.N.O. Rocko, Future, A$AP Rocky
    ("0HFrCOmhCYXlv4NdEwRAuj", "1baooPNpHuiV81mVg5yjVO"),
    # The Spins. Mac Miller - Half Mast. Empire of the Sun
    ("51pshtuYkgUQnt5huMPbKL", "49Hkgl03InFFqBklOQxunt"),
    # Stop Breathing. Playboi Carti - Hit. DaBaby, YoungBoy Never Broke Again
    ("2lLG56qpLP3UbcLuzMvkWX", "4TfEcrA3VitAQ9ft91e5pQ"),
    # 5% TINT. Travis Scott - Cell Therapy. Goodie Mob
    ("11kDth1aKUEUMq9r1pqyds", "5wvxRlpUTSX9CE52yFZsIY"),
    # Letter To My Daughter. NLE Choppa - Valuable Pain. YoungBoy Never Broke Again 
    ("0WMBOtNqkWH6FUiXDNJ7kK", "61Oo3DUJubecZQosjho6Pp"),
    # Having My Way. Lil Skies, Lil Durk - Nobody Safe. Trilla Venus
    ("3TcKJZF01kCz0yyadk3gsI", "1Zg35klf7EnJvLN9SFXt8G"),
    # LSD. Jaythenolife - Dook. Lil Droptop Golf Cart
    ("6EmCPnzF3jqyXsOlF01G5y", "7MJW2vaxAFUKi9sDhR0XUf"),
    # Hide It In My Sock. Lil Stitch - Magnolia. Playboi Carti
    ("2LwjbcLehYt05GUbs7mDPM", "1e1JKLEDKP7hEQzJfNAgPl"),
    # CS. Lil Uzi Vert - Chop Suey. System of a Down        -> cover
    ("0ZpH1PMorID9D4cRCnxpPL", "2DlHlPMa4M17kufBvI2lEN"),
    #
]

"""
    Notes.
    Some features to add?:
        - interpolation? if song1 or song2 interpolate each other
        - sample? if song1 or song2 sample each other
            ^ we can get this from the genius API i believe.
"""

def run_similar_rap_data():
    songs: List[Tuple[Dict, Dict]] = []
    for tracks_tuple in track_ids:
        track_one, track_two = tracks_tuple
        track_one_summarized = SummarizedTrack(track_one)
        track_two_summarized = SummarizedTrack(track_two)
        # Each entry of the "dataset" has to be two songs that are similar
        songs.append((track_one_summarized.data, track_two_summarized.data))
    
    data = {'songs': songs}
    with open('rap/similar_rap_data.json', 'w') as fp:
        json.dump(data, fp, indent=3)
