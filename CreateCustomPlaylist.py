import os
import ListBuilder


def create_custom_playlist(import_channel, selected_channels=""):
    """
    Read search_results.txt and create a custom M3U playlist
    from matching channels in the source playlist
    """
    directory = subprocess.run(
    ['bash', '-c', 'echo $HOME'],
    capture_output=True,
    text=True
    )

    home_base = directory.stdout.strip()
    
    which_playlist = f"{home_base}/src/Build-Your-Own-IPTV/which_playlist.txt"

    with open(which_playlist, 'r') as file:
        static_playlist = file.read().strip()
        source_playlist = f"{home_base}/src/Build-Your-Own-IPTV/{static_playlist}"
        parsed_data = ListBuilder.m3u_parser(static_playlist)

    # File paths
    search_results_file = f"{home_base}/src/Build-Your-Own-IPTV/search_results.txt"
    output_playlist = f"{home_base}/src/Build-Your-Own-IPTV/custom_playlist.m3u"

    # Check if files exist
    if not os.path.exists(search_results_file):
        print(f"Error: {search_results_file} not found!")
        return False

    # Step 1: Read channel names from search_results.txt
    print("Reading search results...")
    target_channels = []

    with open(search_results_file, 'r', encoding='utf-8') as file:
        for line in file:
            if line.startswith('#') or not line.strip():
                continue

            # Parse format: ID|Channel_Name|Group_Name
            parts = line.strip().split('|')
            if len(parts) >= 2:
                channel_name = parts[1].strip()
                target_channels.append(channel_name.lower())

    print(f"Found {len(target_channels)} channels to search for")
    file.close()

    # Step 3: Find exact matches
    matches = []
    exact_matches = []

    for item in parsed_data:
        channel_name = item['channel_name'].lower()

        # Check for exact matches first
        if channel_name in target_channels:
            matches.append({
                'tvg_id': item['tvg_id'],
                'group_title': item['group_title'],
                'channel':  item['channel_name']
            })
            exact_matches.append(channel_name)

    print(f"\nFound {len(matches)} exact matching channels")

    is_selected_mode = True if selected_channels == "selected_channels" else False

    # Step 3: Create custom playlist using sed to preserve original formatting
    if is_selected_mode:
        
        # Create the playlist header

        if not os.path.exists(output_playlist):
            os.system(f'echo "#EXTM3U" > {output_playlist}')
            print("Created new custom playlist")
        else:
            print("Appending to existing custom playlist")

        # Split the import_channel string into individual channel names
        stripped_names = [name.strip() for name in import_channel.split('\n') if name.strip()]

        for new_name in stripped_names:
            grep_cmd = f'grep -nF ",{new_name}" "{source_playlist}"'
            result = os.popen(grep_cmd).read().strip()

            if result:
                # Split multiple results and take only the first one (in case of duplicates)
                lines = result.split('\n')
                first_match = lines[0]  # Take the first match

                # Extract line number (first part before the colon)
                line_num = int(first_match.split(':')[0])

                print(f"Added: {new_name} (EXTINF line {line_num} + URL line {line_num + 1})")

                # Actually add the lines to the playlist
                sed_cmd = f'sed -n "{line_num},{line_num + 1}p" "{source_playlist}" >> {output_playlist}'
                os.system(sed_cmd)
            else:
                print(f"No exact match found for: {new_name}")

    if not is_selected_mode:
        print("Creating custom playlist....")

        # Create the playlist header

        if not os.path.exists(output_playlist):
            os.system(f'echo "#EXTM3U" > {output_playlist}')
            print("Created new custom playlist")
        else:
            print("Appending to existing custom playlist")

        # For each match, find the line number and extract the EXTINF + URL lines
        for i in range(len(matches)):
            matched = matches[i]["channel"]
            name_channel = matched


            grep_cmd = f'grep -nF ",{name_channel}" "{source_playlist}"'
            result = os.popen(grep_cmd).read().strip()

            if result:
                # Split multiple results and take only the first one (in case of duplicates)
                lines = result.split('\n')
                first_match = lines[0]  # Take the first match

                # Extract line number (first part before the colon)
                line_num = int(first_match.split(':')[0])

                sed_cmd = f'sed -n "{line_num},{line_num + 1}p" "{source_playlist}" >> {output_playlist}'
                os.system(sed_cmd)

            else:
                print(f"No exact match found for: {name_channel}")


def reset_playlist():
    
    directory = subprocess.run(
    ['bash', '-c', 'echo $HOME'],
    capture_output=True,
    text=True
    )

    home_base = directory.stdout.strip()    

    output_playlist = f"{home_base}/src/Build-Your-Own-IPTVcustom-playlist/custom_playlist.m3u"

    # Remove the existing playlist file if it exists
    if os.path.exists(output_playlist):
        try:
            os.remove(output_playlist)
            # print(f"\nRemoved existing playlist")
        except OSError as e:
            print(f"No file to remove: {e}")


if __name__ == "__main__":
    create_custom_playlist("", "")



