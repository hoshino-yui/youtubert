from dataclasses import dataclass


@dataclass
class Comment:
    id: str
    text: str

    def text_markdown(self):
        return self.text.replace('\r', '').replace('\n', '\n\n')
