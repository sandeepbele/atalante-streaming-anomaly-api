from abc import ABC, abstractmethod
from dataclasses import dataclass

from pydantic import BaseModel, validator
from typing import Dict, List, Any, Tuple
from datetime import datetime

from river.preprocessing import MinMaxScaler, StandardScaler, RobustScaler, MinMaxScaler, MaxAbsScaler
from river.anomaly import HalfSpaceTrees, GaussianScorer, OneClassSVM, QuantileFilter, ThresholdFilter
from river import compose, feature_extraction as fx, metrics


class MLInput(BaseModel, ABC):
    @abstractmethod
    def get_data_as_dict(self) -> dict:
       pass


class MLProcessor(ABC):

    @abstractmethod
    def in_schema(self):
        pass

    @abstractmethod
    def out_schema(self):
        pass

    @abstractmethod
    def learn_one_predict_one(self, input):
        pass


class MultiMetricTimeseries(BaseModel):

    ds: datetime
    data: Dict[str,float]

    def get_data_as_dict(self)-> dict:

        ts_features = dict()
        ts_features['day'] = self.ds.day
        ts_features['day_of_week'] = self.ds.isoweekday()
        ts_features['hour'] = self.ds.hour
        ts_features['minute'] = self.ds.minute
        ts_features['is_weekend'] = self.ds.isoweekday() in [6,7]
        ts_features['month'] = self.ds.month

        #ts_features.pop('ds')
        return { ** ts_features, ** self.data }

    def get_ts_features(self):

        ts_features = dict()
        ts_features['day'] = self.ds.day
        ts_features['day_of_week'] = self.ds.isoweekday()
        ts_features['hour'] = self.ds.hour
        ts_features['minute'] = self.ds.minute
        ts_features['is_weekend'] = self.ds.isoweekday() in [6, 7]
        ts_features['month'] = self.ds.month

        return ts_features

    def get_ts_features_names(self):
        return ['day','day_of_week','hour','minute','is_weekend','month']


class AnomalyOutput(BaseModel):

    model: Any
    is_anomaly: bool
    score: float
    data: MultiMetricTimeseries


@dataclass
class RiverAnomalyDetector(MLProcessor):

    input_schema = MultiMetricTimeseries
    output_schema = AnomalyOutput

    anomaly_threshold:float = 0.9

    class algorithm:
        HALF_SPACE_TREE = 'hs_tree_with_feature'
        HALF_SPACE_TREE_D2 = 'hs_tree_with_feature_d2'
        HALF_SPACE_TREE_D2_RBF = 'hs_tree_with_feature_d2_rbf'
        SVM_WITH_SCALAR_RBF = 'svm_with_scalar_rbf'
        GAUSSIAN_SCORER = 'guassian_scorer'

    model_zoo = {
        'hs_tree_with_feature': compose.Pipeline(('scale', MinMaxScaler()),
                                                 ('detector', HalfSpaceTrees())),
        'hs_tree_with_feature_d2': compose.Pipeline(('scale', MinMaxScaler()),
                                                    ('detector', HalfSpaceTrees())),
        'hs_tree_with_feature_d2_rbf': compose.Pipeline(('scale', MinMaxScaler()),
                                                        ('sampler', fx.RBFSampler()), ('detector', HalfSpaceTrees())),
        'svm_with_scalar_rbf': compose.Pipeline(('scale', StandardScaler()), ('sampler', fx.RBFSampler()),
                                                ('detector', OneClassSVM())),
        'svm_with_scalar': compose.Pipeline(('scale', StandardScaler()),('transform', fx.PolynomialExtender(degree=2, include_bias=True)), ('detector', OneClassSVM())),
        'svm_with_minmax': compose.Pipeline(('scale', StandardScaler()),
                                            ('transform', fx.PolynomialExtender(degree=2, include_bias=True)),
                                            ('detector', OneClassSVM())),

        # 'guassian_scorer': compose.Pipeline(('scale', StandardScaler()), ('detector', GaussianScorer())),
    }

    def __init__(self,algorithm:str = None,
                 use_standard_scaler:bool = True,use_minmax_scaler:bool = False,
                 use_polynomial_extender:bool = False,use_rbf_sampler:bool = False,
                 use_gaussian_scorer:bool = False,use_quantile_filter:bool = False,
                 use_threshold_filter:bool = False,anomaly_threshold:float = 0.9,
                 algo_one_class_svm:bool = False,algo_half_space_tree:bool = False,
                 debug:bool = False):

        if algorithm is not None:
            model_template = self.model_zoo.get(algorithm,None)
            self.model = model_template.clone() if model_template is not None else None
            if self.model is None:
                raise Exception('Model not found in model zoo')
        else:
            scalar = transformer = sampler = detector = filter = None

            # build model from params
            if use_standard_scaler:
                scalar = StandardScaler()
            if use_minmax_scaler:
                scalar = MinMaxScaler()
            if use_polynomial_extender:
                transformer = fx.PolynomialExtender(degree=2, include_bias=True)
            if use_rbf_sampler:
                sampler = fx.RBFSampler()
            if use_gaussian_scorer:
                detector = GaussianScorer()
            if algo_one_class_svm:
                detector = OneClassSVM()
            if algo_half_space_tree:
                detector = HalfSpaceTrees()
            if use_quantile_filter:
                filter = QuantileFilter(detector, q=anomaly_threshold)
            if use_threshold_filter:
                filter = ThresholdFilter(detector, threshold=anomaly_threshold)

            self.model = compose.Pipeline()
            for step in [("scalar",scalar), ("transformer",transformer), ("sampler",sampler)]:
                if step[1] is not None:
                    self.model |= step

            if filter:
                self.model |= ("filter",filter)
            else:
                self.model |= ("detector",detector)

            print(self.model)

    def in_schema(self) -> MultiMetricTimeseries:
        return self.input_schema

    def out_schema(self) -> AnomalyOutput:
        return self.output_schema

    def detect_anomaly(self, anreq: MultiMetricTimeseries, debug:bool = False) -> Tuple[ bool, float]:
        ''' detect anomalies in a timeseries using river'''

        data = anreq.get_data_as_dict()

        score = self.model.score_one(data)
        self.model = self.model.learn_one(data)

        if debug:
            print(self.model.debug_one(data))

        is_anomaly = self.model['filter'].classify(score) if 'filter' in self.model.steps else False


        return is_anomaly, score

    def learn_one_predict_one(self, input:MultiMetricTimeseries, debug:bool = False):
        is_anomaly, score = self.detect_anomaly(input, debug=debug)
        return AnomalyOutput(model=self.model, is_anomaly=is_anomaly, score=score, data=input)


if __name__ == '__main__':

    anomaly_detector = RiverAnomalyDetector()
    print(anomaly_detector.in_schema())
    #anomaly_output = anomaly_detector.learn_one_predict_one(input=MultiMetricTimeseries())
