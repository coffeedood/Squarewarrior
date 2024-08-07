
userinput = input("type playlist or musicplayer")
if userinput == "playlist":
    import os
    import urllib.parse
    import tkinter as tk
    from tkinter import filedialog, messagebox, scrolledtext
    from natsort import natsorted
    import os
    import tkinter as tk
    from tkinter import filedialog, messagebox
    import urllib.parse
    from natsort import natsorted  # You may need to install this package: pip install natsort
    import string  # Import string module for character validation

    import os
    import tkinter as tk
    from tkinter import filedialog, messagebox
    import urllib.parse
    from natsort import natsorted  # You may need to install this package: pip install natsort
    import string  # Import string module for character validation

    MAX_FILENAME_LENGTH = 245  # Maximum length for playlist filenames

    import os
    import tkinter as tk
    from tkinter import filedialog, messagebox
    import urllib.parse
    from natsort import natsorted  # You may need to install this package: pip install natsort
    import string  # Import string module for character validation
    import os
    import re
    import urllib.parse
    import string
    import tkinter as tk
    from tkinter import filedialog, scrolledtext, messagebox
    from natsort import natsorted
    import pygame

    MAX_FILENAME_LENGTH = 245  # Maximum length for playlist filenames

    class MusicPlaylistGenerator:
        def __init__(self):
            self.music_source_dir = ""
            self.playlist_dest_dir = ""

        def set_directories(self, music_source_dir, playlist_dest_dir):
            self.music_source_dir = music_source_dir
            self.playlist_dest_dir = playlist_dest_dir

        def create_artist_playlists_from_folder(self):
            try:
                if not os.path.exists(self.music_source_dir) or not os.path.isdir(self.music_source_dir):
                    print(f"Error: Music source directory '{self.music_source_dir}' not found.")
                    return False

                if not os.path.exists(self.playlist_dest_dir):
                    os.makedirs(self.playlist_dest_dir)

                artist_playlists = {}

                # Walk through the music source directory
                for root, dirs, files in os.walk(self.music_source_dir):
                    for file in files:
                        if file.lower().endswith('.aif') or file.lower().endswith('.aiff'):
                            artist_name = os.path.basename(os.path.dirname(root))
                            if artist_name not in artist_playlists:
                                artist_playlists[artist_name] = []

                            song_path = os.path.abspath(os.path.join(root, file))
                            encoded_path = urllib.parse.quote(song_path)

                            # Add the song to the artist's playlist
                            artist_playlists[artist_name].append(f'file:///{encoded_path}')

                # Create or update playlists for each artist
                for artist_name, songs in artist_playlists.items():
                    # Sort songs naturally
                    songs = natsorted(songs)

                    # Create the playlist title and file name
                    playlist_title = f'{artist_name}'
                    playlist_name = self.sanitize_playlist_name(playlist_title)
                    playlist_name = playlist_name[:MAX_FILENAME_LENGTH - len('.m3u')]
                    playlist_path = os.path.join(self.playlist_dest_dir, f'{playlist_name}.m3u')

                    # Write playlist file
                    with open(playlist_path, 'w', encoding='utf-8') as playlist_file:
                        for song in songs:
                            playlist_file.write(f'# Song: {os.path.basename(urllib.parse.unquote(song))}\n')
                            playlist_file.write(f'{song}\n')

                    print(f"Written artist playlist to {playlist_name}.m3u")

                return True

            except Exception as e:
                print(f"Error occurred while creating artist playlists: {e}")
                return False

        def create_album_playlists_from_folder(self):
            try:
                if not os.path.exists(self.music_source_dir) or not os.path.isdir(self.music_source_dir):
                    print(f"Error: Music source directory '{self.music_source_dir}' not found.")
                    return False

                if not os.path.exists(self.playlist_dest_dir):
                    os.makedirs(self.playlist_dest_dir)

                for root, dirs, files in os.walk(self.music_source_dir):
                    songs = [file for file in files if file.lower().endswith(('.aif', '.aiff')) and not file.startswith('._')]
                    if songs:
                        artist_name = os.path.basename(os.path.dirname(root))
                        album_name = os.path.basename(root)

                        songs = natsorted(songs)

                        playlist_title = f'{album_name} {artist_name}'
                        playlist_name = self.sanitize_playlist_name(playlist_title)
                        playlist_name = playlist_name[:MAX_FILENAME_LENGTH - len('.m3u')]

                        song_playlist_path = os.path.join(self.playlist_dest_dir, f'{playlist_name}.m3u')
                        with open(song_playlist_path, 'w', encoding='utf-8') as song_playlist_file:
                            for song in songs:
                                title = os.path.splitext(song)[0]
                                encoded_path = urllib.parse.quote(os.path.abspath(os.path.join(root, song)))
                                song_playlist_file.write(f'# Song: {title}\n')
                                song_playlist_file.write(f'file:///{encoded_path}\n')
                                self.create_individual_song_playlist(title, os.path.abspath(os.path.join(root, song)))
                        print(f"Written album playlist to {playlist_name}.m3u")

                return True

            except Exception as e:
                print(f"Error occurred while creating album playlists: {e}")
                return False

        def create_song_playlists_from_folder(self):
            try:
                if not os.path.exists(self.music_source_dir) or not os.path.isdir(self.music_source_dir):
                    print(f"Error: Music source directory '{self.music_source_dir}' not found.")
                    return False

                if not os.path.exists(self.playlist_dest_dir):
                    os.makedirs(self.playlist_dest_dir)

                for root, dirs, files in os.walk(self.music_source_dir):
                    songs = [file for file in files if file.lower().endswith(('.aif', '.aiff')) and not file.startswith('._')]
                    if songs:
                        artist_name = os.path.basename(os.path.dirname(root))
                        album_name = os.path.basename(root)

                        # Sort the songs using natural sorting
                        songs = natsorted(songs)

                        for i, song in enumerate(songs):
                            title = os.path.splitext(song)[0]
                            playlist_title = f'{title} {album_name} {artist_name}appended'
                            playlist_name = playlist_title[:MAX_FILENAME_LENGTH - len('.m3u')]

                            song_playlist_path = os.path.join(self.playlist_dest_dir, f'{playlist_name}.m3u')
                            with open(song_playlist_path, 'w', encoding='utf-8') as song_playlist_file:
                                for next_song in songs[i:] + songs[:i]:
                                    next_title = os.path.splitext(next_song)[0]
                                    next_playlist_title = f'{next_title} {album_name} {artist_name}appended'
                                    next_playlist_name = next_playlist_title[:MAX_FILENAME_LENGTH - len('.m3u')]
                                    encoded_path = urllib.parse.quote(os.path.abspath(os.path.join(root, next_song)))

                                    song_playlist_file.write(f'# Song: {next_title}\n')
                                    song_playlist_file.write(f'file:///{encoded_path}\n')

                                print(f"Written to {playlist_name}.m3u")

                return True

            except Exception as e:
                print(f"Error occurred while creating song playlists: {e}")
                return False

        def create_individual_song_playlist(self, song_title, song_path):
            try:
                playlist_name = self.sanitize_playlist_name(song_title)
                playlist_name = playlist_name[:MAX_FILENAME_LENGTH - len('.m3u')]
                song_playlist_path = os.path.join(self.playlist_dest_dir, f'{playlist_name}.m3u')

                with open(song_playlist_path, 'w', encoding='utf-8') as song_playlist_file:
                    title = os.path.splitext(os.path.basename(song_path))[0]
                    encoded_path = urllib.parse.quote(song_path)
                    song_playlist_file.write(f'# Song: {title}\n')
                    song_playlist_file.write(f'file:///{encoded_path}\n')

                print(f"Written individual song playlist to {playlist_name}.m3u")

                return True

            except Exception as e:
                print(f"Error occurred while creating individual song playlist: {e}")
                return False

        def sanitize_playlist_name(self, name):
            valid_chars = '-_.() %s%s' % (string.ascii_letters, string.digits)
            return ''.join(c for c in name if c in valid_chars)


    class MusicPlayerGUI(tk.Tk):
        def __init__(self):
            super().__init__()
            self.title("Music Playlist Generator")
            self.geometry("600x400")

            self.playlist_generator = MusicPlaylistGenerator()

            # Directory selection labels and buttons
            self.lbl_music_source = tk.Label(self, text="Select Music Source Directory:")
            self.lbl_music_source.pack(pady=10)

            self.btn_select_music_source = tk.Button(self, text="Select Folder", command=self.select_music_source)
            self.btn_select_music_source.pack(pady=5)

            self.lbl_playlist_dest = tk.Label(self, text="Select Playlist Destination Directory:")
            self.lbl_playlist_dest.pack(pady=10)

            self.btn_select_playlist_dest = tk.Button(self, text="Select Folder", command=self.select_playlist_dest)
            self.btn_select_playlist_dest.pack(pady=5)

            # Buttons for generating playlists
            self.btn_generate_artist_playlists = tk.Button(self, text="Generate Artist Playlists", command=self.generate_artist_playlists)
            self.btn_generate_artist_playlists.pack(pady=5)

            self.btn_generate_album_playlists = tk.Button(self, text="Generate Album Playlists", command=self.generate_album_playlists)
            self.btn_generate_album_playlists.pack(pady=5)

            self.btn_generate_song_playlists = tk.Button(self, text="Generate Song Playlists", command=self.generate_song_playlists)
            self.btn_generate_song_playlists.pack(pady=5)

            self.txt_output = scrolledtext.ScrolledText(self, width=70, height=10)
            self.txt_output.pack(pady=10)

        def select_music_source(self):
            self.music_source_dir = filedialog.askdirectory()
            if self.music_source_dir:
                self.lbl_music_source.config(text=f"Music Source Directory: {self.music_source_dir}")
                self.playlist_generator.music_source_dir = self.music_source_dir

        def select_playlist_dest(self):
            self.playlist_dest_dir = filedialog.askdirectory()
            if self.playlist_dest_dir:
                self.lbl_playlist_dest.config(text=f"Playlist Destination Directory: {self.playlist_dest_dir}")
                self.playlist_generator.playlist_dest_dir = self.playlist_dest_dir

        def generate_artist_playlists(self):
            success = self.playlist_generator.create_artist_playlists_from_folder()
            messagebox.showinfo("Info", "Artist playlists generated successfully!" if success else "Failed to generate artist playlists.")
            self.log_output("Artist playlists generation completed.")

        def generate_album_playlists(self):
            success = self.playlist_generator.create_album_playlists_from_folder()
            messagebox.showinfo("Info", "Album playlists generated successfully!" if success else "Failed to generate album playlists.")
            self.log_output("Album playlists generation completed.")

        def generate_song_playlists(self):
            success = self.playlist_generator.create_song_playlists_from_folder()
            messagebox.showinfo("Info", "Song playlists generated successfully!" if success else "Failed to generate song playlists.")
            self.log_output("Song playlists generation completed.")

        def log_output(self, message):
            self.txt_output.insert(tk.END, message + '\n')
            self.txt_output.yview(tk.END)


    if __name__ == "__main__":
        pygame.mixer.init()
        app = MusicPlayerGUI()
        app.mainloop()

else:
    import os
    import random
    import threading
    import tkinter as tk
    from tkinter import filedialog, scrolledtext
    import pygame
    import urllib.parse
    import string
    from difflib import SequenceMatcher  # For finding closest match

    MAX_FILENAME_LENGTH = 245  # Maximum length for playlist filenames

    class MusicPlayer:
        def __init__(self):
            self.playlists_history = []  # To keep track of played playlists
            self.current_playlist = []   # To store the current playlist being played
            self.current_index = 0       # Index of the current song in the playlist
            self.playlist_path = ""      # Path of the current playlist file
            self.paused = False          # Flag to indicate if music is paused
            self.running = True          # Flag to indicate if the player is running
            self.volume = 0.5            # Initial volume setting (0.0 to 1.0)

            self.track_finished_thread = threading.Thread(target=self.track_finished_event)
            self.track_finished_thread.start()  # Start the track monitoring thread

        def load_playlist(self, playlist_path):
            try:
                if not os.path.isfile(playlist_path):
                    print(f"Error: Playlist file '{playlist_path}' not found.")
                    return False

                self.stop()  # Stop current playing
                self.current_playlist.clear()  # Clear current playlist
                self.current_index = 0  # Reset current index
                self.playlist_path = playlist_path  # Track current playlist path

                with open(playlist_path, 'r', encoding='utf-8') as f:
                    lines = f.readlines()
                    for line in lines:
                        line = line.strip()
                        if line.startswith('#EXTM3U') or line.startswith('#EXTINF'):
                            continue  # Skip m3u header and info lines
                        elif line.startswith('# Song:'):
                            continue  # Skip specific comment lines
                        elif line.startswith('file://'):
                            media_path = line.replace('file:///', '')
                            media_path = urllib.parse.unquote(media_path)  # Decode URL encoding
                            if os.path.exists(media_path):
                                self.current_playlist.append(media_path)
                            else:
                                print(f"Skipping unknown or inaccessible file: {media_path}")
                        else:
                            print(f"Skipping unrecognized entry in playlist: {line}")

                if self.current_playlist:
                    print(f"Playlist '{os.path.basename(playlist_path)}' loaded successfully.")
                    self.update_playlists_history()  # Update history with the current playlist
                    self.play()
                    return True
                else:
                    print(f"No valid media files found in playlist '{os.path.basename(playlist_path)}'.")
                    return False

            except Exception as e:
                print(f"Error occurred while loading playlist '{playlist_path}': {e}")
                return False

        def play(self):
            if not self.current_playlist:
                print("Playlist is empty. Load a playlist first.")
                return

            if self.paused:
                pygame.mixer.music.unpause()
                self.paused = False
                print(f"Resumed playing: {os.path.basename(self.current_playlist[self.current_index])}")
            else:
                pygame.mixer.music.load(self.current_playlist[self.current_index])
                pygame.mixer.music.set_volume(self.volume)  # Set initial volume
                pygame.mixer.music.play()
                print(f"Now playing: {os.path.basename(self.current_playlist[self.current_index])}")

        def pause(self):
            if pygame.mixer.music.get_busy():
                pygame.mixer.music.pause()
                self.paused = True
                print("Music paused.")

        def stop(self):
            pygame.mixer.music.stop()
            self.paused = False
            print("Music stopped.")

        def next_track(self):
            if not self.current_playlist:
                print("Playlist is empty. Load a playlist first.")
                return

            # Check if there's another track in the current playlist
            while self.current_index + 1 < len(self.current_playlist):
                self.current_index += 1
                next_track_path = self.current_playlist[self.current_index]
                if os.path.exists(next_track_path):
                    self.play()
                    return next_track_path
                else:
                    print(f"Skipping unknown or inaccessible file: {next_track_path}")

            # If no valid next track found, move to the next playlist in history
            self.advance_history()

            # Play the track from the new playlist or update history accordingly
            if self.current_playlist:
                self.play()
                return self.current_playlist[self.current_index]
            else:
                print("No next track or playlist in history.")

        def previous_track(self):
            if not self.current_playlist:
                print("Playlist is empty. Load a playlist first.")
                return

            # Check if there's a previous track in the current playlist
            if self.current_index > 0:
                self.current_index -= 1
            else:
                # Move to the previous playlist in history
                self.rewind_history()

            # Play the previous track
            self.play()

            return self.current_playlist[self.current_index]

        def advance_history(self):
            # Move to the next playlist in history
            if self.playlists_history:
                self.playlists_history.append(self.playlists_history.pop(0))  # Move first element to the end
                self.current_playlist, self.current_index = self.playlists_history[0]
                print(f"Now playing: {os.path.basename(self.current_playlist[self.current_index])}")
            else:
                print("No next track or playlist in history.")

        def rewind_history(self):
            # Move to the previous playlist in history
            if self.playlists_history:
                self.playlists_history.insert(0, self.playlists_history.pop())  # Move last element to the beginning
                self.current_playlist, self.current_index = self.playlists_history[0]
                print(f"Previous track: {os.path.basename(self.current_playlist[self.current_index])}")
            else:
                print("No previous track or playlist in history.")

        def track_finished_event(self):
            while self.running:
                if pygame.mixer.music.get_busy() == 0 and not self.paused:
                    self.next_track()
                pygame.time.wait(1000)  # Wait for 1 second between checks

        def quit(self):
            self.running = False

        def set_volume(self, volume):
            self.volume = volume
            if pygame.mixer.music.get_busy():
                pygame.mixer.music.set_volume(self.volume)
                print(f"Volume set to: {self.volume:.1f}")

        def get_volume(self):
            return self.volume

        def update_playlists_history(self):
            # Store the current playlist and current song index in the history
            self.playlists_history.append((self.current_playlist.copy(), self.current_index))

        def sanitize_playlist_name(self, playlist_title):
            valid_chars = '-_.() %s%s' % (string.ascii_letters, string.digits)
            return ''.join(c for c in playlist_title if c in valid_chars)


    class MusicPlayerGUI:
        def __init__(self, root):
            self.root = root
            self.root.title("Music Player")
            self.root.geometry("800x600")

            self.selected_folder = ""
            self.player = MusicPlayer()

            self.create_widgets()

        def create_widgets(self):
            self.btn_select_folder = tk.Button(self.root, text="Select Playlist Folder", command=self.select_playlist_folder)
            self.btn_select_folder.pack(pady=10)

            self.search_label = tk.Label(self.root, text="Search Playlist Title:")
            self.search_label.pack()

            self.search_entry = tk.Entry(self.root)
            self.search_entry.pack(pady=5)
            self.search_entry.bind("<Return>", lambda event: self.search_playlist())  # Bind <Return> key to search function

            self.btn_search = tk.Button(self.root, text="Search Playlist", command=self.search_playlist)
            self.btn_search.pack(pady=5)

            self.btn_load_playlist = tk.Button(self.root, text="Load Playlist", command=self.load_playlist)
            self.btn_load_playlist.pack(pady=10)

            self.btn_previous_track = tk.Button(self.root, text="Previous Track", command=self.previous_track)
            self.btn_previous_track.pack(pady=5)

            self.btn_next_track = tk.Button(self.root, text="Next Track", command=self.next_track)
            self.btn_next_track.pack(pady=5)

            self.btn_pause = tk.Button(self.root, text="Pause", command=self.pause)
            self.btn_pause.pack(pady=5)

            self.btn_play = tk.Button(self.root, text="Play", command=self.play)
            self.btn_play.pack(pady=5)

            self.btn_stop = tk.Button(self.root, text="Stop", command=self.stop)
            self.btn_stop.pack(pady=5)

            self.btn_play_random = tk.Button(self.root, text="Play Random Song", command=self.play_random_song)
            self.btn_play_random.pack(pady=5)

            self.volume_scale = tk.Scale(self.root, from_=0.0, to=1.0, resolution=0.1, orient=tk.HORIZONTAL,
                                        label="Volume", command=self.set_volume)
            self.volume_scale.set(self.player.get_volume())
            self.volume_scale.pack(pady=10)

            self.text_widget = scrolledtext.ScrolledText(self.root, width=80, height=20, wrap=tk.WORD)
            self.text_widget.pack(pady=10, padx=10)

        def select_playlist_folder(self):
            self.selected_folder = filedialog.askdirectory()
            self.text_widget.insert(tk.END, f"Selected folder: {self.selected_folder}\n")

        def load_playlist(self):
            playlist_name = self.search_entry.get().strip()
            if not playlist_name:
                self.text_widget.insert(tk.END, "Please enter a playlist name to load.\n")
                return

            sanitized_name = self.player.sanitize_playlist_name(playlist_name)
            playlist_path = os.path.join(self.selected_folder, f"{sanitized_name}.m3u")
            if not os.path.isfile(playlist_path):
                self.text_widget.insert(tk.END, f"Playlist '{playlist_name}' not found in '{self.selected_folder}'.\n")
                return

            if self.player.load_playlist(playlist_path):
                self.text_widget.insert(tk.END, f"Playlist '{os.path.basename(playlist_path)}' loaded.\n")
                self.update_history_file(playlist_name)
            else:
                self.text_widget.insert(tk.END, "Failed to load playlist.\n")

        def search_playlist(self, event=None):
            if not self.selected_folder:
                self.text_widget.insert(tk.END, "Please select a playlist folder first.\n")
                return

            search_title = self.search_entry.get().strip()
            if not search_title:
                self.text_widget.insert(tk.END, "Please enter a title to search.\n")
                return

            self.text_widget.insert(tk.END, f"Searching playlists for: {search_title}\n")
            search_thread = threading.Thread(target=self.search_playlists_thread, args=(search_title,))
            search_thread.start()

        def search_playlists_thread(self, search_title):
            playlists = []
            for root, dirs, files in os.walk(self.selected_folder):
                for file in files:
                    if file.endswith(".m3u"):
                        playlists.append(os.path.join(root, file))

            closest_match = self.find_closest_match(playlists, search_title)
            if closest_match:
                self.text_widget.insert(tk.END, f"Closest match found: {os.path.basename(closest_match)}\n")
                if self.player.load_playlist(closest_match):
                    self.search_entry.delete(0, tk.END)  # Clear the search entry after loading successfully
                    self.update_history_file(os.path.splitext(os.path.basename(closest_match))[0])
            else:
                self.text_widget.insert(tk.END, f"No playlists found in '{self.selected_folder}'.\n")

        def find_closest_match(self, playlists, search_title):
            closest_match = None
            max_similarity = -1

            for playlist in playlists:
                filename = os.path.basename(playlist)
                similarity = SequenceMatcher(None, search_title.lower(), filename.lower()).ratio()
                if similarity > max_similarity:
                    max_similarity = similarity
                    closest_match = playlist

            return closest_match

        def play_random_song(self):
            if not self.selected_folder:
                self.text_widget.insert(tk.END, "Please select a playlist folder first.\n")
                return

            history_playlist = os.path.join(self.selected_folder, "history.m3u")
            if not os.path.isfile(history_playlist):
                self.text_widget.insert(tk.END, f"Error: 'history.m3u' playlist not found in {self.selected_folder}.\n")
                return

            with open(history_playlist, 'r', encoding='utf-8') as f:
                lines = f.readlines()
                valid_playlists = []
                for line in lines:
                    line = line.strip()
                    if line.startswith('# Playlist:'):
                        playlist_name = line[len('# Playlist:'):].strip()
                        sanitized_name = self.player.sanitize_playlist_name(playlist_name)
                        playlist_path = os.path.join(self.selected_folder, f"{sanitized_name}.m3u")
                        if os.path.isfile(playlist_path):
                            valid_playlists.append(playlist_path)

                if valid_playlists:
                    random_playlist = random.choice(valid_playlists)
                    if self.player.load_playlist(random_playlist):
                        self.text_widget.insert(tk.END, f"Playing random song from '{os.path.basename(random_playlist)}'.\n")
                        # Do not update history for random songs
                else:
                    self.text_widget.insert(tk.END, f"No valid playlists found in 'history.m3u'.\n")

        def previous_track(self):
            self.player.previous_track()
            if self.player.current_playlist:
                self.text_widget.insert(tk.END, f"Previous track: {os.path.basename(self.player.current_playlist[self.player.current_index])}\n")

        def next_track(self):
            next_track = self.player.next_track()
            if next_track:
                self.text_widget.insert(tk.END, f"Now playing: {os.path.basename(next_track)}\n")

        def pause(self):
            self.player.pause()
            self.text_widget.insert(tk.END, "Music paused.\n")

        def play(self):
            self.player.play()
            self.text_widget.insert(tk.END, "Music playing.\n")

        def stop(self):
            self.player.stop()
            self.text_widget.insert(tk.END, "Music stopped.\n")

        def set_volume(self, volume):
            self.player.set_volume(float(volume))

        def run(self):
            self.root.mainloop()

        def update_history_file(self, playlist_title):
            if playlist_title.startswith("Random Song from"):
                # Skip updating history for random songs
                return

            history_playlist = os.path.join(self.selected_folder, "history.m3u")
            playlist_entry = f"# Playlist: {playlist_title}\n"

            # Check if playlist title already exists in history.m3u
            if os.path.isfile(history_playlist):
                with open(history_playlist, 'r', encoding='utf-8') as f:
                    lines = f.readlines()
                
                if playlist_entry in lines:
                    return  # Playlist entry already exists, no need to append

            # Append playlist entry to history.m3u
            with open(history_playlist, 'a', encoding='utf-8') as f:
                f.write(playlist_entry)

        def stop_music(self):
            self.player.stop()
            self.root.destroy()


    if __name__ == "__main__":
        pygame.init()
        root = tk.Tk()
        app = MusicPlayerGUI(root)
        app.run()
