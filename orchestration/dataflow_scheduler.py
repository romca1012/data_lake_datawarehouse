import apache_beam as beam
from apache_beam.options.pipeline_options import PipelineOptions
import schedule
import time

def run_job():
    options = PipelineOptions()
    with beam.Pipeline(options=options) as p:
        (
            p
            | "Dummy job" >> beam.Create([1])
            | "Log" >> beam.Map(lambda _: print("Job Beam exécuté."))
        )

schedule.every(10).minutes.do(run_job)

if __name__ == "__main__":
    print("Lancement orchestration. Toutes les 10 minutes.")
    while True:
        schedule.run_pending()
        time.sleep(1)
