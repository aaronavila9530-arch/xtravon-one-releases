from .centro_ejecutivo import install_centro_ejecutivo_screen
from .issue_log import install_issue_log_screen
from .informes import install_informes_screen
from .roles_permisos import install_roles_permisos_screen
from .ia_ejecutiva import install_ia_ejecutiva_screen
from .gestion_profesional import install_gestion_profesional_screen
from .ayuda_qa import install_ayuda_qa_screen
from .liquidaciones_choferes import install_liquidaciones_choferes_screen
from .accounting import install_accounting_screen


def install_frontend_modules(app_class):
    install_centro_ejecutivo_screen(app_class)
    install_issue_log_screen(app_class)
    install_informes_screen(app_class)
    install_roles_permisos_screen(app_class)
    install_ia_ejecutiva_screen(app_class)
    install_gestion_profesional_screen(app_class)
    install_ayuda_qa_screen(app_class)
    install_liquidaciones_choferes_screen(app_class)
    install_accounting_screen(app_class)
