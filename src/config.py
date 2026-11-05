"""Cấu hình dùng chung, không chứa tham số học từ dataset."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RAW_DATA_PATH = ROOT / "data" / "raw" / "kidney_disease.csv"
FIGURES_DIR = ROOT / "reports" / "figures"
TABLES_DIR = ROOT / "reports" / "tables"
TARGET = "classification"
RANDOM_STATE = 42
POSITIVE_LABEL = 1
PRIMARY_SCORING = "recall"
FEATURE_COLUMNS = (
    "age", "bp", "sg", "al", "su", "rbc", "pc", "pcc", "ba", "bgr",
    "bu", "sc", "sod", "pot", "hemo", "pcv", "wc", "rc", "htn", "dm",
    "cad", "appet", "pe", "ane",
)
# sg/al/su lưu dạng số nhưng mang ý nghĩa phân loại/thứ bậc.
# Người 2 chọn cách mã hóa trong CV trên train, không chọn qua tập test.
NUMERIC_COLUMNS = ("age", "bp", "bgr", "bu", "sc", "sod", "pot", "hemo", "pcv", "wc", "rc")
CODED_COLUMNS = ("sg", "al", "su")
CATEGORY_VALUES = {
    "rbc": ("normal", "abnormal"), "pc": ("normal", "abnormal"),
    "pcc": ("present", "notpresent"), "ba": ("present", "notpresent"),
    "htn": ("yes", "no"), "dm": ("yes", "no"), "cad": ("yes", "no"),
    "appet": ("good", "poor"), "pe": ("yes", "no"), "ane": ("yes", "no"),
}
