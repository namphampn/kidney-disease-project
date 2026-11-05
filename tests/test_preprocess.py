"""Kiểm tra hợp đồng bàn giao; không huấn luyện hay chọn mô hình."""
import unittest
import tempfile
from pathlib import Path
import numpy as np
import pandas as pd
from pandas.testing import assert_frame_equal
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import FunctionTransformer, OneHotEncoder, StandardScaler
import joblib
from src.config import RAW_DATA_PATH, FEATURE_COLUMNS, NUMERIC_COLUMNS, CODED_COLUMNS, CATEGORY_VALUES, TARGET
from src.preprocess import clean_features, clean_raw, encode_target


class DataHandoffTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.raw = pd.read_csv(RAW_DATA_PATH)
        cls.X = cls.raw.drop(columns=TARGET)

    def test_actual_dataset_quality(self):
        result = clean_raw(self.raw)
        self.assertEqual(result.shape, (400, 25))
        self.assertEqual(result[TARGET].value_counts().to_dict(), {1: 250, 0: 150})
        self.assertEqual(result.duplicated().sum(), 0)
        self.assertEqual(result[TARGET].isna().sum(), 0)
        self.assertEqual(result[['pcv', 'wc', 'rc']].isna().sum().tolist(), [71, 106, 131])

    def test_no_mutation_and_repeatable(self):
        original = self.raw.copy(deep=True)
        result = clean_raw(self.raw)
        assert_frame_equal(self.raw, original)
        assert_frame_equal(result, clean_raw(result))
        assert_frame_equal(clean_features(self.X), clean_raw(self.X))

    def test_format_and_missing_tokens(self):
        row = self.X.iloc[[0]].copy().astype(object)
        row['dm'] = '\tyes '
        row['pcv'] = ' 44 '
        row['wc'] = '\t?'
        row['rc'] = '  '
        result = clean_features(row)
        self.assertEqual(result.iloc[0]['dm'], 'yes')
        self.assertEqual(result.iloc[0]['pcv'], 44.)
        self.assertTrue(pd.isna(result.iloc[0]['wc']))
        self.assertTrue(pd.isna(result.iloc[0]['rc']))

    def test_label_mapping_and_invalid_labels(self):
        self.assertEqual(encode_target(pd.Series(['ckd\t', ' notckd ', 1, 0])).tolist(), [1, 0, 1, 0])
        for values in [['unknown'], [None], ['?']]:
            with self.subTest(values=values), self.assertRaises(ValueError):
                encode_target(pd.Series(values))

    def test_schema_contract(self):
        for bad in [self.X.iloc[:0], self.X.drop(columns='age'), self.raw, self.X.assign(unknown=0)]:
            with self.subTest(columns=list(bad.columns)), self.assertRaises(ValueError):
                clean_features(bad)
        with self.assertRaises(TypeError):
            clean_features(self.X.to_numpy())
        duplicated = pd.concat([self.X, self.X[['age']]], axis=1)
        with self.assertRaises(ValueError):
            clean_features(duplicated)

    def test_bad_values_not_silently_imputed(self):
        for column, value in [('pcv', 'abc'), ('age', 'abc'), ('sc', np.inf), ('dm', 'maybe')]:
            row = self.X.iloc[[0]].copy().astype(object)
            row[column] = value
            with self.subTest(column=column, value=value), self.assertRaises(ValueError):
                clean_features(row)

    def test_feature_order_and_id_optional(self):
        baseline = clean_features(self.X)
        assert_frame_equal(baseline, clean_features(self.X.drop(columns='id').iloc[:, ::-1]))
        self.assertEqual(tuple(baseline.columns), FEATURE_COLUMNS)

    def test_sklearn_pipeline_and_joblib_inference_without_target(self):
        # Chỉ kiểm tra dữ liệu đi qua Pipeline, không đo chất lượng mô hình.
        numeric = list(NUMERIC_COLUMNS + CODED_COLUMNS)
        categorical = list(CATEGORY_VALUES)
        pipeline = Pipeline([
            ('clean', FunctionTransformer(clean_features, validate=False)),
            ('prepare', ColumnTransformer([
                ('num', Pipeline([('impute', SimpleImputer(strategy='median')),
                                  ('scale', StandardScaler())]), numeric),
                ('cat', Pipeline([('impute', SimpleImputer(strategy='most_frequent')),
                                  ('encode', OneHotEncoder(handle_unknown='ignore', sparse_output=False))]), categorical),
            ])),
        ])
        pipeline.fit(self.X.iloc[:320])
        # Một mẫu giữ lại có tất cả ô trống là đầu vào hợp lệ để imputer xử lý.
        inference = self.X.iloc[320:].drop(columns='id').copy().astype(object)
        inference.iloc[0] = None
        before = inference.copy(deep=True)
        transformed = pipeline.transform(inference)
        self.assertEqual(transformed.shape[0], 80)
        self.assertTrue(np.isfinite(transformed).all())
        assert_frame_equal(before, inference)
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / 'preprocess.joblib'
            joblib.dump(pipeline, path)
            np.testing.assert_allclose(transformed, joblib.load(path).transform(inference))


if __name__ == '__main__':
    unittest.main(verbosity=2)
