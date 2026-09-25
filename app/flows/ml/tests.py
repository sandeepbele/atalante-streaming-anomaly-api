import unittest
from mlprocessor import RiverAnomalyDetector,MultiMetricTimeseries, AnomalyOutput


class MLProcessorTests(unittest.TestCase):

    def test_river_anomaly_detector_input_output_schema(self):
        detector = RiverAnomalyDetector()
        self.assertEqual(detector.in_schema(), detector.input_schema)
        self.assertEqual(detector.out_schema(), detector.output_schema)

    def test_river_anomaly_detector_detect_anomaly(self):

        metric_1 = [0,0,0,0,0,0,0,1,0,0,0,0,3,0,0,4,5,6,7,8,9,10,11,12,300,14,15,16,17,18 ]
        metric_2 = [0,0,0,0,0,0,0,0,0,0,2,3,0,0,0,4,5,6,7,8,9,10,11,12,500,14,15,16,17,18 ]
        #detector = RiverAnomalyDetector(algorithm="svm_with_minmax")
        #detector = RiverAnomalyDetector(algorithm="hs_tree_with_feature")
        detector  = RiverAnomalyDetector( use_standard_scaler=True,
                                          use_minmax_scaler=False,
                                          use_polynomial_extender=True,
                                          algo_one_class_svm=True,
                                          use_quantile_filter=True)

        for i in range(len(metric_1)):
            data = MultiMetricTimeseries(ds=f"2021-01-01T00:{i:02d}:00", data={"metric_1":metric_1[i], "metric_2":metric_2[i]})
            output = detector.learn_one_predict_one(data, debug=False)
            self.assertIsInstance(output, AnomalyOutput)
            print(f"{i} -{output.is_anomaly}, {output.score}")