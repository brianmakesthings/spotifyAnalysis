def songReleaseDate(df, playlist_dict):
    playlist_dict["release_date"] = df["track"]["album"]["release_date"]