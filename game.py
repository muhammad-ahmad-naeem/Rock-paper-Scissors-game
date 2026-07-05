

import random
import tkinter as tk


# ----------------------------------------------------------------------
# COLOUR PALETTE  (warm beige / cream / coffee tones)
# ----------------------------------------------------------------------
BG          = "#F3ECE0"
CARD_BG     = "#FBF7EF"
BORDER      = "#E1D3B8"
ACCENT      = "#B98B4E"
ACCENT_DARK = "#8C6A3B"
TEXT_DARK   = "#4A3B2A"
TEXT_MUTED  = "#8A7A63"
WIN         = "#6E8B4E"
LOSE        = "#B5615B"
TIE         = "#B98B4E"
CHOICE_BG   = "#EFE6D4"
CHOICE_HOVER= "#E6D8BC"
CHOICE_SEL  = "#E4D4AE"
WHITE_TEXT  = "#FFFDF8"

CHOICES = ("rock", "paper", "scissors")
EMOJI = {"rock": "✊", "paper": "✋", "scissors": "✌️"}

BEATS = {  # key beats value
    "rock": "scissors",
    "paper": "rock",
    "scissors": "paper",
}


class RPSApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Rock • Paper • Scissors")
        self.geometry("520x580")
        self.minsize(460, 540)
        self.configure(bg=BG)

        self.wins = 0
        self.losses = 0
        self.ties = 0
        self.choice_buttons = {}

        self._build_layout()

    # ------------------------------------------------------------
    def _build_layout(self):
        outer = tk.Frame(self, bg=BG)
        outer.pack(fill="both", expand=True, padx=26, pady=24)

        tk.Label(
            outer, text="✊✋✌️ Rock Paper Scissors", bg=BG, fg=TEXT_DARK,
            font=("Georgia", 20, "bold")
        ).pack(pady=(0, 4))

        tk.Label(
            outer, text="Pick your move", bg=BG, fg=TEXT_MUTED,
            font=("Helvetica", 11)
        ).pack(pady=(0, 18))

        # Scoreboard
        score_row = tk.Frame(outer, bg=BG)
        score_row.pack(pady=(0, 18))

        self.wins_label = self._score_pill(score_row, "Wins", WIN)
        self.ties_label = self._score_pill(score_row, "Ties", TIE)
        self.losses_label = self._score_pill(score_row, "Losses", LOSE)

        # Result card
        self.card = tk.Frame(
            outer, bg=CARD_BG, highlightbackground=BORDER,
            highlightthickness=1
        )
        self.card.pack(fill="both", expand=True, pady=(0, 20))

        card_inner = tk.Frame(self.card, bg=CARD_BG)
        card_inner.pack(fill="both", expand=True, padx=20, pady=20)

        vs_row = tk.Frame(card_inner, bg=CARD_BG)
        vs_row.pack(fill="x", pady=(6, 6))

        self.player_box = self._reveal_box(vs_row, "You")
        tk.Label(
            vs_row, text="VS", bg=CARD_BG, fg=TEXT_MUTED,
            font=("Georgia", 13, "bold")
        ).pack(side="left", padx=14)
        self.computer_box = self._reveal_box(vs_row, "Computer")

        self.result_label = tk.Label(
            card_inner, text="Make your move to start!", bg=CARD_BG,
            fg=TEXT_MUTED, font=("Helvetica", 14, "bold"), wraplength=420
        )
        self.result_label.pack(pady=(18, 0))

        # Choice buttons
        choice_row = tk.Frame(outer, bg=BG)
        choice_row.pack(pady=(0, 6))

        for choice in CHOICES:
            self._make_choice_button(choice_row, choice)

        # Reset link
        reset_btn = tk.Button(
            outer, text="Reset Score", command=self._reset_score,
            bg=BG, fg=TEXT_MUTED, activebackground=BG,
            activeforeground=TEXT_DARK, font=("Helvetica", 10, "underline"),
            relief="flat", cursor="hand2", bd=0
        )
        reset_btn.pack(pady=(10, 0))

    # ------------------------------------------------------------
    def _score_pill(self, parent, label, colour):
        pill = tk.Frame(parent, bg=CARD_BG, highlightbackground=BORDER,
                         highlightthickness=1)
        pill.pack(side="left", padx=8)

        value = tk.Label(
            pill, text="0", bg=CARD_BG, fg=colour, font=("Georgia", 18, "bold")
        )
        value.pack(padx=18, pady=(8, 0))

        tk.Label(
            pill, text=label, bg=CARD_BG, fg=TEXT_MUTED, font=("Helvetica", 10)
        ).pack(padx=18, pady=(0, 8))

        return value

    # ------------------------------------------------------------
    def _reveal_box(self, parent, title):
        box = tk.Frame(parent, bg=CHOICE_BG, highlightbackground=BORDER,
                        highlightthickness=1)
        box.pack(side="left", fill="both", expand=True)

        tk.Label(
            box, text=title, bg=CHOICE_BG, fg=TEXT_MUTED,
            font=("Helvetica", 10, "bold")
        ).pack(pady=(10, 0))

        emoji_label = tk.Label(
            box, text="❔", bg=CHOICE_BG, fg=TEXT_DARK, font=("Segoe UI Emoji", 34)
        )
        emoji_label.pack(pady=(4, 4))

        name_label = tk.Label(
            box, text="—", bg=CHOICE_BG, fg=TEXT_DARK, font=("Helvetica", 11)
        )
        name_label.pack(pady=(0, 10))

        box.emoji_label = emoji_label
        box.name_label = name_label
        return box

    # ------------------------------------------------------------
    def _make_choice_button(self, parent, choice):
        btn = tk.Frame(
            parent, bg=CHOICE_BG, highlightbackground=BORDER,
            highlightthickness=1, cursor="hand2"
        )
        btn.pack(side="left", padx=8)

        emoji = tk.Label(
            btn, text=EMOJI[choice], bg=CHOICE_BG, font=("Segoe UI Emoji", 30)
        )
        emoji.pack(padx=16, pady=(12, 2))

        name = tk.Label(
            btn, text=choice.capitalize(), bg=CHOICE_BG, fg=TEXT_DARK,
            font=("Helvetica", 11, "bold")
        )
        name.pack(padx=16, pady=(0, 12))

        widgets = (btn, emoji, name)
        self.choice_buttons[choice] = widgets

        for w in widgets:
            w.bind("<Button-1>", lambda e, c=choice: self._play(c))
            w.bind("<Enter>", lambda e, c=choice: self._set_choice_bg(c, CHOICE_HOVER))
            w.bind("<Leave>", lambda e, c=choice: self._set_choice_bg(c, CHOICE_BG))

    # ------------------------------------------------------------
    def _set_choice_bg(self, choice, colour):
        btn, emoji, name = self.choice_buttons[choice]
        btn.configure(bg=colour)
        emoji.configure(bg=colour)
        name.configure(bg=colour)

    # ------------------------------------------------------------
    def _play(self, player_choice):
        computer_choice = random.choice(CHOICES)

        # Update the reveal boxes
        self.player_box.emoji_label.configure(text=EMOJI[player_choice])
        self.player_box.name_label.configure(text=player_choice.capitalize())
        self.computer_box.emoji_label.configure(text=EMOJI[computer_choice])
        self.computer_box.name_label.configure(text=computer_choice.capitalize())

        # Determine outcome
        if player_choice == computer_choice:
            self.ties += 1
            self.result_label.configure(text="🤝 It's a tie!", fg=TIE)
        elif BEATS[player_choice] == computer_choice:
            self.wins += 1
            self.result_label.configure(text="🎉 You win!", fg=WIN)
        else:
            self.losses += 1
            self.result_label.configure(text="💻 Computer wins!", fg=LOSE)

        self.wins_label.configure(text=str(self.wins))
        self.ties_label.configure(text=str(self.ties))
        self.losses_label.configure(text=str(self.losses))

    # ------------------------------------------------------------
    def _reset_score(self):
        self.wins = self.losses = self.ties = 0
        self.wins_label.configure(text="0")
        self.ties_label.configure(text="0")
        self.losses_label.configure(text="0")
        self.result_label.configure(text="Make your move to start!", fg=TEXT_MUTED)
        self.player_box.emoji_label.configure(text="❔")
        self.player_box.name_label.configure(text="—")
        self.computer_box.emoji_label.configure(text="❔")
        self.computer_box.name_label.configure(text="—")


if __name__ == "__main__":
    app = RPSApp()
    app.mainloop()
