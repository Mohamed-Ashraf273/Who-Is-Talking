import argparse
import multiprocessing
import pipeline
import time


def main(
    mode,
    features_file_path,
    datapath,
    audio_test_path,
    test_file_path,
    model_selected,
    grid_search,
    val,
    save_test,
    save_val,
):
    if mode == "train":
        pipeline.dev(
            features_file_path=features_file_path,
            model=model_selected,
            train=True,
            grid_search=grid_search,
            save_test=save_test,
            save_val=save_val,
        )
    elif mode == "features":
        pipeline.dev(datapath=datapath, train=False)
    elif mode == "validate":
        pipeline.predict_all(test_file_path, val=val, model_selected=model_selected)
    elif mode == "predict":
        start = time.time()
        predictions = pipeline.final_out(audio_test_path, model_selected=model_selected)
        end = time.time()
        with open(f"./results.txt", "w") as f:
            for pred in predictions:
                f.write(f"{pred}\n")
        with open("./time.txt", "w") as f:
            f.write(str(round(end - start, 3)))

    else:
        raise ValueError(
            "Invalid mode. Choose from 'train', 'features', 'validate' or 'predict'."
        )


if __name__ == "__main__":
    multiprocessing.freeze_support()

    parser = argparse.ArgumentParser(description="Voice project pipeline")

    parser.add_argument(
        "mode",
        choices=["train", "features", "validate", "predict"],
        help="Mode to run: 'train', 'features', 'validate' or 'predict'",
    )

    parser.add_argument("--features", default=None, help="Path to features file")
    parser.add_argument("--datapath", default=None, help="Path to voice project data")
    parser.add_argument("--audiopath", default=None, help="Path to audio test data")
    parser.add_argument(
        "--testfile", default=None, help="Path to test file for validation"
    )
    parser.add_argument(
        "--model", default="stacking", help="Model to use (default: stacking)"
    )
    parser.add_argument(
        "--gridsearch", action="store_true", help="Enable grid search for training"
    )
    parser.add_argument(
        "--val",
        action="store_true",
        help=" Val (default: False), enable it when the file is already normalized",
    )
    parser.add_argument(
        "--save_test",
        action="store_true",
        help="Save test results during training (default: False)",
    )
    parser.add_argument(
        "--save_val",
        action="store_true",
        help="Save validation results during training (default: False)",
    )

    args = parser.parse_args()

    main(
        mode=args.mode,
        features_file_path=args.features,
        datapath=args.datapath,
        audio_test_path=args.audiopath,
        test_file_path=args.testfile,
        model_selected=args.model,
        grid_search=args.gridsearch,
        val=args.val,
        save_test=args.save_test,
        save_val=args.save_val,
    )
