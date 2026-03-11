import logging

# Nivel personalizado entre INFO (20) y WARNING (30)
NOTICE = 25
logging.addLevelName(NOTICE, "NOTICE")


def notice(self, message, *args, **kwargs):
    """Registra un mensaje con nivel NOTICE."""
    if self.isEnabledFor(NOTICE):
        # stacklevel=2 para que %(module)s sea el llamador real, no este módulo
        stacklevel = kwargs.pop("stacklevel", 1) + 1
        self._log(NOTICE, message, args, stacklevel=stacklevel, **kwargs)


# Añadir el método notice() a la clase Logger
logging.Logger.notice = notice


class CustomFormatter(logging.Formatter):
    # Definimos los colores (Códigos ANSI)
    grey = "\x1b[38;20m"
    blue = "\x1b[34;20m"
    dark_green = "\x1b[32;20m"
    yellow = "\x1b[33;20m"
    red = "\x1b[31;20m"
    bold_red = "\x1b[31;1m"
    reset = "\x1b[0m"

    # Mapeo de Símbolos y Colores por nivel
    FORMATS = {
        logging.DEBUG:    f"{grey}[d][%(module)s]: %(message)s {reset}",
        logging.INFO:     f"{blue}[i][%(module)s]: %(message)s {reset}",
        NOTICE:           f"{dark_green}[>][%(module)s]: %(message)s {reset}",
        logging.WARNING:  f"{yellow}[!][%(module)s]: %(message)s {reset}",
        logging.ERROR:    f"{red}[x][%(module)s]: %(message)s {reset}",
        logging.CRITICAL: f"{bold_red}[X][%(module)s]: %(message)s {reset}"
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)