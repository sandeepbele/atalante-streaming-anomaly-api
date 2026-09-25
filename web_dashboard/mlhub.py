from kafka import KafkaConsumer, KafkaProducer, KafkaAdminClient
from pydantic import BaseModel
import json
from datetime import datetime

from pydantic.class_validators import validator
from river.compose import Pipeline
from river.anomaly import HalfSpaceTrees, OneClassSVM
from river.preprocessing import MinMaxScaler, StandardScaler
from river import feature_extraction as fx
from typing import Dict

# Define Pydantic data model
class TSModel(BaseModel):
    ts: datetime
    metric: str
    value: float

    class Config:
        json_encoders = {
                            datetime: lambda v: v.isoformat()
        }

    def to_features(self):
        features = self.dict()
        features['day'] = self.ts.day
        features['day_of_week'] = self.ts.isoweekday()
        features['hour'] = self.ts.hour
        features['minute'] = self.ts.minute
        features['is_weekend'] = self.ts.isoweekday() in [6,7]
        features['month'] = self.ts.month

        features.pop('ts')
        return features



class RiverANDetector:

    model_zoo = {
        'hs_tree': Pipeline(('scale', MinMaxScaler()), ('detector', HalfSpaceTrees())),
        'hs_tree_with_feature': Pipeline(('scale', MinMaxScaler()), (fx.PolynomialExtender()),
                                                 ('detector', HalfSpaceTrees())),
        'hs_tree_with_feature_d2': Pipeline(('scale', MinMaxScaler()),
                                                    (fx.PolynomialExtender(degree=2, include_bias=True)),
                                                    ('detector', HalfSpaceTrees())),
        'hs_tree_with_feature_d2_rbf': Pipeline(('scale', MinMaxScaler()),
                                                        (fx.PolynomialExtender(degree=3, include_bias=True)),
                                                        ('sampler', fx.RBFSampler()), ('detector', HalfSpaceTrees())),
        'svm_with_scalar_rbf': Pipeline(('scale', StandardScaler()), ('sampler', fx.RBFSampler()),
                                                ('detector', OneClassSVM()))
    }

    def __init__(self,metric:str , model_config:str=None):

        if model_config is None:
            self.model = self.model_zoo['hs_tree'].clone()
        else:
            self.model = self.model_zoo[model_config].clone()

        self.metric = metric
        self.anomaly_threshold = 0.7

    def detect_anomaly(self, ts_point:TSModel):
        score = self.model.score_one({'x':ts_point.value})
        self.model = self.model.learn_one({'x':ts_point.value})

        is_anomaly = False
        if score > self.anomaly_threshold:
            is_anomaly = True

        return ts_point,is_anomaly,score
