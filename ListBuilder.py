import os
import re
import requests
from pycountry import countries
import CreateCustomPlaylist
import subprocess


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
        "G-platforms",
        "IPTV",
        "Samsung"
    ]
    for i in range(len(names_playlist)):
        # print(f"{i+1}. {names_playlist[i]}")
        return names_playlist


def get_playlist_by_name(name):
    """Get playlist by name or index - Updated to use new .m3u file mapping scheme"""

    # New mapping scheme using .m3u file names
    playlist_mapping = {
        "regular streams": "Regular-Streams.m3u",
        "lg channels": "LG-Channels.m3u",
        "lg channels 2": "LG-Channels-2.m3u",
        "lg channels 3": "LG-Channels-3.m3u",
        "lg channels 4": "LG-Channels-4.m3u",
        "lg channels 5": "LG-Channels-5.m3u",
        "g-platforms": "G-platforms.m3u",
        "iptv": "playlist.m3u",
        "other": "Other.m3u",
        "sports": "Sports.m3u",
        "additional streams": "Additional-Streams.m3u",
        "samsung": "Samsung.m3u"
    }

    name_lower = str(name).lower().strip()
    if name_lower in playlist_mapping:
        return playlist_mapping[name_lower]

    # Return None if playlist not found
    return None


def m3u_parser(chosen_playlist=""):
    
    directory = subprocess.run(
    ['bash', '-c', 'echo $HOME'],
    capture_output=True,
    text=True
    )

    home_base = directory.stdout.strip()
    
    
    # Continue with the rest of the function after valid selection
    with open(f'{home_base}/src/Build-Your-Own-IPTV/{chosen_playlist}', 'r') as file:
        # Step 2: Read the file line by line
        lines = file.readlines()
    # print(file.name)
    # Step 3: Initialize an empty list to store the parsed data
    parsed_data = []

    # Step 4: Iterate through each line in the file
    i = 0

    while i < len(lines):
        line = lines[i].strip()
        if line.startswith('#EXTINF:'):
            simple_format_match = re.search(r'^#EXTINF:-1,(.+)$', line)
            unquoted_format_match = re.search(r'#EXTINF:-1\s+tvg-logo="([^"]*)",(.+)$', line)

            has_tvg_id = 'tvg-id=' in line
            has_group_title = 'group-title=' in line

            if unquoted_format_match:
                # New format: #EXTINF:-1 tvg-logo="..." Channel Name
                tvg_logo = unquoted_format_match.group(1)
                channel_name = unquoted_format_match.group(2).strip()
                parsed_data.append({
                    'tvg_id': '',  # No TVG ID in this format
                    'group_title': '',  # No group title in this format
                    'channel_name': channel_name,
                    'tvg_logo': tvg_logo  # Store logo URL if needed
                })
                # print(f"Channel: {channel_name}")

            if simple_format_match and not has_tvg_id and not has_group_title:
                # Simple format: #EXTINF:-1,Channel Name
                channel_name = simple_format_match.group(1).strip()
                parsed_data.append({
                    'tvg_id': '',  # No TVG ID in this format
                    'group_title': '',  # No group title in this format
                    'channel_name': channel_name,
                })
                # print(f"Channel: {channel_name}")

            # Extract Format name, TV Guide ID, and group title using regex
            match = re.search(r'tvg-id="([^"]*)"', line)
            group_title_match = re.search(r'group-title="([^"]*)"(.*)(,|$)', line)
            channel_name_match = re.search(r',(.*)$', line)
            if match:
                tvg_id = match.groups(0)
                if group_title_match:
                    group_title = group_title_match.group(1)
                    additional_text = group_title_match.group(2).strip()
                    if not group_title and additional_text:
                        group_title = additional_text
                else:
                    group_title = ""

                channel_name = channel_name_match.group(1).strip() if channel_name_match else ""

                if tvg_id:  # Only include channels with TV Guide ID
                    parsed_data.append({
                        'tvg_id': tvg_id,
                        'group_title': group_title.strip(),
                        'channel_name': channel_name,
                    })
                    # print(f"Channel: {channel_name},TV Guide ID: {tvg_id}, Group: {group_title}")

        i += 1

    # Step 6: Save the parsed data to a new file
    with open('parsed_us-channels.txt', 'w') as file:
        file.write('\n'.join([f"{item['channel_name']}, {item['tvg_id']},{item['group_title']} "
                              for item in parsed_data]))
    #
        file.close()

    file.close()
    # Return total number of channels
    # print(f"Total channels in playlist {len(parsed_data)}")
    return parsed_data


# If Interested in filtering channels to see blocklist, uncomment the following lines:
def get_blocklist():
    blocklist_url = "https://iptv-org.github.io/api/blocklist.json"
    response = requests.get(blocklist_url)

    if response.status_code == 200:
        blocklist = response.json()

        # Convert to parsed_data format
        parsed_blocklist = []
        for item in blocklist:
            parsed_blocklist.append({
                'channel_id': item.get('channel', ''),
                'reason': item.get('reason', ''),
            })
        # Print in the same format as your parsed_data
        print(f"\nTotal blocked channels: {len(parsed_blocklist)}")

        for item in parsed_blocklist:
            print(f"Channel: {item['channel_id']}, Reason: {item['reason']}")
    else:
        print(f"Failed to fetch blocklist. Status code: {response.status_code}")
        return {}


def get_country_code():
    search_counter = 0

    # 1. Load the list of countries with their codes
    iptv_countries = requests.get("https://iptv-org.github.io/api/countries.json").json()

    # 2. Generate a list of countries using pycountry (ISO 3166-1 alpha-2)
    country_list = [country.name for country in countries]

    # 3. Pick a country name and find its code
    while True:
        name = input("\nEnter a country name (or type list to see all countries, or type exit): ").strip().lower()

        if name.lower() == 'exit':
            print("\nSwitching Query Mode to Global.")
            break
        elif name.lower() == 'list':
            print("\nAvailable countries:")
            for country in country_list:
                print(country)
            continue

        try:
            # Exception for Russia and United Kingdom
            if name.lower() == "russia":
                country = countries.lookup("Russian Federation")
            else:
                country = countries.lookup(name)

            code = country.alpha_2.lower()

            if country.name == "United Kingdom":
                code = "uk"

            print(f"\nCountry: {country.name}, Country code: {code}")

            # Check if the country is available in IPTV list
            if any(c['code'].lower() == code for c in iptv_countries):
                print("\nThis country is available in the IPTV list.")

            while True:
                type_search = input("\nDo you want to search by channel, or group (or type exit): ").lower()

                if type_search == "exit":
                    break

                if type_search not in ["channels", "groups", "channel", "group"]:
                    print("\nInvalid option. Please choose 'channel', 'group', or 'country'.")
                    continue

                term_search = input(f"\n{country.name}: "f"Enter the {type_search} name you're looking for: ").lower()

                # Build the playlist URL for that country
                playlist_url = f"https://iptv-org.github.io/iptv/countries/{code}.m3u"

                # Download the playlist
                response = requests.get(playlist_url)
                if response.status_code == 200:
                    print(f"\nFound playlist for {country.name}")
                    country_playlist = "playlist.m3u"
                    parsed_data = m3u_parser(country_playlist)

                    filtered_channels = []
                    for channel in parsed_data:
                        if channel['tvg_id'] and re.search(rf'\.{re.escape(code)}$', channel['tvg_id'][0].lower()):
                            if re.search(rf'\b{re.escape(term_search)}', channel['channel_name'].lower()):
                                filtered_channels.append(f"Channel: {channel['channel_name']}")

                    filtered_groups = []
                    for group in parsed_data:
                        if group['tvg_id'] and re.search(rf'\.{re.escape(code)}$', group['tvg_id'][0].lower()):
                            if re.search(rf'\b{re.escape(term_search)}', group['group_title'].lower()):
                                filtered_groups.append(f"Channel: {group['channel_name']}, "
                                                       f"Group: {group['group_title']}")
                    # Print results
                    if type_search in ["channels", "channel"]:
                        if filtered_channels:
                            search_counter += 1
                            print("\nMatching channels:")
                            for channel in filtered_channels:
                                print(channel)
                            # Add in total channel count
                            total_channels = len(filtered_channels)
                            print(f"Total channels: {total_channels}")
                            should_stop = write_search_results_to_file(filtered_channels, [], type_search,
                                                                       search_counter)
                            if should_stop:
                                break

                        else:
                            print("\nChannel not available.")

                    elif type_search in ["groups", "group"]:
                        if filtered_groups:
                            search_counter += 1
                            print("\nMatching Groups:")
                            for group in filtered_groups:
                                print(group)
                            # Add in total group count
                            total_groups = len(filtered_groups)
                            print(f"Total groups: {total_groups}")
                            should_stop = write_search_results_to_file([], filtered_groups, type_search, search_counter)
                            if should_stop:
                                break
                        else:
                            print("\nNo matching groups found.")
                else:
                    print(f"Failed to download playlist for {country.name}.")
        except LookupError:
            print(f"Country '{name}' not found. Please try again.")
            break


def playlist_selection():

    while True:
        playlist_choice = (input("\nEnter a playlist name (or type list to see all playlist, or type exit): ")
                           .strip())
        names_given = playlist_names()

        if playlist_choice.lower() == 'exit':
            print("\nExiting IPTV Builder. Goodbye!")
            exit()

        elif playlist_choice.lower() == 'list':
            print("\nAvailable Playlist:")
            if names_given:
                for i, item in enumerate(names_given, 1):
                    print(f"{i}. {item}")
            continue  # Add this to go back to the prompt

        else:  # Add this else block
            selected_playlist = get_playlist_by_name(playlist_choice)

            if selected_playlist is None:
                print(f"Invalid playlist name: '{playlist_choice}'. Please try again.")
                continue  # Go back to prompt for invalid input
            else:
                # print(f"\nFound playlist: {selected_playlist}")
                return selected_playlist


def write_search_results_to_file(found_channels, found_groups, search_type, counter, filename="search_results.txt"):
    """Write search results to a file, and after 5 searches ask to index"""

    # Append mode to keep building the file
    mode = 'a' if counter > 1 else 'w'

    with open(filename, mode) as file:
        if counter == 1:
            # Write header only on first search
            file.write("# Search Results for SimpleDatabase\n")
            file.write("# Format: ID|Channel_Name|Group_Name\n\n")

        file.write(f"# Search {counter} - Type: {search_type}\n")

        if search_type in ["channels", "channel"] and found_channels:
            for i, channel in enumerate(found_channels, 1):
                channel_name = channel.replace("Channel: ", "").strip()
                # file.write(f"{i}|{channel_name}|Unknown\n")
                if ',' in channel_name:
                    channel_name = channel_name.split(',')[-1].strip()
                file.write(f"{i}|{channel_name}|Unknown\n")

        elif search_type in ["groups", "group"] and found_groups:
            for i, group in enumerate(found_groups, 1):
                parts = group.split(", Group: ")
                if len(parts) == 2:
                    channel_name = parts[0].replace("Channel: ", "").strip()
                    group_name = parts[1].strip()
                    # # Extract channel name after comma if M3U8 syntax is present
                    if ',' in channel_name:
                        channel_name = channel_name.split(',')[-1].strip()
                    file.write(f"{i}|{channel_name}|{group_name}\n")

        file.write("\n")

    # print(f"\nSearch {counter} results written to {filename}")

    # After 5 searches, ask to index
    if counter == 5:
        response = input("\nYou've performed 5 searches! Would you like to index these results? (y/n): ").lower()
        if response == 'y':
            print("Indexing results for SimpleDatabase...")
            from DataBase import SimpleGUI
            app = SimpleGUI()
            app.run()
            return "reset_counter"    # Signal to stop searching
        else:
            print("Continuing searches...")
            return False

    return False


def filter_channels():

    search_counter = 0
    playlist_switched = False
    
    directory = subprocess.run(
    ['bash', '-c', 'echo $HOME'],
    capture_output=True,
    text=True
    )

    home_base = directory.stdout.strip()    

    while True:
        # Step 1: Open the file
        with open(f'{home_base}/src/Build-Your-Own-IPTV/parsed_us-channels.txt', 'r') as file:
            # Step 2: Read the file line by line
            lines = file.readlines()

        which_playlist = f"{home_base}/src/Build-Your-Own-IPTV/which_playlist.txt"

        if not os.path.exists(which_playlist):
            selection_of_playlist = playlist_selection()
            os.system(f'echo {selection_of_playlist} > {which_playlist}')
            parsed_data = m3u_parser(selection_of_playlist)

        if os.path.exists(which_playlist):
            print("\nIf you want to change the playlist, type --> playlist.")
            print("\nUsing Static Playlist For Now")
            with open(which_playlist, 'r') as file:
                static_playlist = file.read().strip()
                print(static_playlist)
                parsed_data = m3u_parser(static_playlist)

        search_type = input("\nDo you want to search by channels, group, country? (or type exit): ").lower()

        if search_type == "exit":
            print("\nExiting IPTV Builder. Goodbye!")
            return []

        if search_type not in ["channels", "groups", "channel", "group", "country", "countries", "playlist"]:
            print("\nInvalid option. Please choose 'channel', 'group', or 'country'.")
            continue

        if search_type in ["playlist"]:
            print("\nSwitching playlist\n")
            if os.path.exists(which_playlist):
                playlist_switched = True
                selection_of_playlist = playlist_selection()
                os.system(f'echo {selection_of_playlist} > {which_playlist}')
                parsed_data = m3u_parser(selection_of_playlist)

                clear_results_file = f'{home_base}/src/Build-Your-Own-IPTV/search_results.txt'
                with open(clear_results_file, 'w') as file:
                    file.write("")

                continue

        # Get user input for search term
        if search_type in ["country", "countries"]:
            print("\nSwitching Query Mode to Region/Country\n")

            change_static_playlist = f'{home_base}/src/Build-Your-Own-IPTV/which_playlist.txt'
            with open(change_static_playlist, 'w') as file:
                file.write("playlist.m3u")
            get_country_code()
            continue

        search_term = input(f"\nEnter the {search_type} name you're looking for: ").lower()

        # Step 3: Filter and print the channel names prompted by the user
        found_channels = []
        for line in lines:
            parts = line.strip().split(', ')
            if len(parts) >= 1:
                channel_name = parts[0]
                # Make the search case-insensitive and match variations
                if re.search(rf'\b{re.escape(search_term)}', channel_name.lower()):
                    # Search by channel
                    found_channels.append(f"Channel: {channel_name}")

        found_groups = []
        for item in parsed_data:
            if re.search(rf'\b{re.escape(search_term)}', item['group_title'].lower()):
                found_groups.append(f"Channel: {item['channel_name']}, Group: {item['group_title']}")

        if playlist_switched:
            search_counter = 4
            playlist_switched = False

        # Print results
        if search_type in ["channels", "channel"]:
            if found_channels:
                print("\nMatching channels:")
                for channel in found_channels:
                    print(channel)

                search_counter += 1
                total_channels = len(found_channels)
                print(f"Total channels: {total_channels}")
                should_stop = write_search_results_to_file(found_channels, [], search_type, search_counter)
                if should_stop == "reset_counter":
                    search_counter = 0  # Reset counter to continue
                elif should_stop:
                    break
            else:
                print("\nChannel not available.")

        elif search_type in ["groups", "group"]:
            if found_groups:
                print("\nMatching Groups:")
                for group in found_groups:
                    print(group)
                # Add in total group count
                search_counter += 1
                total_groups = len(found_groups)
                print(f"Total groups: {total_groups}")
                should_stop = write_search_results_to_file([], found_groups, search_type, search_counter)
                if should_stop == "reset_counter":
                    search_counter = 0  # Reset counter to continue
                elif should_stop:
                    break
            else:
                print("\nNo matching groups found.")

        file.close()
    return []


def reset_playlist():
    """Call this function when executing ListBuilder.py"""

    directory = subprocess.run(
    ['bash', '-c', 'echo $HOME'],
    capture_output=True,
    text=True
    )

    home_base = directory.stdout.strip()

    playlist_path = f"{home_base}/src/Build-Your-Own-IPTV/which_playlist.txt"

    # Remove the existing playlist file if it exists
    if os.path.exists(playlist_path):
        try:
            os.remove(playlist_path)
            # print(f"\nRemoved existing playlist: {playlist_path}")
        except OSError as e:
            print(f"No file to remove: {e}")

    # print("\nPlaylist reset")


# Call the function
if __name__ == '__main__':
    CreateCustomPlaylist.reset_playlist()
    reset_playlist()
    filter_channels()
    # get_blocklist()
