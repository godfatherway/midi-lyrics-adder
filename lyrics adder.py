import mido
import os
import tkinter as tk
from tkinter import filedialog

def add_lyrics_to_midi(midi_file, lyrics_file):
    try:
        # Read MIDI file
        midi = mido.MidiFile(midi_file)

        # Read lyrics file
        with open(lyrics_file, 'r', encoding='utf-8') as f:
            lyrics = f.readlines()

        # Melody track is track 1
        melody_track = midi.tracks[0]

        # Associate each line of lyrics with note-on events in the melody track
        lyric_index = 0
        for msg in melody_track:
            if msg.type == 'note_on' and msg.velocity != 0:
                if lyric_index < len(lyrics):
                    # Add lyric event just before the note-on event
                    melody_track.append(mido.MetaMessage('lyrics', text=lyrics[lyric_index].strip(), time=0))
                    lyric_index += 1

        # Save modified MIDI file with the same name
        output_file = os.path.splitext(midi_file)[0] + '_with_lyrics.mid'
        midi.save(output_file)
        print(f"Lyrics added to {output_file}")

    except Exception as e:
        print(f"Error processing {midi_file}: {e}")

def process_files(midi_file, lyrics_file):
    if not midi_file or not lyrics_file:
        print("Please select both MIDI and lyrics files.")
        return

    add_lyrics_to_midi(midi_file, lyrics_file)

def browse_midi_file():
    filename = filedialog.askopenfilename(filetypes=[("MIDI files", "*.mid")])
    if filename:
        midi_entry.delete(0, tk.END)
        midi_entry.insert(0, filename)

def browse_lyrics_file():
    filename = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
    if filename:
        lyrics_entry.delete(0, tk.END)
        lyrics_entry.insert(0, filename)

# Create the main window
window = tk.Tk()
window.title("MIDI Lyrics App")

# Create and pack widgets
midi_label = tk.Label(window, text="Select MIDI File:")
midi_label.pack()

midi_entry = tk.Entry(window, width=50)
midi_entry.pack()

midi_button = tk.Button(window, text="Browse", command=browse_midi_file)
midi_button.pack()

lyrics_label = tk.Label(window, text="Select Lyrics File:")
lyrics_label.pack()

lyrics_entry = tk.Entry(window, width=50)
lyrics_entry.pack()

lyrics_button = tk.Button(window, text="Browse", command=browse_lyrics_file)
lyrics_button.pack()

process_button = tk.Button(window, text="Process Files", command=lambda: process_files(midi_entry.get(), lyrics_entry.get()))
process_button.pack()

window.mainloop()
