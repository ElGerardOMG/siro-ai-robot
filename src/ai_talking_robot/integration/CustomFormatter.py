import logging

class CustomFormatter(logging.Formatter):
    # Definimos los colores (Códigos ANSI)
    grey = "\x1b[38;20m"
    blue = "\x1b[34;20m"
    yellow = "\x1b[33;20m"
    red = "\x1b[31;20m"
    bold_red = "\x1b[31;1m"
    reset = "\x1b[0m"

    # Mapeo de Símbolos y Colores por nivel
    FORMATS = {
        logging.DEBUG:    f"{grey}[d][%(module)s]: %(message)s {reset}",
        logging.INFO:     f"{blue}[i][%(module)s]: %(message)s {reset}",
        logging.WARNING:  f"{yellow}[!][%(module)s]: %(message)s {reset}",
        logging.ERROR:    f"{red}[x][%(module)s]: %(message)s {reset}",
        logging.CRITICAL: f"{bold_red}[X][%(module)s]: %(message)s {reset}"
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)