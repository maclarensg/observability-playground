import time
import logging
from opentelemetry import metrics
from opentelemetry.exporter.otlp.proto.http.metric_exporter import OTLPMetricExporter
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configure the OTLP Exporter without the 'insecure' parameter
exporter = OTLPMetricExporter(
    endpoint="http://localhost:4318/v1/metrics",  # Alloy's OTLP HTTP endpoint
    # headers={"Authorization": "Bearer YOUR_TOKEN"}  # Uncomment and set if needed
)

# Create a Metric Reader with a collection interval (e.g., 5 seconds)
metric_reader = PeriodicExportingMetricReader(exporter, export_interval_millis=5000)

# Set up MeterProvider with the metric reader
meter_provider = MeterProvider(metric_readers=[metric_reader])
metrics.set_meter_provider(meter_provider)
meter = metrics.get_meter(__name__)

# Create a Counter metric without 'value_type'
request_counter = meter.create_counter(
    name="example_request_counter",
    description="Counts the number of requests",
    unit="1",
)

# Simulate metric recording with error handling
def generate_metrics():
    count = 0
    while True:
        try:
            count += 1
            # Record the metric
            request_counter.add(1, {"endpoint": "/home"})
            logger.info(f"Recorded request count: {count}")
            time.sleep(1)  # Wait for 1 second before next metric
        except Exception as e:
            logger.error(f"Error recording metric: {e}")
            time.sleep(5)  # Wait before retrying

if __name__ == "__main__":
    generate_metrics()
