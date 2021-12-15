ADVIL = "Advil"
ALEVE = "Aleve"
CELEBREX = "Celebrex"
COLCRYS = "Colcrys"
INDOCIN = "Indocin"
METHYLPRED = "Methylprednisolone"
MOBIC = "Mobic"
OTHERTREATMENT = "Other treatment"
PRED = "Prednisone"
TINCTUREOFTIME = "Tincture of time"

UNDERONE = "under 24 hours"
ONETOTHREE = "more than 1 but less than 3 days"
THREETOSEVEN = "more than 3 but less than 7 days"
SEVERENTOTEN = "more than 7 but less than 10 days"
TENTOFOURTEEN = "more than 10 but less than 14 days"
FOURTEENPLUS = "over 14 days"

AST = "AST"
ALT = "ALT"
CREATININE = "Creatinine"
HGB = "Hemoglobin"
PLTS = "Platelets"
WBC = "White blood cells"
URATE = "Urate"

TOER1 = "Right great toe"
TOER2 = "Right second toe"
TOER3 = "Right third toe"
TOER4 = "Right fourth toe"
TOER5 = "Right little toe"
TOEL1 = "Left great toe"
TOEL2 = "Left secont toe"
TOEL3 = "Left third toe"
TOEL4 = "Left fourth toe"
TOEL5 = "Left little toe"
MTPR1 = "Right first MTP"
MTPR2 = "Right second MTP"
MTPR3 = "Right third MTP"
MTPR4 = "Right fourth MTP"
MTPR5 = "Right fifth MTP"
MTPL1 = "Left first MTP"
MTPL2 = "Left second MTP"
MTPL3 = "Left third MTP"
MTPL4 = "Left fourth MTP"
MTPL5 = "Left fifth MTP"
ANKLER = "Right ankle"
ANKLEL = "Left ankle"
TNR = "Right talonavicular"
TNL = "Left talonavicular"
MIDFOOTR = "Right midfoot"
MIDFOOTL = "Left midfoot"
KNEER = "Right knee"
KNEEL = "Left knee"
HIPR = "Right hip"
HIPL = "Left hip"
FINGR1 = "Right thumb"
FINGR2 = "Right index finger"
FINGR3 = "Right middle finger"
FINGR4 = "Right ring finger"
FINGR5 = "Right little finger"
FINGL1 = "Left thumb"
FINGL2 = "Left index finger"
FINGL3 = "Left middle finger"
FINGL4 = "Left ring finger"
FINGL5 = "Left little finger"
MCPR1 = "Right first MCP"
MCPR2 = "Right second MCP"
MCPR3 = "Right third MCP"
MCPR4 = "Right fourth MCP"
MCPR5 = "Right fifth MCP"
MCPL1 = "Left first MCP"
MCPL2 = "Left second MCP"
MCPL3 = "Left third MCP"
MCPL4 = "Left fourth MCP"
MCPL5 = "Left fifth MCP"
CMCL = "Left first CMC"
CMCR = "Right first CMC"
WRISTR = "Right wrist"
WRISTL = "Left wrist"
ELBOWR = "Right elbow"
ELBOWL = "Left elbow"
SHOUDLERR = "Right shoulder"
SHOULDERL = "Left shoulder"
ACR = "Right acromioclacivular"
ACL = "Left acromioclavicular"
SCR = "Right sternoclavicular"
SCL = "Left sternoclavicular"
TMR = "Right temporomandibular"
TML = "Left temporomandibular"
RFOOT = "Right foot"
LFOOT = "Left foot"
RHAND = "Right hand"
LHAND = "Left hand"

LIMITED_JOINT_CHOICES = (
    (RFOOT, "Right foot"),
    (LFOOT, "Left foot"),
    (ANKLER, "Right ankle"),
    (ANKLEL, "Left ankle"),
    (KNEER, "Right knee"),
    (KNEEL, "Left knee"),
    (HIPR, "Right hip"),
    (HIPL, "Left hip"),
    (RHAND, "Right hand"),
    (LHAND, "Left hand"),
    (WRISTR, "Right wrist"),
    (WRISTL, "Left wrist"),
    (ELBOWR, "Right elbow"),
    (ELBOWL, "Left elbow"),
    (SHOUDLERR, "Right shoulder"),
    (SHOULDERL, "Left shoulder"),
)

JOINT_CHOICES = (
    (TOER1, "Right great toe"),
    (TOER2, "Right second toe"),
    (TOER3, "Right third toe"),
    (TOER4, "Right fourth toe"),
    (TOER5, "Right little toe"),
    (TOEL1, "Left great toe"),
    (TOEL2, "Left second toe"),
    (TOEL3, "Left third toe"),
    (TOEL4, "Left fourth toe"),
    (TOEL5, "Left little toe"),
    (MTPR1, "Right first MTP"),
    (MTPR2, "Right second MTP"),
    (MTPR3, "Right third MTP"),
    (MTPR4, "Right fourth MTP"),
    (MTPR5, "Right fifth MTP"),
    (MTPL1, "Left first MTP"),
    (MTPL2, "Left second MTP"),
    (MTPL3, "Left third MTP"),
    (MTPL4, "Left fourth MTP"),
    (MTPL5, "Left fifth MTP"),
    (ANKLER, "Right ankle"),
    (ANKLEL, "Left ankle"),
    (TNR, "Right talonavicular"),
    (TNL, "Left talonavicular"),
    (MIDFOOTR, "Right midfoot"),
    (MIDFOOTL, "Left midfoot"),
    (KNEER, "Right knee"),
    (KNEEL, "Left knee"),
    (HIPR, "Right hip"),
    (HIPL, "Left hip"),
    (FINGR1, "Right thumb"),
    (FINGR2, "Right index finger"),
    (FINGR3, "Right middle finger"),
    (FINGR4, "Right ring finger"),
    (FINGR5, "Right little finger"),
    (FINGL1, "Left thumb"),
    (FINGL2, "Left index finger"),
    (FINGL3, "Left middle finger"),
    (FINGL4, "Left ring finger"),
    (FINGL5, "Left little finger"),
    (MCPR1, "Right first MCP"),
    (MCPR2, "Right second MCP"),
    (MCPR3, "Right third MCP"),
    (MCPR4, "Right fourth MCP"),
    (MCPR5, "Right fifth MCP"),
    (MCPL1, "Left first MCP"),
    (MCPL2, "Left second MCP"),
    (MCPL3, "Left third MCP"),
    (MCPL4, "Left fourth MCP"),
    (MCPL5, "Left fifth MCP"),
    (CMCL, "Left first CMC"),
    (CMCR, "Right first CMC"),
    (WRISTR, "Right wrist"),
    (WRISTL, "Left wrist"),
    (ELBOWR, "Right elbow"),
    (ELBOWL, "Left elbow"),
    (SHOUDLERR, "Right shoulder"),
    (SHOULDERL, "Left shoulder"),
    (ACR, "Right acromioclacivular"),
    (ACL, "Left acromioclavicular"),
    (SCR, "Right sternoclavicular"),
    (SCL, "Left sternoclavicular"),
    (TMR, "Right temporomandibular"),
    (TML, "Left temporomandibular"),
)

LAB_CHOICES = ((URATE, "Urate"),)

TREATMENT_CHOICES = (
    (COLCRYS, "Colchicine"),
    (ADVIL, "Ibuprofen"),
    (ALEVE, "Naproxen"),
    (CELEBREX, "Celecoxib"),
    (INDOCIN, "Indocin"),
    (MOBIC, "Meloxicam"),
    (PRED, "Prednisone"),
    (METHYLPRED, "Methylprednisolone"),
    (TINCTUREOFTIME, "Tincture of time"),
    (OTHERTREATMENT, "Other treatment"),
)

BOOL_CHOICES = ((True, "Yes"), (False, "No"))

DURATION_CHOICES = [
    (UNDERONE, "Under 24 hours"),
    (ONETOTHREE, "More than 1 but less than 3 days"),
    (THREETOSEVEN, "More than 3 but less than 7 days"),
    (SEVERENTOTEN, "More than 7 but less than 10 days"),
    (TENTOFOURTEEN, "More than 10 but less than 14 days"),
    (FOURTEENPLUS, "Over 14 days"),
]

UNLIKELY = "unlikely"
EQUIVOCAL = "equivocal"
LIKELY = "likely"

LOWRANGE = "Gout is not likely and alternative causes of symptoms should be investigated."
MIDRANGE = "Indeterminate likelihood of gout and it can't be ruled in or out. Physician evaluation is required."
HIGHRANGE = "Gout is very likely. Not a whole lot else needs to be done, other than treat your gout!"


LOWPREV = "2.2%"
MODPREV = "31.2%"
HIGHPREV = "80.4%"
