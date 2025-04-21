from pathlib import Path


class Key_takeaways:
    _str_dropdown_start: str = (
        '```{dropdown} <i class="fas fa-brain"></i>&nbsp;&nbsp;&nbsp;Key takeaways\n\n'
    )

    _str_dropdown_end: str = "```\n"

    _str_card_ref: str

    _str_card: str

    _dict_key_takeaways: dict[int, list[str]]

    def _read_key_takeaways(self, key_takeaways_path: Path) -> None:
        """Parses a `*_keytakeaways.txt`-file.

        Args:
            key_takeaways_path: Path to an existing `.txt`-file
        """
        with open(key_takeaways_path, encoding="utf-8") as f:
            key_takeaways_number = None
            for line in f:
                if line.strip() == "":
                    key_takeaways_number = None
                    continue

                if key_takeaways_number is not None:
                    self._dict_key_takeaways[key_takeaways_number].append(line.strip())
                    continue

                if line.strip().isnumeric() and key_takeaways_number is None:
                    key_takeaways_number = int(line.strip())
                    self._dict_key_takeaways[key_takeaways_number] = []

    def get_key_takeaway_dropdown_str(self) -> str:
        """Creates a string representation of the dropdown.

        Returns:
            Complete key takeaways dropdown string from the <notebook-name>.txt file
        """
        str_dropdown = self._str_dropdown_start
        for key_takeaway_number in sorted(self._dict_key_takeaways.keys()):
            str_card_copy = self._str_card.replace(
                "?key_takeaway_number?", str(key_takeaway_number)
            )
            str_card_copy = str_card_copy.replace(
                "?key_takeaway_text?",
                "\n".join(self._dict_key_takeaways.get(key_takeaway_number)),
            )
            str_dropdown += str_card_copy

        str_dropdown += self._str_dropdown_end

        return str_dropdown

    def __init__(self, key_takeaways_path: Path):
        self._str_card_ref = (
            str(key_takeaways_path.parent).split("/")[-1].replace("_", "-")
            + "-"
            + "-".join(str(key_takeaways_path.stem).split("_")[0:-1])
            + "-key-takeaway-"
        )

        self._str_card = (
            ":::{card}\n"
            ":link: " + self._str_card_ref + "?key_takeaway_number?\n"
            ":link-type: ref\n"
            "?key_takeaway_text?\n"
            ":::\n\n"
        )

        self._dict_key_takeaways = {}
        self._read_key_takeaways(key_takeaways_path)
