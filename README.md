# Full Score Separator

This project provides a solution to separating full scores into each part of scores. Currently this is all of image manipulation without any OCR technique involved and we hope to add it in the future.

**Note. All of the scores fetched with this project should be only used in regard of learning, and we will not be responsible for anything invading copyright of the original music pieces.**

## Usage

### Environment setup

```shell
pip install pyqt6 numpy
```

### Process

**This part will be re-written after adding argument parsing**

- Prepare your full score (For instance, this may be achieved by fetching certain frames of a video via `ffmpeg`) in the form of a list of images, under `samples/imgs`
- Indicate all of the instrument parts in `sample_config.json`
- Run `python main.py`. Then you will see a GUI for line annotation.
- **Click** on the scrollbar to indicate a line for segment. *We will add dragging support for preview in the future*.
- `Undo` for discarding the last line, `Discard annotations` for clearing all of the annotations
- Click `Next page` if you believe your annotation has been fine. The completeness will be checked and you will be able to proceed if ad only if the annotation has been all right. The previous annotation will be automatically applied to the new page, and if there are error, just discard them to make a new annotation.
- If you meet duplicated pages, `discard page` will help.
- If you believe you have completed all, `Export` all of the stuff and they will be under `./output`. 

