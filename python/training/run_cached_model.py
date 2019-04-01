from joblib import load
from sklearn.pipeline import Pipeline


def main():
    filename = 'method_comment_pipeline.joblib'
    pipeline: Pipeline = load(filename)
    print(pipeline.steps)

if __name__ == '__main__':
    main()