import requests
import ArrayRunner


def get_playlist_info():

    # 1. Pick a playlist name and find its code
    while True:
        playlist = input("\nEnter a playlist name (or type list to see all playlist, or type exit): ").strip()
        playlist_names = ArrayRunner.playlist_names()

        if playlist.lower() == 'exit':
            print("\nExiting Playlist Selection.")
            return []

        elif playlist.lower() == 'list':
            print("\nAvailable Playlist:")
            if playlist_names:
                for i, item in enumerate(playlist_names, 1):
                    print(f"{i}. {item}")

        else:
            # Get the actual playlist using the case-insensitive function
            selected_playlist = ArrayRunner.get_playlist_by_name(playlist)
            if selected_playlist is not None:
                # Try to find which playlist was matched
                if playlist_names:
                    for i, name in enumerate(playlist_names, 1):
                        test_playlist = ArrayRunner.get_playlist_by_name(name)
                        if test_playlist is selected_playlist:
                            matched_name = name

                            # Store the playlist URL count
                            url_counter = len(selected_playlist)
                            for x in range(url_counter):
                                # print(f"{x +1}:  {selected_playlist[x]}")
                                playlist_url = f"{selected_playlist[x]}"

                                # Create filename from URL or use a default name
                                new_name = matched_name.replace(' ', '-')
                                filename = f"/home/src/Build-Your-Own-IPTV/{new_name}.m3u"
                                response = requests.get(playlist_url)

                                # Check/Verify URL
                                if response.status_code == 200:
                                    print(f"Playlist verified, CODE:{response.status_code}")

                                    # Download/Write the playlist content to a m3u file
                                    if x == 0:
                                        with open(filename, 'w', encoding='utf-8') as file:
                                            print(f"Downloading {playlist_url}")
                                            file.write(response.text)

                                    if x > 0:
                                        with open(filename, 'a', encoding='utf-8') as file:
                                            print(f"Appending {playlist_url}")
                                            file.write(response.text)
                                            file.close()

                                if not response.status_code == 200:
                                    print(f"Playlist not verified{response.status_code}. Check URL--> {playlist_url}")
                            break

                print(f"Download completed. Saved as {filename}")
                print(f"\nMatched playlist: {matched_name}")
                continue
            else:
                print("\nInvalid option. Please choose from the list of playlist.")
                continue


# Run the program when the script is executed
if __name__ == "__main__":
    get_playlist_info()
