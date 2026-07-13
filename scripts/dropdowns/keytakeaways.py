from pathlib import Path


class Key_takeaways:
    _str_dropdown_start: str = "```{dropdown} 🧠 Key takeaways\n\n"

    _str_dropdown_end: str = "```\n"

    _str_card_ref: str

    _str_card: str

    _dict_key_takeaways: dict[int, list[str]]

    _dict_key_takeaway_link_overrides: dict[int, str]

    def _read_key_takeaways(self, key_takeaways_path: Path) -> None:
        """Parses a `*_keytakeaways.txt`-file.

        Each key takeaway is introduced by a line with its number, optionally
        followed by ``:<label>`` to link the card to an existing label instead
        of the default ``<section>-<notebook>-key-takeaway-<number>`` one.
        This is needed when several key takeaways describe the same heading,
        since MyST only allows a single label per heading.

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

                number_part, _, label_override = line.strip().partition(":")
                if number_part.isnumeric() and key_takeaways_number is None:
                    key_takeaways_number = int(number_part)
                    self._dict_key_takeaways[key_takeaways_number] = []
                    if label_override:
                        self._dict_key_takeaway_link_overrides[key_takeaways_number] = (
                            label_override
                        )

    def get_key_takeaway_dropdown_str(self) -> str:
        """Creates a string representation of the dropdown.

        Returns:
            Complete key takeaways dropdown string from the <notebook-name>.txt file
        """
        str_dropdown = self._str_dropdown_start
        for key_takeaway_number in sorted(self._dict_key_takeaways.keys()):
            link = self._dict_key_takeaway_link_overrides.get(
                key_takeaway_number, self._str_card_ref + str(key_takeaway_number)
            )
            str_card_copy = self._str_card.replace("?key_takeaway_link?", link)
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
            ":::{card}\n:link: #?key_takeaway_link?\n?key_takeaway_text?\n:::\n\n"
        )

        self._dict_key_takeaways = {}
        self._dict_key_takeaway_link_overrides = {}
        self._read_key_takeaways(key_takeaways_path)
