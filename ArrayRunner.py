#!/usr/bin/python3

playlist = [
    "https://www.apsattv.com/localnow.m3u",
    "https://www.apsattv.com/redbox.m3u",
    "https://www.apsattv.com/distro.m3u"
     ]


lg_channels = [
    "https://www.apsattv.com/arlg.m3u",
    "https://www.apsattv.com/atlg.m3u",
    "https://www.apsattv.com/aulg.m3u",
    "https://www.apsattv.com/belg.m3u",
    "https://www.apsattv.com/brlg.m3u"
]

lg_channels_2 = [
    "https://www.apsattv.com/calg.m3u",
    "https://www.apsattv.com/chlg.m3u",
    "https://www.apsattv.com/cllg.m3u",
    "https://www.apsattv.com/colg.m3u",
    "https://www.apsattv.com/delg.m3u"
]

lg_channels_3 = [
    "https://www.apsattv.com/dklg.m3u",
    "https://www.apsattv.com/eslg.m3u",
    "https://www.apsattv.com/filg.m3u",
    "https://www.apsattv.com/frlg.m3u",
    "https://www.apsattv.com/gblg.m3u"
]

lg_channels_4 = [
    "https://www.apsattv.com/ielg.m3u",
    "https://www.apsattv.com/inlg.m3u",
    "https://www.apsattv.com/itlg.m3u",
    "https://www.apsattv.com/jplg.m3u",
    "https://www.apsattv.com/krlg.m3u"
]

lg_channels_5 = [
    "https://www.apsattv.com/lulg.m3u",
    "https://www.apsattv.com/mxlg.m3u",
    "https://www.apsattv.com/nllg.m3u",
    "https://www.apsattv.com/nolg.m3u",
    "https://www.apsattv.com/nzlg.m3u",
    "https://www.apsattv.com/pelg.m3u",
    "https://www.apsattv.com/ptlg.m3u",
    "https://www.apsattv.com/sglg.m3u",
    "https://www.apsattv.com/selg.m3u",
    "https://www.apsattv.com/uslg.m3u"
]

other_platforms = [
    "https://www.apsattv.com/firetv.m3u",
    "https://www.apsattv.com/galxytv.m3u",
    "https://www.apsattv.com/xiaomi.m3u",
    "https://www.apsattv.com/tclplus.m3u",
    "https://www.apsattv.com/tclbr.m3u",
    "https://www.apsattv.com/tcl.m3u",
    "https://www.apsattv.com/tablo.m3u",
    "https://www.apsattv.com/vizio.m3u",
    "https://www.apsattv.com/zeasn.m3u",
    "https://www.apsattv.com/vidaa.m3u"
]

sports_playlist = [
    "https://www.apsattv.com/xumo.m3u",
    "https://www.apsattv.com/sportstv.m3u",
    "https://tvpass.org/playlist/m3u",

]

additional_platforms = [
    "https://www.apsattv.com/klowd.m3u",
    "https://www.apsattv.com/freetv.m3u",
    "https://www.apsattv.com/zeasn.m3u",
    "https://www.apsattv.com/rewardedtv.m3u",
    "https://www.apsattv.com/freemoviesplus.m3u",
    "https://www.apsattv.com/veely.m3u"
]

samsung_channels = [
    "https://www.apsattv.com/ssungnz.m3u",
    "https://www.apsattv.com/ssungaus.m3u",
    "https://www.apsattv.com/ssungsg.m3u",
    "https://www.apsattv.com/ssungph.m3u",
    "https://www.apsattv.com/ssungth.m3u",
    "https://www.apsattv.com/ssungbra.m3u",
    "https://www.apsattv.com/ssungmex.m3u",
    "https://www.apsattv.com/ssungnor.m3u",
    "https://www.apsattv.com/ssungfin.m3u",
    "https://www.apsattv.com/ssungden.m3u",
    "https://www.apsattv.com/ssungswe.m3u",
    "https://www.apsattv.com/ssungpor.m3u",
    "https://www.apsattv.com/ssunglux.m3u",
    "https://www.apsattv.com/ssungbelg.m3u",
    "https://www.apsattv.com/ssungire.m3u",
    "https://www.apsattv.com/ssungneth.m3u"
]


def playlist_names():

    names_playlist = [
        "Regular Streams",
        "LG Channels",
        "LG Channels 2",
        "LG Channels 3",
        "LG Channels 4",
        "LG Channels 5",
        "Other",
        "Sports",
        "Additional Streams",
        "Samsung"
    ]
    for i in range(len(names_playlist)):
        # print(f"{i+1}. {names_playlist[i]}")
        return names_playlist


def get_playlist_by_name(name):
    """Get playlist by name or index"""
    playlist_mapping = {
        "regular streams": playlist,
        "lg channels": lg_channels,
        "lg channels 2": lg_channels_2,
        "lg channels 3": lg_channels_3,
        "lg channels 4": lg_channels_4,
        "lg channels 5": lg_channels_5,
        "other": other_platforms,
        "sports": sports_playlist,
        "additional streams": additional_platforms,
        "samsung": samsung_channels
    }

    name_lower = str(name).lower().strip()
    if name_lower in playlist_mapping:
        return playlist_mapping[name_lower]


if __name__ == "__main__":
    playlist_names()
