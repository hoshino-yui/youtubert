from dataclasses import dataclass


@dataclass
class Comment:
    id: str
    text: str

    def text_lines(self):
        return self.text.splitlines()
