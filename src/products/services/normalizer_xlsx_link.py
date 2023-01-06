from typing import Callable


class NormalizeXLSXLink:
    """
    Normalizes a link to appropriate form.
    """

    def __init__(self, link: str):
        """
        Stores the link which should be normalized. Also, it
        defines the URL part which specifies what normalizer must be
        used.
        """
        self.link = link
        self._link_normalizers = {
            'docs.google.com/spreadsheets': self._google_normalizer,
        }

    def execute(self) -> str:
        """
        Performs normalization operations on Excel file link if
        needed.
        """
        normalizer = self._get_normalizer()
        return normalizer() if normalizer else self.link

    def _get_normalizer(self) -> Callable[[], None] | None:
        """
        Factory function. Defines what normalizer is needed to use.
        If nothing matches, returns None.
        """
        for link_part, normalizer_func in self._link_normalizers:
            if link_part in self.link:
                return normalizer_func
        return None

    def _google_normalizer(self) -> str:
        """
        Normalize link for the Google spreadsheets if it has a `/edit#gid=`
        part. Otherwise, it will return the same link as was passed.
        """
        edit_part = '/edit#gid='
        return (
            self.link.replace(edit_part, '/export?format=xlsx&gid=')
            if edit_part in self.link else self.link
        )
