import re
from pathlib import Path

# Every key takeaway card is itself a link, and HTML forbids nesting an anchor inside an
# anchor. A citation, glossary term, cross reference or markdown link in a key takeaway
# therefore produces markup the browser has to reparent, which breaks React hydration for
# the *whole* page: nothing on it stays interactive and the browser back button starts
# throwing. The failure is silent at build time, so it is caught here instead.
_LINK_IN_CARD = re.compile(r"\{(?:cite[a-z:]*|term|ref|doc|download|numref)\}`|\]\(")


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
        self._reject_links(key_takeaways_path)

    def _reject_links(self, key_takeaways_path: Path) -> None:
        """Fails the build if a key takeaway contains anything that renders as a link.

        Args:
            key_takeaways_path: Path to the `*_keytakeaways.txt`-file being parsed

        Raises:
            ValueError: If a key takeaway contains a link, citation or cross reference
        """
        offenders = [
            (number, line)
            for number, lines in sorted(self._dict_key_takeaways.items())
            for line in lines
            if _LINK_IN_CARD.search(line)
        ]
        if offenders:
            details = "\n".join(f"  key takeaway {n}: {line}" for n, line in offenders)
            raise ValueError(
                f"{key_takeaways_path}: key takeaways must not contain links, "
                f"citations or cross references, because the card around them is "
                f"already a link and the nested anchor breaks the page.\n{details}"
            )
