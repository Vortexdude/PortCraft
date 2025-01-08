from portcraft.models import Stage


class Extractor(object):
    def __init__(self, config):
        self.__conf = config
        self._stages = self._extract('stages')


    def _extract(self, name: str):
        """
        Extract the specified key from the configuration data.

        Args:
            name (str): Key to extract from the configuration.

        Returns:
            dict or list: Extracted value or an empty list if not found.
        """
        if isinstance(self.__conf, dict) and name in self.__conf:
            return self.__conf[name]
        if isinstance(self.__conf, list):
            return self.__conf[0].get(name, [])
        return []

    @property
    def stages(self):
        """
        Prepare stages from the configuration data.

        Returns:
            list: List of stage objects.
        """
        return [
            Stage.prepare_model(attrs={"name": name, "args": value})
            for name, value in self._stages.items()
        ]
