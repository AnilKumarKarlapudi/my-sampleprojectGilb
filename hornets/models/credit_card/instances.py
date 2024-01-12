from hornets.models.credit_card.models import CreditCardBrandEnum, EmvCreditCard, MagstripeCreditCard

VISA_MAGSTRIPE = MagstripeCreditCard(
    card_brand=CreditCardBrandEnum.CORE,
    card_name="Visa",
    card_number="4012002000028021"
)
VISA_EMV = EmvCreditCard(
    card_brand=CreditCardBrandEnum.CORE,
    card_name="EMVVisaCredit",
    card_number="4761739001010036"
)
VISA_US_DEBIT_EMV = EmvCreditCard(
    card_brand=CreditCardBrandEnum.CORE,
    card_name="EMVVisaUSDebit",
    card_number="4761739001010135"
)
VISA_EMV_CRINDSIM = EmvCreditCard(
    card_brand=CreditCardBrandEnum.CORE,
    card_name="CRINDSim EMV VISA [No CVM]",
    card_number="4761739001010440"
)
MAESTRO_EMV = EmvCreditCard(
    card_brand=CreditCardBrandEnum.CORE,
    card_name="EMVMaestro",
    card_number="5413330089099023"
)
US_MAESTRO_EMV = EmvCreditCard(
    card_brand=CreditCardBrandEnum.CORE,
    card_name="EMVUSMaestro",
    card_number="5413330089099023"
)
DINERS_CLUB_EMV = EmvCreditCard(
    card_brand=CreditCardBrandEnum.CORE,
    card_name="EMVDinersClub",
    card_number="6510000000000125"
)
MASTERCARD_MAGSTRIPE = MagstripeCreditCard(
    card_brand=CreditCardBrandEnum.CORE,
    card_name="MasterCard",
    card_number="5100000000000008"
)
DISCOVER_MAGSTRIPE = MagstripeCreditCard(
    card_brand=CreditCardBrandEnum.CORE,
    card_name="Discover",
    card_number="344546474849509"
)
WEX_MAGSTRIPE = MagstripeCreditCard(
    card_brand=CreditCardBrandEnum.CORE,
    card_name="WEX1",
    card_number="6900460420001234566"
)
WEX_EMV = EmvCreditCard(
    card_brand=CreditCardBrandEnum.CORE,
    card_name="WEX1_EMV",
    card_number="6900460420001234566"
)
VOYAGER_MASTRIPE = MagstripeCreditCard(
    card_brand=CreditCardBrandEnum.CORE,
    card_name="Voyager",
    card_number="7088859990012002574"
)
VOYAGER_EMV = EmvCreditCard(
    card_brand=CreditCardBrandEnum.CORE,
    card_name="VOYAGER_EMV",
    card_number="7088869420240001402"
)
