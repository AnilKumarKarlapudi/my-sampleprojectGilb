import platform


class RegisterKeys:
    if '7' in platform.release():
        PASSPORT = r"SOFTWARE\Gilbarco\Passport"
        NT = r'SOFTWARE\Gilbarco\NT'
        CRIND = r'SOFTWARE\Gilbarco\CRIND'
        SECURE = r'SOFTWARE\Gilbarco\Secure'
        RES = r'SOFTWARE\Gilbarco\Passport\MWS'
        CASH_DRAWER = r'SOFTWARE\OleForRetail\ServiceOPOS\CashDrawer'
        POS_PRINTER = r'SOFTWARE\OleForRetail\ServiceOPOS\POSPrinter'
        CAR_WASH = r'SOFTWARE\OLEforRetail\ServiceOPOS\CarWashController'
        C_SOFT_PASSPORT = r'SOFTWARE\CSOFT\Passport'
        REMOTE_MANAGER = r'SOFTWARE\Gilbarco\RemoteManager'
    else:
        PASSPORT = r"SOFTWARE\WOW6432Node\Gilbarco\Passport"
        NT = r'SOFTWARE\WOW6432Node\Gilbarco\NT'
        CRIND = r'SOFTWARE\WOW6432Node\Gilbarco\CRIND'
        SECURE = r'SOFTWARE\WOW6432Node\Gilbarco\Secure'
        RES = r'SOFTWARE\WOW6432Node\Gilbarco\Passport\MWS'
        CASH_DRAWER = r'SOFTWARE\WOW6432Node\OleForRetail\ServiceOPOS\CashDrawer'
        POS_PRINTER = r'SOFTWARE\WOW6432Node\OleForRetail\ServiceOPOS\POSPrinter'
        POS_PRINTER_T88II = r'SOFTWARE\WOW6432Node\OleForRetail\ServiceOPOS\POSPrinter\TM-T88II'
        CAR_WASH = r'SOFTWARE\WOW6432Node\OLEforRetail\ServiceOPOS\CarWashController'
        C_SOFT_PASSPORT = r'SOFTWARE\WOW6432Node\CSOFT\Passport'
        HTML_POS = r'SOFTWARE\WOW6432Node\Gilbarco\HTMLPOS'
        REMOTE_MANAGER = r'SOFTWARE\WOW6432Node\Gilbarco\RemoteManager'
        RUN = r"Software\Microsoft\Windows\CurrentVersion\RunOnce"
        STORE_CONFIG = r'SOFTWARE\WOW6432Node\Gilbarco\automation'
