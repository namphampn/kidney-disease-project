"""Làm sạch theo quy tắc cố định; không điền thiếu hoặc học từ dữ liệu."""
import numpy as np
import pandas as pd
from src.config import FEATURE_COLUMNS, NUMERIC_COLUMNS, CODED_COLUMNS, CATEGORY_VALUES, TARGET


def _strip_missing(series):
    """Chuẩn hóa chuỗi, giữ số và dùng np.nan tương thích sklearn."""
    return series.map(
        lambda x: np.nan if pd.isna(x) or (isinstance(x, str) and x.strip() in ("", "?"))
        else x.strip() if isinstance(x, str) else x
    )


def clean_features(df):
    """Nhận X gồm 24 thuộc tính (+ id tùy chọn), trả DataFrame mới.

    Không nhận nhãn để tránh đưa nhãn vào mô hình. Sai schema hoặc token
    không hợp lệ sẽ báo lỗi. Ô trống để thiếu cho imputer phía sau.
    Dùng FunctionTransformer(clean_features, validate=False) trong Pipeline.
    """
    if not isinstance(df, pd.DataFrame):
        raise TypeError("Đầu vào phải là pandas DataFrame có tên cột.")
    if df.empty:
        raise ValueError("Dữ liệu đầu vào rỗng.")
    if df.columns.duplicated().any():
        raise ValueError("Tên cột bị trùng.")
    missing = set(FEATURE_COLUMNS) - set(df.columns)
    extra = set(df.columns) - set(FEATURE_COLUMNS) - {"id"}
    if missing or extra:
        raise ValueError(f"Sai schema: thiếu cột {sorted(missing)}, cột ngoài dự kiến {sorted(extra)}")
    clean = df.loc[:, list(FEATURE_COLUMNS)].copy()
    for col in clean:
        clean[col] = _strip_missing(clean[col])
    for col in NUMERIC_COLUMNS + CODED_COLUMNS:
        converted = pd.to_numeric(clean[col], errors="coerce")
        bad = clean[col].notna() & converted.isna()
        if bad.any():
            raise ValueError(f"Cột {col} có giá trị không phải số: {clean.loc[bad, col].unique().tolist()}")
        clean[col] = converted.astype(float)
        if np.isinf(clean[col]).any():
            raise ValueError(f"Cột {col} có giá trị vô hạn.")
    for col, allowed in CATEGORY_VALUES.items():
        bad = clean[col].notna() & ~clean[col].isin(allowed)
        if bad.any():
            raise ValueError(f"Cột {col} có giá trị phân loại không hợp lệ: {clean.loc[bad, col].unique().tolist()}")
        clean[col] = clean[col].astype(object).where(clean[col].notna(), np.nan)
    return clean


def encode_target(y):
    """ckd=1, notckd=0; chấp nhận nhãn đã mã hóa; không điền nhãn thiếu."""
    labels = _strip_missing(y.copy())
    if labels.isna().any():
        raise ValueError("Nhãn bị thiếu; cần kiểm tra nguồn, không tự điền nhãn.")
    mapping = {"ckd": 1, "notckd": 0, 1: 1, 0: 0}
    invalid = labels[~labels.isin(mapping)]
    if not invalid.empty:
        raise ValueError(f"Nhãn không hợp lệ: {invalid.unique().tolist()}")
    return labels.map(mapping).astype("int64").rename(TARGET)


def clean_raw(df):
    """Tiện ích EDA tương thích cách gọi cũ: nhận X hoặc bảng có nhãn.

    Pipeline dự đoán gọi clean_features; encode_target chạy riêng trên y.
    """
    if not isinstance(df, pd.DataFrame):
        raise TypeError("Đầu vào phải là pandas DataFrame có tên cột.")
    clean = clean_features(df.drop(columns=[TARGET], errors="ignore"))
    if TARGET in df.columns:
        clean[TARGET] = encode_target(df[TARGET])
    return clean
