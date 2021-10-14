Advil = "Advil"
Aleve = "Aleve"
Celebrex = "Celebrex"
Colcrys = "Colcrys"
Methylpred = "Methylprednisolone"
Mobic = "Mobic"
Othertreatment = "Other treatment"
Pred = "Prednisone"
TinctureofTime = "Tincture of time"


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
ANKLER = "Right ankle"
ANKLEL = "Left ankle"
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
WRISTR = "Right wrist"
WRISTL = "Left wrist"
ELBOWR = "Right elbow"
ELBOWL = "Left elbow"
SHOUDLERR = "Right shoulder"
SHOULDERL = "Left shoulder"

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
    (ANKLER, "Right ankle"),
    (ANKLEL, "Left ankle"),
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
    (WRISTR, "Right wrist"),
    (WRISTL, "Left wrist"),
    (ELBOWR, "Right elbow"),
    (ELBOWL, "Left elbow"),
    (SHOUDLERR, "Right shoulder"),
    (SHOULDERL, "Left shoulder"),
)

LAB_CHOICES = ((URATE, "Urate"),)

TREATMENT_CHOICES = (
    (Colcrys, "Colchicine"),
    (Advil, "Ibuprofen"),
    (Aleve, "Naproxen"),
    (Celebrex, "Celecoxib"),
    (Mobic, "Meloxicam"),
    (Pred, "Prednisone"),
    (Methylpred, "Methylprednisolone"),
    (TinctureofTime, "Tincture of time"),
    (Othertreatment, "Other treatment"),
)

BOOL_CHOICES = ((True, "Yes"), (False, "No"))
