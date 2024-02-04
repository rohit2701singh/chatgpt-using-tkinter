from tkinter import *
from tkinter.scrolledtext import ScrolledText
from openai import OpenAI

message_box = [
            {"role": "system", "content": "You are a kind helpful assistant."},
        ]


class ChatBot:
    def __init__(self, api_key, theme_color="grey", text_size=13):

        label_font = ("times new roman", 15, "bold")
        button_font = ("times new roman", 13)
        text_font = ("georgia", text_size)

        self.theme_color = theme_color
        self.api_key = api_key
        self.text_size = text_size

        # ui
        self.window = Tk()
        self.window.title("Chatty")
        photo = PhotoImage(file="bot.png")
        self.window.iconphoto(False, photo)
        self.window.config(padx=20, pady=20, bg=self.theme_color)
        self.window.resizable(width=0, height=0)

        self.user_label = Label(text="what you want to do:", bg=self.theme_color, fg="white", font=label_font, )
        self.user_label.grid(row=0, column=0, columnspan=2, sticky="w", pady=(0, 5))

        self.radio_state = IntVar()
        self.radiobutton1 = Radiobutton(text="Chat", value=1, justify="center", variable=self.radio_state, highlightthickness=0, width=10, font=button_font)
        self.radiobutton2 = Radiobutton(text="Img Generate", value=2, justify="center", variable=self.radio_state, highlightthickness=0, width=10, font=button_font)
        self.radiobutton1.grid(row=1, column=0,)
        self.radiobutton2.grid(row=1, column=1,)

        self.user_label = Label(text="User:", bg=self.theme_color, fg="white", font=label_font,)
        self.user_label.grid(row=2, column=0, columnspan=2, sticky="w",  pady=(3, 5))

        self.user_textbox = ScrolledText(height=4, width=35, font=text_font, wrap="word")
        self.user_textbox.focus()
        self.user_textbox.grid(row=3, column=0, columnspan=2)

        # buttons
        self.clear_button = Button(text="Clear Screen", width=13, justify="center", font=button_font, command=self.clear_screen)
        self.clear_button.grid(row=4, column=0, pady=10)
        self.ok_button = Button(text="Ask", width=13, justify="center", font=button_font, command=self.get_answer)
        self.ok_button.grid(row=4, column=1, pady=10)

        self.chatbot_label = Label(text="ChatBot:", fg="white", bg=self.theme_color, font=label_font)
        self.chatbot_label.grid(row=5, column=0, columnspan=3, sticky="w")

        self.chatbot_textbox = ScrolledText(height=16, width=36, font=text_font, wrap="word")
        self.chatbot_textbox.grid(row=6, column=0, columnspan=2)

        self.window.mainloop()

    def get_answer(self):
        client = OpenAI(api_key=self.api_key)

        if self.radio_state.get() == 1:
            self.ok_button.config(state="disable")
            global message_box

            messages = message_box
            print(messages)
            message = self.user_textbox.get(1.0, END)
            if message:
                message_box.append({"role": "user", "content": message})
                chat = client.chat.completions.create(
                    model="gpt-3.5-turbo", messages=messages
                )
                reply = chat.choices[0].message.content
                self.chatbot_textbox.insert(END, reply)
                message_box.append({"role": "assistant", "content": reply})

        elif self.radio_state.get() == 2:
            self.ok_button.config(state="disable")

            response = client.images.generate(
                model="dall-e-2",
                prompt=self.user_textbox.get(1.0, END),
                size="1024x1024",
                quality="standard",
                n=1,
            )
            image_url = response.data[0].url
            self.chatbot_textbox.insert(END, image_url)

    def clear_screen(self):
        self.user_textbox.delete(1.0, END)
        self.chatbot_textbox.delete(1.0, END)
        self.radio_state.set(0)
        self.ok_button.config(state="active")
